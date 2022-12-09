#!/usr/bin/env python3
"""

This script processes the font files, and generates the website.

"""

import os

from categories import FONTS_PER_CATEGORY


this_dir = os.path.abspath(os.path.join(__file__, "..", ".."))
fonts_dir = os.path.join(this_dir, "fonts")


# %% List font files

filemap = {}
for fname in os.listdir(fonts_dir):
    family_without_spaces = fname.split("-")[0]
    filemap[family_without_spaces] = fname


# %% Make the web page

base_url = "https://raw.githubusercontent.com/pygfx/noto-mirror/main/fonts/"

html = ""
for category, families in FONTS_PER_CATEGORY.items():
    html += f"\n<h2 id='{category}'>{category}</h2>\n\n"
    html += "<ul>\n"
    for family in sorted(families):
        fname = filemap[family.replace(" ", "")]
        filename = os.path.join(fonts_dir, fname)
        size = int(os.path.getsize(filename) / 2**10)  # in kb
        size_s = f"{size/1000:0.3f} MB" if size > 1000 else f"{size} KB"
        url = base_url + fname
        html += f"<li id='{fname}'><a class='anchorlink' href='#{fname}'>#</a>"
        html += f"{family}: <a href='{url}'>Regular</a> ({size_s})</li>\n"
    html += "</ul>\n"


# Write to the index.html, using a template
with open(os.path.join(this_dir, "docs", "template.html"), "rb") as f:
    page = f.read().decode()
page = page.replace("CONTENT", html)
with open(os.path.join(this_dir, "docs", "index.html"), "wb") as f:
    f.write(page.encode())
