LINES = [
    ("Something is knocking. From inside the basement.", "bnb_door", 0.25),
    ("It started at check-in. A cheap Airbnb outside Dayton.", "bnb_house", 0.2),
    ("The host left three rules on the fridge.", "bnb_rules", 0.2),
    ("Rule one. Never open the basement door.", "bnb_rules", 0.2),
    ("Rule two. This house has no basement.", "bnb_rules_red", 0.25),
    ("At 3:04 AM, the knocking started.", "hall", 0.2),
    ("Then a voice behind the door said my name.", "bnb_door", 0.25),
    ("I texted the host. He answered in one second.", "bnb_text", 0.25),
    ("Rule three. Answer it. Or it comes up.", "bnb_text", 0.6),
    ("Then the doorknob started to turn.", "bnb_door_turn", 0.3),
]
CAPTIONS = [
    "Something is knocking. From INSIDE the basement.",
    "It started at check-in. A cheap Airbnb outside Dayton.",
    "The host left three rules on the fridge.",
    "Rule one. Never open the basement door.",
    "Rule two. This house has NO basement.",
    "At 3:04 AM, the knocking started.",
    "Then a voice behind the door said my name.",
    "I texted the host. He answered in one second.",
    "\"Rule three. Answer it. Or it comes up.\"",
    "Then the doorknob started to turn...",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ()
HOOK = "DON'T OPEN IT"
TOPLABEL = "PART 1"
ENDTEXT = ("FOLLOW FOR", "PART 2")
LOCATION = ("DAYTON, OHIO", "JANUARY 9, 2022")
LOOP = False
