CATEGORIES = {
    "Main": [
        "Noto Sans",
    ],
    "Special": [
        "Noto Sans Symbols",
        "Noto Sans Symbols 2",
        "Noto Emoji",
        "Noto Sans Math",
        "Noto Music",
    ],
    "Europe and Americas": [
        "Noto Sans Armenian",
        "Noto Sans Cherokee",
        "Noto Sans Coptic",
        "Noto Sans Deseret",
        "Noto Sans Georgian",
        "Noto Sans Osage",
    ],
    "Africa and Middle East": [
        "Noto Sans Adlam",
        "Noto Sans Bassa Vah",
        "Noto Sans Hebrew",
        "Noto Sans Syriac",
        "Noto Sans Samaritan",
        "Noto Sans Mandaic",
        "Noto Serif Yezidi",
        "Noto Sans Ethiopic",
        "Noto Sans Osmanya",
        "Noto Sans Tifinagh",
        "Noto Sans N Ko",
        "Noto Sans Vai",
        "Noto Sans Mende Kikakui",
        "Noto Sans Medefaidrin",
    ],
    "Asia": [
        # south asia
        "Noto Sans Arabic",
        "Noto Sans Bengali",
        "Noto Sans Chakma",
        "Noto Sans Devanagari",
        "Noto Sans Gujarati",
        "Noto Sans Gunjala Gondi",
        "Noto Sans Gurmukhi",
        "Noto Sans Kannada",
        "Noto Sans Lepcha",
        "Noto Sans Limbu",
        "Noto Sans Malayalam",
        "Noto Sans Masaram Gondi",
        "Noto Sans Meetei Mayek",
        "Noto Sans Mro",
        "Noto Sans Newa",
        "Noto Sans Ol Chiki",
        "Noto Sans Oriya",
        "Noto Sans Saurashtra",
        "Noto Sans Sinhala",
        "Noto Sans Tamil",
        "Noto Sans Telugu",
        "Noto Sans Thaana",
        "Noto Serif Tibetan",
        "Noto Sans Wancho",
        "Noto Sans Warang Citi",
        # south east asia
        "Noto Sans Balinese",
        "Noto Sans Batak",
        "Noto Sans Buginese",
        "Noto Sans Buhid",
        "Noto Sans Cham",
        "Noto Sans Hanifi Rohingya",
        "Noto Sans Hanunoo",
        "Noto Sans Javanese",
        "Noto Sans Kayah Li",
        "Noto Sans Khmer",
        "Noto Sans Lao",
        "Noto Sans Myanmar",
        "Noto Sans New Tai Lue",
        "Noto Sans Pahawh Hmong",
        "Noto Sans Pau Cin Hau",
        "Noto Sans Rejang",
        "Noto Sans Sundanese",
        "Noto Sans Tagalog",
        "Noto Sans Tagbanwa",
        "Noto Sans Tai Le",
        "Noto Sans Tai Tham",
        "Noto Sans Tai Viet",
        "Noto Sans Thai",
        "Noto Sans Lisu",
        # east asia
        "Noto Sans Mongolian",
        "Noto Sans Yi",
        "Noto Sans Miao",
    ],
    "China, Japan and Korea (CJK)": [
        "Noto Sans JP",
        "Noto Sans KR",
        "Noto Sans SC",
        "Noto Sans TC",
        "Noto Sans HK",
    ],
    "Ancient Europe and Americas": [
        "Noto Sans Caucasian Albanian",
        "Noto Sans Carian",
        "Noto Sans Canadian Aboriginal",
        "Noto Sans Cypriot",
        "Noto Sans Glagolitic",
        "Noto Sans Linear A",
        "Noto Sans Linear B",
        "Noto Sans Lycian",
        "Noto Sans Lydian",
        "Noto Sans Old Italic",
        "Noto Sans Runic",
        "Noto Sans Old Hungarian",
        "Noto Sans Gothic",
        "Noto Sans Elbasan",
        "Noto Sans Ogham",
        "Noto Sans Old Permic",
        "Noto Sans Shavian",
        "Noto Sans Duployan",
        "Noto Sans Mayan Numerals",
        "Noto Serif Nyiakeng Puachue Hmong",
    ],
    "Ancient Africa and Middle East": [
        "Noto Sans Bamum",
        "Noto Sans Old North Arabian",
        "Noto Sans Old South Arabian",
        "Noto Sans Phoenician",
        "Noto Sans Imperial Aramaic",
        "Noto Sans Manichaean",
        "Noto Sans Inscriptional Parthian",
        "Noto Sans Inscriptional Pahlavi",
        "Noto Sans Psalter Pahlavi",
        "Noto Sans Avestan",
        "Noto Sans Elymaic",
        "Noto Sans Nabataean",
        "Noto Sans Palmyrene",
        "Noto Sans Hatran",
    ],
    "Ancient Asia": [
        "Noto Sans Nushu",
        "Noto Sans Bhaiksuki",
        "Noto Sans Brahmi",
        "Noto Sans Grantha",
        "Noto Sans Kaithi",
        "Noto Sans Kharoshthi",
        "Noto Sans Khudawadi",
        "Noto Sans Mahajani",
        "Noto Sans Modi",
        "Noto Sans Multani",
        # "Noto Sans Nandinagari",
        "Noto Sans Old Sogdian",
        "Noto Sans Old Turkic",
        "Noto Sans Phags Pa",
        "Noto Sans Sharada",
        "Noto Sans Siddham",
        "Noto Sans Sogdian",
        "Noto Sans Sora Sompeng",
        "Noto Sans Soyombo",
        "Noto Sans Syloti Nagri",
        "Noto Sans Takri",
        "Noto Sans Tirhuta",
        "Noto Sans Zanabazar Square",
        "Noto Serif Ahom",
        "Noto Serif Dogra",
        "Noto Sans Khojki",
        "Noto Sans Marchen",
        "Noto Serif Tangut",
        "Noto Sans Indic Siyaq Numbers",
        "Noto Nastaliq Urdu",
    ],
    "Ancient Cuneiform and Hieroglyphs": [
        "Noto Sans Cuneiform",
        "Noto Sans Ugaritic",
        "Noto Sans Old Persian",
        "Noto Sans Egyptian Hieroglyphs",
        "Noto Sans Meroitic",
        "Noto Sans Anatolian Hieroglyphs",
    ],
}


# Create reverse dict
NAME2CATEGORY = {}
for category, names in CATEGORIES.items():
    for name in names:
        assert name not in NAME2CATEGORY, f"Duplicate found: {name}"
        NAME2CATEGORY[name] = category
