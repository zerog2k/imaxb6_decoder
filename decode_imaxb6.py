#!/usr/bin/env python

## imax b6 serial data decoder
## temperature sensor port pinout (front to back): GND, TXD, VCC
## note: "USB/Temp Select" must be in "USB" mode to output data
## 
## Jens Jensen 2016
## reference https://blog.dest-unreach.be/2012/01/29/imax-b6-charger-protocol-reverse-engineered/comment-page-1
##

import serial
import struct
import os
import datetime
import argparse

ap = argparse.ArgumentParser(description="decodes serial output from Imax B6 chargers")
ap.add_argument("-d", "--debug", action="store_true",
                help="debug output")
ap.add_argument("-p", "--port", required=True)
args = ap.parse_args()

DEBUG = args.debug
PORT = args.port
MSG_SIZE = 72

def cksum(data):
    sum = 0;
    for b in data:
        sum += b
    return sum & 0xFF

def verify(body):
    checksum_calc = cksum(body[0:MSG_SIZE])
    checksum_actual = body[MSG_SIZE] << 4 & 0xF0 | body[MSG_SIZE+1] & 0xF
    #print "cksum_calc: %x, cksum_actual: %x" % (checksum_calc, checksum_actual)
    if checksum_actual == checksum_calc:
        return True
    else:
        return False

def two_byte_float(body, b1):
    return body[b1] + body[b1+1] / 100.0

def two_byte_int(body, b1):
    return body[b1] * 100 + body[b1+1]  

def hexprint(data, addrfmt=None):
    """Return a hexdump-like encoding of @data"""
    ## handy function borrowed from Chirp project
    if addrfmt is None:
        addrfmt = '%(addr)03i'

    block_size = 8

    lines = len(data) / block_size

    if (len(data) % block_size) != 0:
        lines += 1
        data += "\x00" * ((lines * block_size) - len(data))

    out = ""

    for block in range(0, (len(data)/block_size)):
        addr = block * block_size
        try:
            out += addrfmt % locals()
        except (OverflowError, ValueError, TypeError, KeyError):
            out += "%03i" % addr
        out += ': '

        left = len(data) - (block * block_size)
        if left < block_size:
            limit = left
        else:
            limit = block_size

        for j in range(0, limit):
            out += "%02x " % ord(data[(block * block_size) + j])

        out += "  "

        for j in range(0, limit):
            char = data[(block * block_size) + j]

            if ord(char) > 0x20 and ord(char) < 0x7E:
                out += "%s" % char
            else:
                out += "."

        out += "\n"

    return out

## address map

ADDR_CONFIG = 0
ADDR_NICD_SENS = 1
ADDR_NIMH_SENS = 2
ADDR_TEMP_CUTOFF = 3
ADDR_CHG_DCHG_WASTE_TIME = 4

ADDR_INPUT_VOLTAGE_CUTOFF = 6
ADDR_CHARGE_STATE = 7
ADDR_NICD_SET_CHARGE_CURRENT = 8
ADDR_NICD_SET_DISCHARGE_CURRENT = 9

ADDR_NIMH_SET_CHARGE_CURRENT = 12
ADDR_NIMH_SET_DISCHARGE_CURRENT = 13
ADDR_CYCLE_MODE = 14
ADDR_CYCLE_COUNT = 15
ADDR_LI_SET_CHARGE_CURRENT = 16
ADDR_LI_SET_CHARGE_CELL_COUNT = 17
ADDR_LI_SET_DISCHARGE_CURRENT = 18
ADDR_LI_SET_DISCHARGE_CELL_COUNT = 19
ADDR_PB_SET_CHARGE_CURRENT = 20
ADDR_PB_SET_CELL_COUNT = 21
ADDR_MODE = 22
MODES = ["Config", "Li", "NiMH", "NiCd", "Pb", "Save", "Load"]

ADDR_CHARGE_STATE = 23
ADDR_NIMH_SET_DISCHARGE_VOLTAGE = 24
ADDR_NICD_SET_DISCHARGE_VOLTAGE = 26
ADDR_SAFETY_TIMER = 29
ADDR_CAPACITY_CUTOFF = 30

ADDR_IOUT = 32
ADDR_VOUT = 34
ADDR_VIN = 40
ADDR_CHARGE_OUT = 42
ADDR_LI_CELL_VOLTAGES = 44
ADDR_CHARGE_TIME = 68


## start

ser = serial.Serial(PORT, 9600, bytesize=serial.SEVENBITS)

msg = ""
b = ser.read()
while b is not None:
    b = ser.read()
    if b != '{':
        continue
    msg = ser.read(MSG_SIZE+2)
    if ser.read() != '}':
        continue
    msgbytes = bytearray(msg)
    valid = verify(msgbytes)

    if DEBUG:
        print "%s cnt: %d cksum: %X cksum_verify: %s" % \
            ( hexprint(msg), len(msgbytes), cksum(msgbytes[0:MSG_SIZE]), valid)
    if valid:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Vin = two_byte_float(msgbytes, ADDR_VIN)
        Iout = two_byte_float(msgbytes, ADDR_IOUT)
        Vout = two_byte_float(msgbytes, ADDR_VOUT)
        Cout = two_byte_int(msgbytes, ADDR_CHARGE_OUT) 
        time = two_byte_int(msgbytes, ADDR_CHARGE_TIME)
        print "%s, time: %3d m, Vin: %0.2f V, Vout: %0.2f V, Iout: %0.1f A, Cout: %4d mAh" % \
            (dt, time, Vin, Vout, Iout, Cout)
    


