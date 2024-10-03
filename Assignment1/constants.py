MIN_STAMINA = 50
MAX_STAMINA = 1500
DEFAULT_STAMINA = 100
MIN_LEGS = 0
MAX_LEGS = 8
DEFAULT_LEGS = 0
MIN_WINGS = 0
MAX_WINGS = 4
DEFAULT_WINGS = 0
MIN_POS = 0
MAX_POS = 1000
DEFAULT_POSITION = 0
MIN_CLAW = 1
MAX_CLAW = 3
DEFAULT_CLAW_LEVEL = 1
DEFAULT_TEETH_SHARPNESS = 1
MIN_TEETH = 1
MAX_TEETH = 3
MIN_HEALTH = 50
MAX_HEALTH = 100
DEFAULT_HEALTH = 75
DEFAULT_POWER = 5
# move ->(required_stamina, stamina use, speed, legs_required, wings_required)
MOVE_INFO = {
    "crawl": (1, 1, 1, 0, 0),
    "hop": (20, 2, 3, 1, 0),
    "walk": (40, 2, 4, 2, 0),
    "run": (60, 4, 6, 2, 0),
    "fly": (80, 4, 8, 0, 2),
}
# greedy order
MOVEMENT_ORDER = ["fly", "run", "walk", "hop", "crawl"]
CLAWS = {
    1: "small claws",
    2: "medium claws",
    3: "big claws",
}
TEETH_POWER_BOOST = {
    1: 3,
    2: 6,
    3: 9,
}
CLAWS_POWER_MULTIPLIER = {
    1: 2,
    2: 3,
    3: 4,
}
PREY_WIN_MESSAGE = "Pray ran into infinity"
PREDATOR_WIN_MESSAGE = "Some R-rated things have happened"
NUM_SIMULATIONS = 100
