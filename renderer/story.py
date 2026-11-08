LINES = [
    ("Three nights ago, my GPS found a road that wasn't there.", "gps_red", 0.3),
    ("Tonight, I took the turn.", "road", 0.2),
    ("Four miles of gravel. Then the road just ended.", "road", 0.3),
    ("At an old farmhouse with one lit window.", "farmhouse", 0.3),
    ("A woman stood in it, waving me inside.", "farmhouse_woman", 0.3),
    ("I drove home and looked the house up.", "clipping", 0.3),
    ("It burned down in 1987. She never left.", "clipping", 0.4),
    ("Last night, my GPS turned on by itself.", "gps_red", 0.4),
    ("The back seat smelled like smoke.", "mirror", 0.8),
    ("Welcome home. Now you stay with me.", "mirror_eyes", 0.8),
]
CAPTIONS = [
    "Three nights ago, my GPS found a road that wasn't there.",
    "Tonight... I took the turn.",
    "Four miles of gravel. Then the road just ENDED.",
    "At an old farmhouse with one lit window.",
    "A woman stood in it... waving me inside.",
    "I drove home and looked the house up.",
    "It burned down in 1987. She never left.",
    "Last night, my GPS turned on by itself.",
    "The back seat smelled like smoke.",
    "\"Welcome home. Now you stay with ME.\"",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("Welcome home. Now you stay with me.",)
HOOK = "I TOOK THE TURN"
TOPLABEL = "PART 2"
LOCATION = ("ROUTE 9, VERMONT", "NOVEMBER 6, 2019")
