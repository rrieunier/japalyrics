# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime

import yaml
from furigana import Furigana

with open("src/metadata.yml", "r") as f:
    meta = yaml.safe_load(f)
    song = meta.get("song", "")
    artist = meta.get("artist", "")
    year = meta.get("year", "")
    exceptions = meta.get("exceptions", {})

with open("src/en.txt", "r") as f:
    en = [l.rstrip("\n") for l in f.readlines()]
with open("src/jp.txt", "r") as f:
    jp = [l.rstrip("\n") for l in f.readlines()]

assert len(en) == len(jp), f"{len(en)=} mismatches {len(jp)=}"

# Saves input files
run_id = f"{artist}-{song}".replace(" ", "_") + "-" + datetime.now().isoformat().replace(":", "_")
output_dir = os.path.join("hist", run_id)

dest = ["<html><body>",
        '<link rel="stylesheet" href="file:///Users/romanrieunier/PycharmProjects/japalyrics/be/dst/style.css"/>',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">',
        '<div class="header">', f"<h1>{song}</h1>", f"<h2>{artist} - {year}</h2>", "</div>", "<hr/>",
        '<div class="lyrics">']

furigana = Furigana(exceptions=exceptions)

open_verse = False
for e, j in zip(en, jp):
    if not e.strip():
        dest.append('<p class="sep"></p>')
    elif e.startswith("["):
        if open_verse:
            dest.append("</div>")
        dest.append('<div class="verse">')
        open_verse = True
        dest.append(f'<p class="desc">{e}</p>')
    elif e.strip() == j.strip():
        dest.append('<div class="group">')
        dest.append(f'<p class="en">{e}</p>')
        dest.append('</div>')
    else:
        dest.append('<div class="group">')
        dest.append(f'<p class="en">{e}</p>')
        # MeCab doesn't handle spaces/line breaks well
        j2 = j.split(" ")
        j2 = " ".join(furigana.to_html(_) for _ in j2)
        dest.append(f'<p class="jp">{j2}</p>')
        dest.append('</div>')

if open_verse:
    dest.append("</div>")
dest.append("</div>")
dest.append("</body></html>")

shutil.copytree("src", output_dir)

with open(os.path.join(output_dir, "output.html"), "w") as f:
    f.writelines(dest)
with open(f"dst/output.html", "w") as f:
    f.writelines(dest)

print(f"🎤  Done 🎶  saved to {output_dir}")
