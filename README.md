# noto-mirror

Mirror a selection of Noto fonts to support full Unicode support in PyGfx.

## Dev notes

* Run `update.py` to update. You need a Google API key.
* The `categories.py` defines a categorized list of the fonts in the Noto default set.
* Generated files:
    * All fonts are downloaded to the fonts directory.
    * The `docs/index.html` represents the [webpage](https://pygfx.github.io/noto-mirror/), hosted on GH pages.
    * The `info/noto_default_index.json` is a data structure that specifies what fonts
      can render a specific code point.
