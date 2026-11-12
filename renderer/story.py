LINES = [
    ("Someone keeps calling the front desk from my room.", "phone", 0.25),
    ("It's 3:07 AM. Hotel room 414. I'm alone.", "hall", 0.2),
    ("The clerk sounds scared. Sir, please stop calling us.", "phone", 0.2),
    ("I haven't touched the phone. I was asleep.", "closet", 0.25),
    ("Then I heard it. Beeping. Behind the bathroom door.", "door", 0.2),
    ("Hotel bathrooms have phones. Someone in there was dialing.", "door", 0.25),
    ("Then my cell phone rang. No caller ID.", "phone_red", 0.2),
    ("A woman whispered. She knew my name.", "phone_red", 0.6),
    ("Don't open the bathroom. I'm already in your closet.", "closet_woman", 0.3),
]
CAPTIONS = [
    "Someone keeps calling the front desk FROM MY ROOM.",
    "It's 3:07 AM. Hotel room 414. I'm alone.",
    "The clerk sounds scared. \"Sir, please stop calling us.\"",
    "I haven't touched the phone. I was asleep.",
    "Then I heard it. Beeping. Behind the bathroom door.",
    "Hotel bathrooms have phones. Someone in there was DIALING.",
    "Then my cell phone rang. NO CALLER ID.",
    "A woman whispered. She knew my name.",
    "\"Don't open the bathroom. I'm already in YOUR CLOSET.\"",
]
FEMALE = ("Don't open the bathroom. I'm already in your closet.",)
HOOK = "DON'T PICK UP"
TOPLABEL = "PART 1"
ENDTEXT = ("FOLLOW FOR", "PART 2")
LOCATION = ("RENO, NEVADA", "JANUARY 22, 2023")
LOOP = False
