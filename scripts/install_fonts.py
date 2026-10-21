#!/usr/bin/env python3
"""Optional installer for open-licensed fonts from google/fonts. Run only when needed."""
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import argparse
import hashlib
import subprocess

FONTS = {
    "inter": "Inter[opsz,wght].ttf",
    "manrope": "Manrope[wght].ttf",
    "lora": "Lora[wght].ttf",
    "dmsans": "DMSans[opsz,wght].ttf",
    "plusjakartasans": "PlusJakartaSans[wght].ttf",
    "playfairdisplay": "PlayfairDisplay[wght].ttf",
    "ibmplexsans": "IBMPlexSans[wdth,wght].ttf",
}
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true", help="explicitly download and install fonts")
    args = parser.parse_args()
    folder = Path.home() / ".local/share/fonts/inttrade"
    if not args.install:
        print("Dry run only. Fonts from https://github.com/google/fonts (SIL OFL):")
        for name, file in FONTS.items(): print(name, file)
        print("Run with --install only if network and installation are permitted.")
        return
    folder.mkdir(parents=True, exist_ok=True)
    for family, filename in FONTS.items():
        url = "https://raw.githubusercontent.com/google/fonts/main/ofl/" + family + "/" + quote(filename)
        with urlopen(url, timeout=30) as response:
            data = response.read(5000000)
        if len(data) < 30000 or data[:4] not in (bytes([0,1,0,0]), b"OTTO", b"ttcf"):
            raise RuntimeError("Invalid or unexpectedly small font from " + url)
        dest = folder / filename
        dest.write_bytes(data)
        print("INSTALLED", filename, "sha256=" + hashlib.sha256(data).hexdigest())
    try:
        subprocess.run(["fc-cache","-f",str(folder)],check=True)
    except FileNotFoundError:
        print("fc-cache missing; manually refresh font cache if necessary.")
    print("Fonts installed for THIS user only; Codex Cloud sessions may not persist them.")
if __name__ == "__main__":
    main()
