#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coin_diag.py - ST-001 wiring test  (RUN THIS FIRST after wiring)
================================================================
Shows the raw bytes arriving on the serial port so you can verify
your wiring before running the fun stuff.

    sudo python3 coin_diag.py

Drop a few coins. GOOD output looks like complete lines:

    b'value:30,frequency:213\r\n'

If you see NOTHING          -> check wiring (TX->RX? common GND?) and
                               make sure no other program holds the port.
If you see BROKEN FRAGMENTS -> the serial login console is stealing
   (b'v', b'cy:213\n')         bytes:  sudo raspi-config ->
                               Interface Options -> Serial Port ->
                               login shell NO / hardware YES -> reboot.
If you see GARBAGE BYTES    -> wrong baud; the ST-001 speaks 115200.
"""
import serial

PORT = "/dev/serial0"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
ser.reset_input_buffer()
print(f"Listening on {PORT} @ {BAUD} ... drop a few coins, then Ctrl+C")
print("-" * 46)
got = 0
try:
    while True:
        n = ser.in_waiting
        data = ser.read(n or 1)
        if data:
            got += len(data)
            print(repr(data))
except KeyboardInterrupt:
    print("-" * 46)
    print(f"Done. Received {got} bytes total.")
    ser.close()
