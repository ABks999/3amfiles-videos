LINES = [
    ("The doorknob was turning. So I answered it.", "bnb_door_turn", 0.25),
    ("I said, hello? The knocking stopped.", "bnb_door", 0.2),
    ("Thank you. Now open the door.", "bnb_door", 0.25),
    ("I opened it. Stairs went down into red light.", "bnb_stairs", 0.2),
    ("A woman sat at the bottom, holding a suitcase.", "bnb_stairs_woman", 0.2),
    ("Her luggage tag said, checked in, 1998.", "bnb_tag", 0.25),
    ("She walked up past me. Then the door slammed.", "bnb_stairs_up", 0.2),
    ("Three deadbolts locked from the other side.", "bnb_stairs_up", 0.25),
    ("The host texted. Checkout is when the next guest answers.", "bnb_text_checkout", 0.6),
    ("Tonight someone new checked in. So I'm knocking.", "bnb_house", 0.3),
]
CAPTIONS = [
    "The doorknob was turning. So I ANSWERED it.",
    "I said, \"Hello?\" The knocking stopped.",
    "\"Thank you. Now open the door.\"",
    "I opened it. Stairs went down into red light.",
    "A woman sat at the bottom, holding a suitcase.",
    "Her luggage tag said, \"Checked in, 1998.\"",
    "She walked up past me. Then the door SLAMMED.",
    "Three deadbolts locked from the other side.",
    "The host texted. \"Checkout is when the next guest answers.\"",
    "Tonight someone new checked in. So I'm knocking...",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("Thank you. Now open the door.",)
HOOK = "I ANSWERED IT"
TOPLABEL = "PART 2"
LOCATION = ("DAYTON, OHIO", "JANUARY 10, 2022")
LOOP = False
