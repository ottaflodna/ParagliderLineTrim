#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 13:56:40 2026

@author: loic
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
            for char in service.characteristics:
                if "notify" in char.properties or "indicate" in char.properties:
                    chars.append(char)

        if not chars:
            print("Aucune characteristic notify/indicate trouvée")
            return

        for char in chars:
            print("Abonnement sur", char.uuid, char.properties)
            await client.start_notify(char.uuid, on_measure)

        print("👉 Appuie sur MESURE sur le DISTO")
        print("Ctrl+C pour quitter")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
