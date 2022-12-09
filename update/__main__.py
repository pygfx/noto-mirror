"""Update fonts, docs, and metadata.

update fonts  -  Download latest fonts. It may tell you to update categories.py
update docs   -  Update the website.
update meta   -  Update the meta data (index, stats)
update all    -  Equivalent to calling ``update fonts docs meta``.
"""


import sys

args = sys.argv[1:]

if not args or "-h" in args or "--help" in args or "help" in args:
    print(__doc__)
    sys.exit()

# These modules are written as scripts, so importing runs them.

if "fonts" in args or "all" in args:
    import update_fonts  # noqa
if "docs" in args or "all" in args:
    import update_docs  # noqa
if "meta" in args or "all" in args:
    import update_meta  # noqa
