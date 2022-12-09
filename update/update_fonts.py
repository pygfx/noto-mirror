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
import time
import shutil

import requests

from categories import EXPECTED_FONTS


this_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
fonts_dir = os.path.join(this_dir, "fonts")


# %% Download index from Google

# Obtain the API key, either from the environ or a CLI arg.
api_key = os.getenv("GOOGLE_FONTS_API_KEY", "")
assert api_key, "You need to set the GOOGLE_FONTS_API_KEY environment variable."

# Download font list
url = f"https://www.googleapis.com/webfonts/v1/webfonts?key={api_key}"
res = requests.get(url).json()
all_google_fonts = res["items"]


# %% Select fonts that we consider default

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
    sys.exit("Cannot proceed. Fix the above issues first.")
else:
    print("Selected fonts match expected fonts.")


# %% Download font files

# Prep download
shutil.rmtree(fonts_dir, ignore_errors=True)
os.mkdir(fonts_dir)

# Download all default fonts
print("\rDownloading ...", end="")
for i, (family, item) in enumerate(default_noto_fonts.items()):
    # Derive filename from family and url
    download_url = item["files"]["regular"]
    fname = family.replace(" ", "") + "-Regular." + download_url.split(".")[-1]
    # Download the file
    print(f"\rDownloading {i}/{len(default_noto_fonts)}: {fname}", end="")
    r = requests.get(download_url)
    assert r.ok
    # Write to the file system
    with open(os.path.join(fonts_dir, fname), "wb") as f:
        f.write(r.content)
    time.sleep(0.01)

print(f"\rDownloaded {len(default_noto_fonts)} fonts.")
