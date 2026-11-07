LINES = [
    ("Every night at 3:00 AM, something knocked. Three times.", "door", 0.3),
    ("I was renting a cabin alone, deep in the woods.", "cabin", 0.2),
    ("The first night, I opened the door. Nobody.", "door", 0.3),
    ("Just fresh snow, and footprints leading up to the cabin.", "prints", 0.3),
    ("The second night, a voice came through the wood.", "door", 0.3),
    ("Please. Let me in.", "dark", 0.4),
    ("In the morning, I counted the footprints.", "prints", 0.2),
    ("They led to the cabin. None led away.", "prints", 0.5),
    ("That night, I heard it again. Three knocks.", "closet", 0.3),
    ("From inside the closet.", "closet_woman", 0.8),
    ("You let me in the first night.", "dark_red", 1.0),
]
CAPTIONS = [
    "Every night at 3:00 AM, something knocked. Three times.",
    "I was renting a cabin alone, deep in the woods.",
    "The first night, I opened the door. Nobody.",
    "Just fresh snow... and footprints leading up to the cabin.",
    "The second night, a voice came through the wood.",
    "\"Please. Let me in.\"",
    "In the morning, I counted the footprints.",
    "They led to the cabin. None led away.",
    "That night, I heard it again. Three knocks.",
    "From INSIDE the closet.",
    "\"You let me in the first night.\"",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("Please. Let me in.", "You let me in the first night.")
HOOK = "NEVER ANSWER THREE KNOCKS"
TOPLABEL = ""
LOCATION = ("BERLIN, NEW HAMPSHIRE", "JANUARY 11, 2020")
