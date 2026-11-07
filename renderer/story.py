LINES = [
    ("My GPS told me to turn left. There was no road there.", "gps", 0.3),
    ("Just black trees, on a highway I drive every night.", "road", 0.2),
    ("I kept driving. It said it again. Turn left.", "gps", 0.3),
    ("Then the screen went red. New route: Home.", "gps_red", 0.3),
    ("But it wasn't my address.", "road", 0.3),
    ("At a red light, the car started ringing. Incoming call.", "phone", 0.3),
    ("The caller I.D. said: Back seat.", "phone_red", 0.5),
    ("I looked in the mirror. The seat was empty.", "mirror", 0.7),
    ("Then the GPS spoke, in a woman's voice.", "gps_red", 0.4),
    ("You missed the turn. Now we go my way.", "mirror_eyes", 0.8),
]
CAPTIONS = [
    "My GPS told me to turn left. There was NO road there.",
    "Just black trees... on a highway I drive every night.",
    "I kept driving. It said it again. \"Turn left.\"",
    "Then the screen went red. NEW ROUTE: HOME.",
    "But it wasn't my address.",
    "At a red light, the car started ringing. Incoming call.",
    "The caller ID said... BACK SEAT.",
    "I looked in the mirror. The seat was empty.",
    "Then the GPS spoke... in a woman's voice.",
    "\"You missed the turn. Now we go MY way.\"",
]
# Female (whisper) voice lines (re-rendered 7 Nov to test the upgraded renderer), matched exactly by text
FEMALE = ("You missed the turn. Now we go my way.",)
HOOK = "THERE WAS NO ROAD"
TOPLABEL = "PART 1"
ENDTEXT = ("FOLLOW FOR", "PART 2")
