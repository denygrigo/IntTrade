#!/usr/bin/env python3
"""Fontconfig inventory for the current runtime, not a guarantee of embedding."""
import shutil
import subprocess

families = [
    "Inter", "Manrope", "IBM Plex Sans", "DM Sans", "Plus Jakarta Sans",
    "Lora", "Libre Baskerville", "Playfair Display", "Noto Sans",
    "Liberation Sans", "Aptos"
]

if not shutil.which("fc-list"):
    print("Fontconfig unavailable. FONT STATUS: NOT TESTED")
else:
    output = subprocess.check_output(["fc-list", ":", "family"], text=True, errors="replace")
    installed = {item.strip().lower() for line in output.splitlines() for item in line.split(",")}
    for font in families:
        print(("FOUND" if font.lower() in installed else "MISSING"), font)
    print("Font listing is not proof that a particular Office viewer preserves appearance.")
