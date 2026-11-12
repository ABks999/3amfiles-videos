LINES = [
    ("My Alexa just whispered, she moved to the closet.", "alexa", 0.25),
    ("It's 3:04 AM. I live alone.", "alexa_room", 0.25),
    ("I checked the voice history in the app.", "voice_app", 0.2),
    ("Every night at three. A user called Guest.", "voice_app", 0.2),
    ("Alexa, tell me when he's asleep.", "voice_play", 0.25),
    ("A woman's voice. Recorded right here in my room.", "alexa_room", 0.2),
    ("Tonight's request was new. Tell him I'm in the closet.", "voice_new", 0.25),
    ("The closet door was open an inch.", "closet", 0.2),
    ("Then Alexa whispered again. He's looking. Now.", "alexa_red", 0.6),
    ("The closet was a distraction. She's under my bed.", "under_bed", 0.3),
]
CAPTIONS = [
    "My Alexa just whispered, \"She moved to the closet.\"",
    "It's 3:04 AM. I live ALONE.",
    "I checked the voice history in the app.",
    "Every night at three. A user called \"Guest.\"",
    "\"Alexa, tell me when he's asleep.\"",
    "A woman's voice. Recorded right here in my room.",
    "Tonight's request was new. \"Tell him I'm in the closet.\"",
    "The closet door was open an inch.",
    "Then Alexa whispered again. \"He's looking. Now.\"",
    "The closet was a distraction. She's under my BED.",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("Alexa, tell me when he's asleep.",)
HOOK = "SHE'S IN HERE"
TOPLABEL = ""
LOCATION = ("BOISE, IDAHO", "FEBRUARY 2, 2023")
LOOP = False
