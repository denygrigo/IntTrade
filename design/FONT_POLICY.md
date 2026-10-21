# Font policy

Curated families: Inter, Manrope, DM Sans, IBM Plex Sans, Lora, Libre Baskerville, Playfair Display, Plus Jakarta Sans, Montserrat and Source Sans 3.

These are font preferences, not proof of runtime availability. A reproducible, **optional** setup script `bash scripts/setup_fonts.sh` downloads pinned files directly from the Google Fonts repository under their Open Font Licenses into the current user's font directory. It does not commit or share font binaries. Verify each run by `fc-match "Font Family"`, render the final artifact, and check font substitution.

Prefer pairing one editorial serif with a neutral contemporary sans when appropriate. For research reading decks prioritize open, readable, predictable text faces; for premium brand decks a more expressive headline typeface may be justified.

Fallbacks: Liberation Sans, Aptos, Arial and Noto Serif (verify actual platform font availability). PowerPoint recipients may see substitution unless fonts are installed or suitable embedding is permitted. Never assume that a font installed on Codex Cloud is available on an iPhone or a recipient's computer.

Source: https://github.com/google/fonts (pinned commit 45e3d5269e4a17d823f6d84470bc084dc5ae46f6); fonts supplied under their individual OFL.txt license files, downloaded only on demand.
