#!/usr/bin/env bash
# Install a curated group of Google Fonts OFL variable fonts to this user's environment.
# Downloads from one PINNED upstream google/fonts commit, never writes into Git.
set -euo pipefail
command -v curl >/dev/null || { echo "curl required" >&2; exit 2; }
command -v fc-cache >/dev/null || { echo "fontconfig (fc-cache) required" >&2; exit 2; }
PIN="45e3d5269e4a17d823f6d84470bc084dc5ae46f6"
BASE="https://raw.githubusercontent.com/google/fonts/${PIN}/ofl"
DEST="${HOME}/.local/share/fonts/IntTrade"
mkdir -p "$DEST"
fetch() {
  local family="$1" file="$2" dst="$DEST/$2"
  if [ -s "$dst" ]; then echo "EXISTS $file"; return; fi
  local tmp="$dst.part"
  echo "Downloading $family / $file"
  curl --fail --silent --show-error --location --globoff --retry 1 --connect-timeout 10 --max-time 100 \
       "$BASE/$family/$file" -o "$tmp"
  test -s "$tmp" || { rm -f "$tmp"; return 1; }
  mv "$tmp" "$dst"
}
while IFS='|' read -r family file; do
  [ -n "$family" ] || continue
  fetch "$family" "$file"
  fetch "$family" "OFL.txt" || echo "WARN: verify license manually for $family"
done <<'FONTS'
inter|Inter[opsz,wght].ttf
manrope|Manrope[wght].ttf
dmsans|DMSans[opsz,wght].ttf
ibmplexsans|IBMPlexSans[wdth,wght].ttf
lora|Lora[wght].ttf
librebaskerville|LibreBaskerville[wght].ttf
playfairdisplay|PlayfairDisplay[wght].ttf
plusjakartasans|PlusJakartaSans[wght].ttf
montserrat|Montserrat[wght].ttf
sourcesans3|SourceSans3[wght].ttf
FONTS
fc-cache -f "$DEST"
echo "Font installation attempted in $DEST."
echo "Inspect actual font matches using: fc-match Inter; fc-match 'IBM Plex Sans'; fc-match Manrope"
echo "Project Git content does NOT make fonts available on other machines."
