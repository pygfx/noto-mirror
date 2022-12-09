#!/usr/bin/env python3
"""

This script processes the font files, and generates the website.

"""

import os
import json

import freetype

from categories import EXPECTED_FONTS


this_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
fonts_dir = os.path.join(this_dir, "fonts")


# %% List font files

filemap = {}
for fname in os.listdir(fonts_dir):
    family_without_spaces = fname.split("-")[0]
    filemap[family_without_spaces] = fname


# %% Create the index

# The main font should come first
assert EXPECTED_FONTS[0] == "Noto Sans"

# Prepare data structure
noto_default_index = {
    "fonts": [],
    "index": {},
}

# Get codepoints of the main font
fname = filemap["NotoSans"]
face = freetype.Face(os.path.join(fonts_dir, fname))
main_codepoints = set(i for i, _ in face.get_chars())

# Add them to the map
for codepoint in main_codepoints:
    noto_default_index["index"][codepoint] = [0]

# Now add the codepoints of the other fonts. For codepoints that
# are covered by the main font, we only register the main font.
# In all other cases we list all fonts that support a codepoint.
for font_index, family in enumerate(EXPECTED_FONTS):
    fname = filemap[family.replace(" ", "")]
    face = freetype.Face(os.path.join(fonts_dir, fname))
    noto_default_index["fonts"].append(fname)
    codepoints = set(i for i, _ in face.get_chars())
    for codepoint in codepoints:
        if codepoint not in main_codepoints:
            x = noto_default_index["index"].setdefault(codepoint, [])
            x.append(font_index)

# Write index to disk. By using indent, changes are nicely tracked in git.
filename = os.path.join(this_dir, "meta", "noto_default_index.json")
with open(filename, "wt", encoding="utf-8") as f:
    json.dump(noto_default_index, f, indent=0)


# %% Write stats

# Get memory consumption
getsize = lambda fname: os.path.getsize(os.path.join(fonts_dir, fname))  # noqa
total_size = sum(getsize(fname) for fname in os.listdir(fonts_dir))
total_size_mb = total_size / 2**20

md = f"""# Noto mirror stats

* Number of fonts in the default set: {len(EXPECTED_FONTS)}
* Memory consumption: {total_size_mb:0.1f} MB
* Unicode code points: {len(noto_default_index['index'])}

"""

# Write stats to disk
filename = os.path.join(this_dir, "meta", "stats.md")
with open(filename, "wb") as f:
    f.write(md.encode())
