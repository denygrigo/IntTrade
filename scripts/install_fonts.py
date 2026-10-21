#!/usr/bin/env python3
"""Explicit, optional installer for OFL Google Fonts; never commit font binaries."""
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
from hashlib import sha256
from subprocess import run
import argparse

GOOGLE_FONTS_COMMIT="45e3d5269e4a17d823f6d84470bc084dc5ae46f6"
BASE="https://raw.githubusercontent.com/google/fonts/"+GOOGLE_FONTS_COMMIT+"/ofl/"
FONTS={
 "inter":"Inter[opsz,wght].ttf",
 "manrope":"Manrope[wght].ttf",
 "lora":"Lora[wght].ttf",
 "dmsans":"DMSans[opsz,wght].ttf",
 "plusjakartasans":"PlusJakartaSans[wght].ttf",
 "playfairdisplay":"PlayfairDisplay[wght].ttf",
 "ibmplexsans":"IBMPlexSans[wdth,wght].ttf",
 "librebaskerville":"LibreBaskerville[wght].ttf",
 "montserrat":"Montserrat[wght].ttf",
 "sourcesans3":"SourceSans3[wght].ttf",
}
def get(url):
    with urlopen(url,timeout=40) as r:
        return r.read(5_000_001)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--install",action="store_true")
    args=p.parse_args()
    if not args.install:
        print("Dry-run: 10 open-license families from a pinned Google Fonts commit:")
        print(*FONTS.items(),sep="\n")
        print("Use --install only where outbound network access and local font installation are allowed.")
        return
    dest=Path.home()/".local/share/fonts/inttrade"
    dest.mkdir(parents=True,exist_ok=True)
    for family,name in FONTS.items():
        target=dest/name
        if target.is_file() and target.stat().st_size>30000:
            print("PRESENT",name)
            continue
        base=BASE+family+"/"
        license_data=get(base+"OFL.txt")
        if not license_data.startswith(b"SIL OPEN FONT LICENSE") and b"OPEN FONT LICENSE" not in license_data[:1000].upper():
            raise RuntimeError("Cannot validate OFL license for "+family)
        font=get(base+quote(name,safe=""))
        if len(font)<30000 or font[:4] not in (b"OTTO",b"ttcf",bytes([0,1,0,0])):
            raise RuntimeError("Invalid font data from "+base+name)
        (dest/(family+"-OFL.txt")).write_bytes(license_data)
        target.write_bytes(font)
        print("INSTALLED",name,"sha256",sha256(font).hexdigest())
    try:
        run(["fc-cache","-f",str(dest)],check=True,timeout=90)
    except FileNotFoundError:
        print("WARN: fc-cache unavailable. Refresh font cache manually.")
    print("Installed fonts for current user only; verify with fc-match and actual slide rendering.")
if __name__=="__main__":main()
