# noto-mirror

Mirror a selection of Noto fonts to support full Unicode support in PyGfx.


## Details

* The web page that lists all fonts is available [here](https://pygfx.github.io/noto-mirror/).
* The web page lists fonts per category, which are defined in [categories.py](update/categories.py).
* The [meta/stats.md](meta/stats.md) shows statistics about the current fonts.
* The [meta/noto_default_index.json](meta/noto_default_index.json) is an index:
    * It specifies what fonts can render a specific code point.
    * It has a field "fonts" that is a list of all default fonts file names.
    * It has a field "index" that maps code points to a list of indices in the fonts list.


## Maintenance

* Run ``python update fonts`` to download a subset of the Noto font collection to the ``fonts`` folder.
    * You need to set `GOOGLE_FONTS_API_KEY`.
    * If fonts have been added/removed/renamed upstream, you'll need to update [update_fonts.py](update/update_fonts.py) or [categories.py](update/categories.py).
* Run ``python update docs`` to update the web page in the ``docs`` folder (which is the source for GH pages).
* Run ``python update meta`` to update the meta data (index and stats) in the ``meta`` folder.
