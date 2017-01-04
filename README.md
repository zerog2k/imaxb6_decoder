# imaxb6_decoder
imax b6 serial data decoder

Decodes log stream from Imax B6 charger serial UART output port

## hardware
temperature sensor port pinout (front to back): GND, TXD, VCC

*note:* "USB/Temp Select" must be in "USB" (really: serial UART) mode to output data

use a cheap usb-serial UART adapter, e.g. CP2102, FTDI 232, PL2303, etc

## references
https://blog.dest-unreach.be/2012/01/29/imax-b6-charger-protocol-reverse-engineered/comment-page-1
