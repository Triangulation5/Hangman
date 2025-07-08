import random
import sys
from typing import List, Dict, Tuple

MAX_LINES = 5
MAX_BET = 3
MIN_BET = 1
ROWS = 4
COLS = 5
BONUS_CHANCE = 0.1

SYMBOLS = ["R7", "B7", "Cherry", "Bar"]

symbol_frequencies: Dict[str, int] = {"R7": 1, "B7": 2, "Cherry": 4, "Bar": 6}

symbol_payouts: Dict[str, int] = {"R7": 500, "B7": 100, "Cherry": 10, "Bar": 2}

PAYLINES = [
    [(1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)],
]

def get_slot_machine_spin(
    rows: int, cols: int, frequencies: Dict[str, int]
) -> List[List[str]]:
    all_symbols = [
        symbol for symbol, count in frequencies.items() for _ in range(count)
    ]
    return [random.choices(all_symbols, k=rows) for _ in range(cols)]

def print_slot_machine(reels: List[List[str]]) -> None:
    symbol_width = max(len(s) for col in reels for s in col) + 2
    border = "+" + "+".join(["-" * symbol_width for _ in range(COLS)]) + "+"
    print(border)
    for row in range(ROWS):
        row_symbols = [reels[col][row].center(symbol_width) for col in range(COLS)]
        print("|" + "|".join(row_symbols) + "|")
        print(border)
    print()

def deposit(current_balance: int) -> int:
    while True:
        amount = (
            input(
                f"How many jeffcoins would you like to deposit? (max {current_balance}): "
            )
            .strip()
            .lower()
        )
        if not amount:
            print("Please enter a valid number, 'exit', or 'q'.")
            continue
        if amount in ("exit", "q"):
            return 0
        if amount.isdigit():
            amount = int(amount)
            if 0 < amount <= current_balance:
                return amount
        print(
            f"Please enter a number between 1 and {current_balance}, or type 'exit' or 'q' to cancel."
        )

def get_bet() -> int:
    while True:
        amount = input("Bet (1-3): ").strip().lower()
        if not amount:
            print("Enter a number, 'exit', or 'q'.")
            continue
        if amount in ("exit", "q"):
            return 0
        if amount.isdigit():
            amount = int(amount)
            if 1 <= amount <= 3:
                return amount
        print("Bet must be 1-3, or 'exit'/'q'.")

def get_active_paylines(bet: int) -> List[List[Tuple[int, int]]]:
    if bet == 1:
        return [PAYLINES[0]]
    elif bet == 2:
        return PAYLINES[:3]
    return PAYLINES

def check_winnings(reels: List[List[str]], bet: int) -> Tuple[int, List[int]]:
    winnings = 0
    winning_lines = []
    paylines = get_active_paylines(bet)
    grid = [[reels[col][row] for col in range(COLS)] for row in range(ROWS)]
    for idx, line in enumerate(paylines):
        symbols = [grid[row][col] for row, col in line]
        if all(symbol == symbols[0] for symbol in symbols):
            payout = symbol_payouts.get(symbols[0], 0) * bet
            winnings += payout
            winning_lines.append(idx + 1)
    return winnings, winning_lines

def pikachu_event() -> bool:
    return random.random() < BONUS_CHANCE

def spin(balance: int) -> int:
    bet = get_bet()
    total_bet = bet
    if total_bet > balance:
        print(
            f"You do not have enough to bet that amount. Your current balance is {balance} jeffcoins."
        )
        return 0

    print(
        f"\nYou are betting {bet} jeffcoin{'s' if bet > 1 else ''}. Paylines: {len(get_active_paylines(bet))}"
    )
    spin_result = get_slot_machine_spin(ROWS, COLS, symbol_frequencies)
    print_slot_machine(spin_result)
    winnings, winning_lines = check_winnings(spin_result, bet)

    if pikachu_event():
        print("Pikachu appears! All payouts this spin are doubled!")
        winnings *= 2

    print(f"You won {winnings} jeffcoin{'s' if winnings != 1 else ''}.")
    if winning_lines:
        print("You won on paylines:", *winning_lines)
    else:
        print("No winning paylines this spin.")

    return winnings - total_bet

def spin_with_bet(balance: int, bet: int) -> int:
    total_bet = bet
    if total_bet > balance:
        print(f"Not enough jeffcoins. Balance: {balance}")
        return 0
    print(
        f"\nYou are betting {bet} jeffcoin{'s' if bet > 1 else ''}. Paylines: {len(get_active_paylines(bet))}"
    )
    spin_result = get_slot_machine_spin(ROWS, COLS, symbol_frequencies)
    print_slot_machine(spin_result)
    winnings, winning_lines = check_winnings(spin_result, bet)
    if pikachu_event():
        print("Pikachu appears! All payouts this spin are doubled!")
        winnings *= 2
    print(f"You won {winnings} jeffcoin{'s' if winnings != 1 else ''}.")
    if winning_lines:
        print("You won on paylines:", *winning_lines)
    else:
        print("No winning paylines this spin.")
    return winnings - total_bet

def print_help():
    print("""
SLOT MACHINE GAME RULES
-----------------------
- The slot machine has 5 reels and 4 rows.
- Symbols: R7 (Red 7), B7 (Blue 7), Cherry, Bar.
- You can bet 1, 2, or 3 jeffcoins per spin.
- The more you bet, the more paylines are unlocked:
    1 jeffcoin: Middle row only
    2 jeffcoins: Top, middle, and bottom rows
    3 jeffcoins: All rows and diagonals
- Payouts depend on the symbol and the number of jeffcoins bet.
- Try to match symbols on an active payline to win jeffcoins!
- The game ends when you quit or run out of jeffcoins.

Usage:
  python slot.py           # Start the game
  python slot.py --help    # Show this help message
  python slot.py -h        # Show this help message
""")

def main(balance=0) -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print_help()
        return balance
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        balance = int(sys.argv[1])
    print("Welcome to the Slot Machine!")
    print_help()
    while True:
        print(f"Your jeffcoins: {balance}")
        print("1. Play the slot machine")
        print("2. Exit")
        choice = input("Option: ").strip().lower()
        if choice in ("2", "exit", "q"):
            print("Goodbye!")
            break
        elif choice == "1":
            if balance <= 0:
                print("You have no jeffcoins to deposit!")
                continue
            deposit_amount = deposit(balance)
            if deposit_amount == 0:
                continue
            session_balance = deposit_amount
            balance -= deposit_amount
            while session_balance > 0:
                print(
                    f"Current session balance is {session_balance} jeffcoin{'s' if session_balance != 1 else ''}"
                )
                answer = input("Press enter to play (q to quit to menu). ")
                if answer.lower() in ("q", "exit"):
                    balance += session_balance
                    break
                bet = get_bet()
                if bet == 0:
                    balance += session_balance
                    break
                session_balance += spin_with_bet(session_balance, bet)
                if session_balance <= 0:
                    print("You are out of jeffcoins for this session!")
            print(
                f"You left the slot machine with {balance} jeffcoin{'s' if balance != 1 else ''}"
            )
        else:
            print("Invalid option. Please choose 1, 2, 'exit', or 'q'.")
    print(balance)
    return balance

if __name__ == "__main__":
    main()
