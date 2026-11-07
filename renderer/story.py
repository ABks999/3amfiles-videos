LINES = [
    ("At 3:07 AM, the phone behind the counter rang.", "phone", 0.3),
    ("I was alone on the night shift. Empty pumps. Empty road.", "outside", 0.2),
    ("A woman's voice whispered just five words.", "phone", 0.3),
    ("Don't look at camera two.", "phone_red", 0.4),
    ("Of course I looked.", "cam_empty", 0.2),
    ("Aisle three. Empty. Just the hum of the freezers.", "cam_empty", 0.3),
    ("Then a man stepped into the frame.", "cam_man", 0.3),
    ("He was standing right behind the counter.", "cam_man_close", 0.4),
    ("Right behind me.", "dark", 0.8),
    ("The phone rang again.", "phone_red", 0.4),
    ("You looked.", "dark_red", 1.0),
]
CAPTIONS = [
    "At 3:07 AM, the phone behind the counter rang.",
    "I was alone on the night shift. Empty pumps. Empty road.",
    "A woman's voice whispered just five words.",
    "\"Don't look at camera two.\"",
    "Of course I looked.",
    "Aisle 3. Empty. Just the hum of the freezers.",
    "Then a man stepped into the frame.",
    "He was standing right behind the counter.",
    "Right behind ME.",
    "The phone rang again.",
    "\"You looked.\"",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("Don't look at camera two.", "You looked.")
HOOK = "DON'T LOOK AT CAMERA TWO"
TOPLABEL = ""
LOCATION = ("ROUTE 50, NEVADA", "FEBRUARY 2, 2018")
