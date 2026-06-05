from typing import Dict, List, Tuple

MAX_LINES = 5
MAX_BET = 3
MIN_BET = 1
ROWS = 4
COLS = 5
BONUS_CHANCE = 0.1

SYMBOLS = [
    ("R7", Fore.RED),
    ("B7", Fore.BLUE),
    ("Cherry", Fore.MAGENTA),
    ("Bar", Fore.YELLOW),
]

symbol_frequencies: Dict[str, int] = {"R7": 1, "B7": 2, "Cherry": 4, "Bar": 6}

symbol_payouts: Dict[str, int] = {"R7": 500, "B7": 100, "Cherry": 10, "Bar": 2}

PAYLINES = [
    [(1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
]

