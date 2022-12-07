#!/usr/bin/env python3
"""

This script uses the Google font API to get a list of Noto fonts, make
a selection and then download them.

This file is organized as a script with cells that can be executed
individually in some IDE's to allow easy maintenance.

To use this script you need an API key, which you can obtain at
https://developers.google.com/fonts

"""


# %% Init

import os
import sys
import json
import time
import shutil

import requests
import freetype

from categories import FONTS_PER_CATEGORY, EXPECTED_FONTS


this_dir = os.path.dirname(os.path.abspath(__file__))
fonts_dir = os.path.join(this_dir, "fonts")


# %% Download index from Google

# Obtain the API key, either from the environ or a CLI arg.
api_key1 = os.getenv("GOOGLE_FONTS_API_KEY", "")
api_key2 = sys.argv[1] if len(sys.argv) == 2 else ""
api_key = api_key1 or api_key2
assert api_key, "Need Google API key!"

# Download font list
url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}"
res = requests.get(url).json()
all_google_fonts = res["items"]


# %% Select fonts that we condider default

print(f"Found {len(all_google_fonts)} Google fonts")

# Select all Noto fonts
all_noto_fonts = {}
for item in all_google_fonts:
    family = item["family"]
    if family.startswith("Noto "):
        all_noto_fonts[family] = item

print(f"Of these, {len(all_noto_fonts)} are Noto fonts")

# Collect Sans fonts
default_noto_fonts = {}
for family, item in all_noto_fonts.items():
    parts = family.split()
    if parts[1] == "Sans":
        default_noto_fonts[family] = item

# Use another variant for script that do not have Sans
for family, item in all_noto_fonts.items():
    parts = family.split()
    if parts[1] != "Sans":
        sans_equivalent = " ".join([parts[0], "Sans", *parts[2:]])
        if sans_equivalent not in default_noto_fonts or len(parts) == 2:
            default_noto_fonts[family] = item

print(f"Initially selected {len(default_noto_fonts)} Sans fonts")

# Now we'll exclude fonts ...

# Remove alt fonts
for family in list(default_noto_fonts.keys()):
    if family.endswith(("Looped", "Unjoined", "Supplement")):
        family_alt = family.rsplit(" ", 1)[0]
        if family_alt in default_noto_fonts:
            default_noto_fonts.pop(family)
            print("Drop alt font:", family)

EXCLUDES = {
    "Noto Color Emoji",
    "Noto Serif",
    "Noto Sans Mono",
    "Noto Sans Display",
}

# Remove specific fonts
for family in EXCLUDES:
    default_noto_fonts.pop(family)
print(f"Dropped {len(EXCLUDES)} more fonts")


# %% Compare with our list

# Compare the selected fonts with our expectation
unexpected = set(default_noto_fonts).difference(EXPECTED_FONTS)
missing = set(EXPECTED_FONTS).difference(default_noto_fonts)

# Report ...

if unexpected:
    print()
    print("The following fonts are selected, but not categorized.")
    print("We should either add them to the categories-list,")
    print("or exclude them from the selection.")
    print(unexpected)

if missing:
    print()
    print("The following fonts are categorized but not selected.")
    print("We should either remove them from the categories-list,")
    print("or check if our selection is broken.")
    print(missing)

if unexpected or missing:
    raise RuntimeError("Cannot proceed")
else:
    print("Selected fonts match expected fonts.")


# %% Establish filenames

for family, item in default_noto_fonts.items():
    download_url = item["files"]["regular"]
    ext = download_url.split(".")[-1]
    parts = [x.capitalize() for x in family.split()]
    parts += ["-Regular", ".", ext]
    item["fname"] = "".join(parts)


# %% Download font files


# Prep download
shutil.rmtree(fonts_dir, ignore_errors=True)
os.mkdir(fonts_dir)

# Download all default fonts
print("\rDownloading ...", end="")
for i, (family, item) in enumerate(default_noto_fonts.items()):
    download_url, fname = item["files"]["regular"], item["fname"]
    print(f"\rDownloading {i}/{len(default_noto_fonts)}: {fname}", end="")
    r = requests.get(download_url)
    assert r.ok
    blob = r.content
    with open(os.path.join(fonts_dir, fname), "wb") as f:
        f.write(blob)
    time.sleep(0.01)

print(f"\rDownloaded {len(default_noto_fonts)} fonts.")


# %% Make the web page


# base_url = "https://raw.githubusercontent.com/pygfx/noto-mirror/main/fonts/"
base_url = "https://pygfx.github.io/noto-mirror/fonts/"

html = """<!DOCTYPE html>
<html>
<head>
    <title>Noto font mirror</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<style>
body {
    color: #000;
    font-family: Ubuntu,"Helvetica Neue",Arial,sans-serif;
}
a:link, a:visited, a:active {
    color: #36C;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
a.anchorlink {
    color: #555;
    margin-right: 7px;
}
a.anchorlink:hover {
    text-decoration: none;
}
li:target { background: #dfd; }
</style>

<body>

<h1>Noto font mirror</h1>
"""

for category, families in FONTS_PER_CATEGORY.items():
    html += f"\n<h2 id='{category}'>{category}</h2>\n\n"
    html += "<ul>\n"
    for family in sorted(families):
        item = default_noto_fonts[family]
        fname = item["fname"]
        filename = os.path.join(fonts_dir, fname)
        size = int(os.path.getsize(filename) / 2**10)  # in kb
        size_s = f"{size/1000:0.3f} MB" if size > 1000 else f"{size} KB"
        url = base_url + fname
        html += f"<li id='{fname}'><a class='anchorlink' href='#{fname}'>#</a>"
        html += f"{family}: <a href='{url}'>Regular</a> ({size_s})</li>\n"
    html += "</ul>\n"

html += "\n</body>/n</html>\n\n"


with open(os.path.join(this_dir, "index.html"), "wb") as f:
    f.write(html.encode())


# %% Create the index

assert EXPECTED_FONTS[0] == "Noto Sans"

# Prepare data structure
noto_default_index = {
    "fonts": [],
    "index": {},
}

# Get codepoints of the main font
fname = default_noto_fonts["Noto Sans"]["fname"]
face = freetype.Face(os.path.join(fonts_dir, fname))
main_codepoints = set(i for i, _ in face.get_chars())

# Add them to the map
for codepoint in main_codepoints:
    noto_default_index["index"][codepoint] = [0]

# Now add the codepoints of the other fonts. For codepoints that
# are covered by the main font, we only register the main font.
# In all other cases we list all fonts that support a codepoint.
for font_index, family in enumerate(EXPECTED_FONTS):
    fname = default_noto_fonts[family]["fname"]
    face = freetype.Face(os.path.join(fonts_dir, fname))
    noto_default_index["fonts"].append(fname)
    codepoints = set(i for i, _ in face.get_chars())
    for codepoint in codepoints:
        if codepoint not in main_codepoints:
            x = noto_default_index["index"].setdefault(codepoint, [])
            x.append(font_index)

# Write index to disk
filename = os.path.join(this_dir, "info", "noto_default_index.json")
with open(filename, "wt", encoding="utf-8") as f:
    json.dump(noto_default_index, f)


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
filename = os.path.join(this_dir, "info", "stats.md")
with open(filename, "wb") as f:
    f.write(md.encode())
