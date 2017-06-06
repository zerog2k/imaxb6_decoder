# imaxb6_decoder
imax b6 serial data decoder

Decodes log stream from Imax B6 charger serial UART output port

works on a Imax B6 charger [like this one from Banggood:](https://www.banggood.com/Wholesale-IMAX-B6-Digital-RC-Lipo-NiMH-battery-Balance-Charger-p-46220.html?p=WX0407753399201409DA)

![image of Imax B6 charger at Banggood.com](https://img1.banggood.com/thumb/large/upload/SKU035917/20120601164150545.jpg?p=WX0407753399201409DA)

## hardware
temperature sensor port pinout (front to back): GND, TXD, VCC

*note:* "USB/Temp Select" must be in "USB" (really: serial UART) mode to output data

use a cheap usb-serial UART adapter, e.g. CP2102, FTDI 232, PL2303, etc

## usage

```
$ ./decode_imaxb6.py --help
usage: decode_imaxb6.py [-h] [-d] -p PORT [-i INTERVAL] [-f FILE]

decodes serial output from Imax B6 chargers

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           debug output
  -p PORT, --port PORT
  -i INTERVAL, --interval INTERVAL
                        minimum output interval in seconds, default: 1
  -f FILE, --file FILE  also log to file
```

## example output
```
2016-12-10 21:07:19, mode:   NiCd, time:  78 m, Running, Charge, Cycle, Vin: 15.03 V, Vout: 4.72 V, Iout: 0.3 A, Cout:  368 mAh
2016-12-10 21:08:20, mode:   NiCd, time:  79 m, Running, Charge, Cycle, Vin: 15.02 V, Vout: 4.73 V, Iout: 0.3 A, Cout:  373 mAh
2016-12-10 21:09:21, mode:   NiCd, time:  80 m, Running, Charge, Cycle, Vin: 15.02 V, Vout: 4.62 V, Iout: 0.3 A, Cout:  377 mAh
2016-12-10 21:10:22, mode:   NiCd, time:  81 m, Running, Charge, Cycle, Vin: 14.97 V, Vout: 4.72 V, Iout: 0.3 A, Cout:  383 mAh
2016-12-10 21:11:22, mode:   NiCd, time:  82 m, Running, Charge, Cycle, Vin: 15.00 V, Vout: 4.72 V, Iout: 0.3 A, Cout:  388 mAh
2016-12-10 21:12:23, mode:   NiCd, time:  83 m, Running, Charge, Cycle, Vin: 15.03 V, Vout: 4.71 V, Iout: 0.3 A, Cout:  393 mAh
2016-12-11 09:01:00, mode:   NiCd, time:  83 m, Running, Charge, Cycle, Vin: 15.01 V, Vout: 4.70 V, Iout: 0.3 A, Cout:  394 mAh
```

## references
https://blog.dest-unreach.be/2012/01/29/imax-b6-charger-protocol-reverse-engineered/comment-page-1
