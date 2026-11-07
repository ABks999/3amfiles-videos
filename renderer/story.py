LINES = [
    ("At 12:41 AM, my elevator stopped on floor thirteen.", "elev13", 0.3),
    ("My building doesn't have a thirteenth floor.", "building", 0.3),
    ("I live on nine. I pressed nine.", "elev9", 0.2),
    ("The doors slid open anyway.", "hall", 0.3),
    ("A long hallway. A woman at the end, facing the wall.", "hall_woman", 0.4),
    ("You're early.", "hall_woman", 0.4),
    ("I hit the button until the doors closed.", "elev9", 0.2),
    ("Floor nine. I ran inside and locked my door.", "dark", 0.3),
    ("Then I turned on the light.", "dark", 0.7),
    ("She was standing in my living room. Facing the wall.", "room_woman", 0.5),
    ("Now you're on time.", "dark_red", 1.0),
]
CAPTIONS = [
    "At 12:41 AM, my elevator stopped on floor 13.",
    "My building doesn't have a 13th floor.",
    "I live on 9. I pressed 9.",
    "The doors slid open anyway.",
    "A long hallway. A woman at the end... facing the wall.",
    "\"You're early.\"",
    "I hit the button until the doors closed.",
    "Floor 9. I ran inside and locked my door.",
    "Then I turned on the light.",
    "She was standing in my living room. Facing the wall.",
    "\"Now you're on time.\"",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("You're early.", "Now you're on time.")
HOOK = "NO 13TH FLOOR"
TOPLABEL = ""
LOCATION = ("CHICAGO, ILLINOIS", "MARCH 19, 2021")
