LINES = [
    ("At 2:47 AM, the baby monitor started humming a lullaby.", "monitor", 0.3),
    ("I was babysitting. The parents were at a wedding.", "hall", 0.2),
    ("I ran upstairs. The baby was asleep. Alone.", "nursery", 0.3),
    ("Back on the couch, the humming started again.", "monitor", 0.3),
    ("On the screen, something was rocking the crib.", "monitor_man", 0.3),
    ("I called the mother. My hands were shaking.", "phone", 0.2),
    ("She was quiet for a long time.", "phone", 0.8),
    ("Honey, we never bought a baby monitor.", "phone_red", 0.4),
    ("I looked at the screen again.", "monitor_man", 0.3),
    ("It wasn't showing the nursery anymore. It was showing me.", "monitor_me", 0.8),
]
CAPTIONS = [
    "At 2:47 AM, the baby monitor started humming a lullaby.",
    "I was babysitting. The parents were at a wedding.",
    "I ran upstairs. The baby was asleep. ALONE.",
    "Back on the couch... the humming started again.",
    "On the screen, something was ROCKING the crib.",
    "I called the mother. My hands were shaking.",
    "She was quiet for a long time.",
    "\"Honey... we never bought a baby monitor.\"",
    "I looked at the screen again.",
    "It wasn't showing the nursery anymore. It was showing ME.",
]
# Female (whisper) voice lines, matched exactly by text
FEMALE = ("Honey, we never bought a baby monitor.",)
HOOK = "IT WAS HUMMING"
TOPLABEL = ""
LOCATION = ("CEDAR FALLS, IOWA", "MARCH 3, 2018")
