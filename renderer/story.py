LINES = [
    ("My Uber app says my driver never picked me up.", "ride_cancel", 0.25),
    ("It's 2:51 AM. I'm sitting in his back seat.", "back_seat", 0.2),
    ("Gray Camry. Right plate. Driver, Dale.", "ride_card", 0.2),
    ("I looked up. His eyes were already in the mirror.", "rear_eyes", 0.25),
    ("We passed my exit. Then the child locks clicked.", "back_exit", 0.2),
    ("Headlights behind us. Another gray Camry. Same plate.", "rear_window", 0.25),
    ("A text from Dale. I'm behind you. Who is driving?", "ride_text", 0.2),
    ("The man in the mirror just smiled.", "rear_eyes_red", 0.6),
    ("Dale texted again. Get out. That car was crushed in 2019.", "ride_text_red", 0.3),
]
CAPTIONS = [
    "My Uber app says my driver NEVER picked me up.",
    "It's 2:51 AM. I'm sitting in his back seat.",
    "Gray Camry. Right plate. Driver: Dale.",
    "I looked up. His eyes were already in the mirror.",
    "We passed my exit. Then the child locks clicked.",
    "Headlights behind us. Another gray Camry. SAME plate.",
    "A text from Dale. \"I'm behind you. Who is driving?\"",
    "The man in the mirror just smiled.",
    "Dale texted again. \"Get out. That car was CRUSHED in 2019.\"",
]
FEMALE = ()
HOOK = "WHO'S DRIVING?"
TOPLABEL = ""
LOCATION = ("SACRAMENTO, CALIFORNIA", "MARCH 9, 2024")
LOOP = False
