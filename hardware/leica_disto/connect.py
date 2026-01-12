#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Connect to Leica DISTO via Bluetooth and send measurements as keyboard input
"""
import asyncio
import struct
from bleak import BleakScanner, BleakClient
from pynput.keyboard import Controller, Key

DISTO_NAME = "DISTO"

keyboard = Controller()

def on_measure(sender, data):
    try:
        # Conversion float 32 → mètres
        val_m = struct.unpack('<f', data)[0]

        # Conversion en mm
        val_mm = int(round(val_m * 1000))

        # Transformer en chaîne
        text = str(val_mm)

        # Simuler la frappe clavier
        for c in text:
            keyboard.press(c)
            keyboard.release(c)

        # Entrée
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        print(f"Mesure envoyée au clavier: {text} mm")

    except Exception:
        print("Erreur sur la donnée brute:", data)

async def main():
    devices = await BleakScanner.discover(timeout=5)
    disto = next((d for d in devices if d.name and DISTO_NAME in d.name), None)
    if disto is None:
        print("DISTO non trouvé")
        return

    async with BleakClient(disto) as client:
        print("Connecté au DISTO")
        services = client.services

        chars = []
        for service in services:
            # Skip standard GATT services (16-bit UUIDs in the 0000XXXX-0000-1000-8000-00805f9b34fb format)
            service_uuid = service.uuid.lower()
            if service_uuid.startswith("0000") and service_uuid.endswith("-0000-1000-8000-00805f9b34fb"):
                continue
            
            for char in service.characteristics:
                if "notify" in char.properties or "indicate" in char.properties:
                    chars.append(char)

        if not chars:
            print("Aucune characteristic notify/indicate trouvée")
            return

        for char in chars:
            print("Abonnement sur", char.uuid, char.properties)
            try:
                await client.start_notify(char.uuid, on_measure)
            except Exception as e:
                print(f"Erreur lors de l'abonnement à {char.uuid}: {e}")
                continue

        print("👉 Appuie sur MESURE sur le DISTO")
        print("Ctrl+C pour quitter")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
