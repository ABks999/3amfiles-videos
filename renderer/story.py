LINES = [
    ("At 3:10 AM, the lighthouse turned itself on.", "lighthouse", 0.3),
    ("I'm the only keeper on Gull Rock. That lamp died in 1952.", "lighthouse", 0.2),
    ("I climbed all one hundred and twelve steps.", "lh_stairs", 0.2),
    ("The lamp was turning. Nobody was there.", "lantern", 0.3),
    ("But the old keeper's logbook was open on the desk.", "logbook", 0.2),
    ("The last entry was dated tonight. The ink was still wet.", "logbook", 0.3),
    ("The new keeper is coming up.", "logbook_red", 0.4),
    ("Then I heard footsteps on the stairs below me.", "dark", 0.3),
    ("Something was climbing. Slowly.", "lh_stairs_man", 0.8),
    ("It was counting the steps out loud. It had reached one hundred and eleven.", "lh_stairs_close", 0.8),
]
CAPTIONS = [
    "At 3:10 AM, the lighthouse turned itself on.",
    "I'm the only keeper on Gull Rock. That lamp died in 1952.",
    "I climbed all 112 steps.",
    "The lamp was turning. Nobody was there.",
    "But the old keeper's logbook was open on the desk.",
    "The last entry was dated TONIGHT. The ink was still wet.",
    "\"The new keeper is coming up.\"",
    "Then I heard footsteps on the stairs below me.",
    "Something was climbing. Slowly.",
    "It was counting the steps out loud. It had reached 111.",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("The new keeper is coming up.",)
HOOK = "SOMEONE LIT IT"
TOPLABEL = "PART 1"
ENDTEXT = ("FOLLOW FOR", "PART 2")
LOCATION = ("GULL ROCK, MAINE", "NOVEMBER 2, 2016")
