#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scan for nearby Bluetooth devices and list them in the console
to help identify the Leica DISTO device to define in connect.py.
"""
import asyncio
from bleak import BleakScanner

async def main():
    devices = await BleakScanner.discover(timeout=5)
    for d in devices:
        print(d)

asyncio.run(main())
