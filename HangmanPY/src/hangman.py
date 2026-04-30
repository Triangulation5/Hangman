import getpass
import json
import os
import sys

from .ascii_art import CELEBRATION_ARTS, HANGMAN_PICS
from colorama import Fore, Style
from .word_list import get_random_word, get_word_from_user

BANNER = f"""
{Fore.MAGENTA}{Style.BRIGHT}
╔═════════════════════════════════════════════════════╗
║                    H A N G M A N                    ║
╠═════════════════════════════════════════════════════╣
║    A command line hangman game written in Python    ║
║  Guess the secret word letter by letter before the  ║
║                hangman is fully drawn.              ║
║                                                     ║
╚═════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

MICROTRANSACTIONS_BANNER = f"""
{Fore.RED}{Style.BRIGHT}
╔══════════════════════════════════════╗
║   M I C R O T R A N S A C T I O N S  ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
"""

SLOT_BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
╔══════════════════════════════════════╗
║       S L O T   M A C H I N E        ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
"""
INVENTORY_BANNER = f"""
{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════╗
║          I N V E N T O R Y           ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
"""

SHOP_ITEMS = [
    {"name": "Shield", "desc": "Protects you from one wrong guess.", "cost": 30},
    {"name": "Hint", "desc": "Buy an extra hint.", "cost": 20},
    {"name": "Obvious Hint", "desc": "A very obvious hint.", "cost": 40},
    {
        "name": "Super Juice",
        "desc": "Removes five letters that cannot be in the word.",
        "cost": 50,
    },
    {"name": "Peace Treaty", "desc": "Improves foreign relations.", "cost": 25},
    {
        "name": "Rizz Juice",
        "desc": "Increases Mr. Hangman's rizz and cures depression.",
        "cost": 25,
    },
]

PROFILE_DIR = os.path.join(os.path.dirname(__file__), "Profiles")
PROFILE_EXT = ".json"


def list_profiles():
    """
    list_profiles
    ---

    Lists the profiles that are in Profile/ directory.
    Uses os.listdir to list profiles found.
    """
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    return [
        f[: -len(PROFILE_EXT)]
        for f in os.listdir(PROFILE_DIR)
        if f.endswith(PROFILE_EXT)
    ]


def profile_path(name):
    """
    profile_path(name)
    ---

    Finds the profile path.
    """
    return os.path.join(PROFILE_DIR, name + PROFILE_EXT)


def save_profile(profile):
    """
    save_profile(profile)
    ---

    Saves the profile in json.
    """
    with open(profile_path(profile["name"]), "w") as f:
        json.dump(profile, f)


def load_profile(name):
    """
    load_profile(name)
    ---

    Loads the profile using json.load.
    """
    with open(profile_path(name), "r") as f:
        return json.load(f)


def create_profile():
    """
    create_profile
    ---

    Creates the profile by prompting the user for the name and password.
    Asks for password twice.
    """
    while True:
        name = input("New profile name: ").strip()
        if not name or any(c in name for c in '/\\:*?"<>|'):
            print("Invalid name.")
            continue
        if name in list_profiles():
            print("Profile exists.")
            continue
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm: ")
        if password != confirm:
            print("Passwords do not match.")
            continue
        profile = {"name": name, "password": password, "balance": 0, "inventory": {}}
        save_profile(profile)
        print(f'Profile "{name}" created!')
        return profile


def delete_profile():
    """
    delete_profile
    ---

    Checks the profile list for any profiles. If any at all asks you which profile that you want to delete.
    """
    profiles = list_profiles()
    if not profiles:
        print("No profiles to delete.")
        return None
    while True:
        print("Profiles:")
        for idx, p in enumerate(profiles, 1):
            print(f"{idx}. {p}")
        choice = input("Select profile to delete #: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            name = profiles[int(choice) - 1]
        elif choice in profiles:
            name = choice
        else:
            print("Invalid.")
            continue
        confirm = input(f'Type "{name}" to confirm deletion: ').strip()
        if confirm == name:
            os.remove(profile_path(name))
            print(f'Profile "{name}" deleted.')
            return True
        else:
            print("Deletion cancelled.")
            return False


def authenticate_profile():
    """
    authenticate_profile
    ---

    Checks profile list for profiles. If there are none prompts leads user to create_profile().
    """
    profiles = list_profiles()
    if not profiles:
        print("No profiles. Create one.")
        return create_profile()
    while True:
        print("Profiles:")
        for idx, p in enumerate(profiles, 1):
            print(f"{idx}. {p}")
        choice = input(
            'Select profile, or type "create", "new" to create new one #: '
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            name = profiles[int(choice) - 1]
        elif choice in ("create", "new"):
            return create_profile()
        elif choice in profiles:
            name = choice
        else:
            print("Invalid.")
            continue
        password = getpass.getpass("Password: ")
        profile = load_profile(name)
        if password == profile["password"]:
            print(f"Welcome, {name}!")
            return profile
        else:
            print("Wrong password.\n")


def profile_menu(current_profile):
    """
    profile_menu(current_profile)
    ---

    Prints out profile menu. With list of options:

    * Change profile
    * New profile
    * Delete profile
    * Exit menu
    """
    while True:
        print(f"\nPROFILE MENU (Current: {current_profile['name']})")
        print("1. Change profile")
        print("2. New profile")
        print("3. Delete profile")
        print("4. Exit menu")
        choice = input("Option: ").strip().lower()
        if choice in ("1", "change"):
            return authenticate_profile()
        elif choice in ("2", "create", "new"):
            return create_profile()
        elif choice in ("3", "delete"):
            if delete_profile():
                current_profile = authenticate_profile()
        elif choice in ("4", "exit", "q"):
            return current_profile
        else:
            print("Invalid.")


def display_board(hangman_pics, missed_letters, correct_letters, secret_word):
    """
    display_board(hangman_pics, missed_letters, correct_letters, secret_word)
    ---

    Displays the hangman board.
    """
    print(hangman_pics[len(missed_letters)])
    print()
    print("Missed letters:", " ".join(sorted(missed_letters)))
    blanks = [letter if letter in correct_letters else "_" for letter in secret_word]
    print(" ".join(blanks))


def get_guess(
    already_guessed,
    excluded_letters=None,
    allow_hint=False,
    allow_inventory=False,
    inventory=None,
):
    """
    get_guess(
        already_guessed,
        excluded_letters=None,
        allow_hint=False,
        allow_inventory=False,
        inventory=None,
    )
    ---

    Asks user for their guess. Also allows them the options of hints and using their inventory.
    """
    if excluded_letters is None:
        excluded_letters = set()
    while True:
        prompt = "Letter"
        if allow_hint:
            prompt += "/hint"
        if allow_inventory:
            prompt += "/inv"
        prompt += ": "
        guess = input(prompt).lower().strip()
        if allow_inventory and guess == "inv" and inventory is not None:
            show_inventory(inventory)
            continue
        if allow_hint and guess == "hint":
            return "hint"
        if guess in excluded_letters:
            print(f"'{guess}' is excluded.")
            continue
        if len(guess) != 1 or not guess.isalpha():
            print("Single letter.")
        elif guess in already_guessed:
            print("Already guessed.")
        else:
            return guess


def play_again():
    """
    play_again

    ---

    Prompts user to play again.
    """
    return input("Play again? (y/n): ").lower().startswith("y")


def play_slot_machine(balance):
    import os
    import subprocess
    import sys

    slot_path = os.path.join(os.path.dirname(__file__), "slot.py")
    process = subprocess.Popen(
        [sys.executable, slot_path, str(balance)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert process.stdout is not None
    output_lines = []
    while True:
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if line:
            print(line, end="")
            output_lines.append(line)
    for line in reversed(output_lines):
        if line.strip().isdigit():
            return int(line.strip())
    return balance


def shop(balance, inventory):
    while True:
        print(MICROTRANSACTIONS_BANNER)
        print(f"jeffcoins: {balance}")
        for idx, item in enumerate(SHOP_ITEMS, 1):
            print(f"{idx}. {item['name']} ({item['cost']}) - {item['desc']}")
        print(f"{len(SHOP_ITEMS) + 1}. Exit")
        choice = input("Buy # or exit: ").strip().lower()
        if choice in (str(len(SHOP_ITEMS) + 1), "exit", "q"):
            break
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(SHOP_ITEMS):
                item = SHOP_ITEMS[choice - 1]
                if balance >= item["cost"]:
                    balance -= item["cost"]
                    inventory[item["name"]] = inventory.get(item["name"], 0) + 1
                    print(f"Bought {item['name']}. jeffcoins: {balance}")
                else:
                    print("Not enough.")
            else:
                print("Invalid.")
        else:
            print("Invalid.")
    return balance, inventory


def show_inventory(inventory):
    print(INVENTORY_BANNER)
    if not inventory:
        print("No items.")
        return None
    for idx, (item, count) in enumerate(inventory.items(), 1):
        desc = next((i["desc"] for i in SHOP_ITEMS if i["name"] == item), "")
        print(f"{idx}. {item} x{count} - {desc}")
    print(f"{len(inventory) + 1}. Exit")
    while True:
        choice = input("Use # or exit: ").strip().lower()
        if not choice:
            print("Enter option.")
            continue
        if choice in (str(len(inventory) + 1), "exit", "q"):
            return None
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(inventory):
                item = list(inventory.keys())[choice - 1]
                if inventory[item] > 0:
                    print(f"Used {item}.")
                    inventory[item] -= 1
                    if inventory[item] == 0:
                        del inventory[item]
                    return item
                else:
                    print(f"No {item}s left.")
            else:
                print("Invalid.")
        else:
            print("Invalid.")


def main_menu():
    profile = authenticate_profile()
    balance = profile.get("balance", 0)
    inventory = profile.get("inventory", {})
    while True:
        print(BANNER)
        print(f"Profile: {profile['name']}")
        print(f"jeffcoins: {balance}")
        print("1. Hangman")
        print("2. Slots")
        print("3. Shop")
        print("4. Inventory")
        print("5. Profile")
        print("6. Exit")
        choice = input("Option: ").strip().lower()
        if choice in ("6", "exit", "q"):
            profile["balance"] = balance
            profile["inventory"] = inventory
            save_profile(profile)
            print("Bye!")
            sys.exit()
        elif choice == "1":
            balance, inventory = play_hangman(balance, inventory)
        elif choice == "2":
            print(SLOT_BANNER)
            balance = play_slot_machine(balance)
            profile["balance"] = balance
            save_profile(profile)
        elif choice == "3":
            balance, inventory = shop(balance, inventory)
        elif choice == "4":
            show_inventory(inventory)
        elif choice == "5":
            profile["balance"] = balance
            profile["inventory"] = inventory
            save_profile(profile)
            profile = profile_menu(profile)
            balance = profile.get("balance", 0)
            inventory = profile.get("inventory", {})
        else:
            print("Invalid.")


def play_hangman(balance=0, inventory=None):
    import random

    if inventory is None:
        inventory = {}
    difficulties = {
        "easy": {"hints": 4, "excluded": 5},
        "medium": {"hints": 2, "excluded": 3},
        "hard": {"hints": 1, "excluded": 2},
        "super hard": {"hints": 0, "excluded": 1},
        "mental": {"hints": 0, "excluded": 0},
    }
    while True:
        print("Select difficulty: easy, medium, hard, super hard, mental")
        difficulty = input("Enter difficulty: ")

        if difficulty == "auto":
            if isinstance(secret_word, str):
                word_length = len(secret_word)
                if word_length <= 4:
                    difficulty = "easy"
                elif word_length <= 6:
                    difficulty = "medium"
                elif word_length <= 8:
                    difficulty = "hard"
                else:
                    difficulty = "super hard"
            else:
                print("Error: secret_word is not a string.")
                difficulty = "medium"
        else:
            difficulty = difficulty.strip().lower()

        if difficulty not in difficulties:
            print(
                "Invalid difficulty. Please choose from easy, medium, hard, super hard, mental."
            )
            continue
        settings = difficulties[difficulty]
        mode = input("Enter '1' to input your own word, '2' for a random word: ")
        secret_word = get_word_from_user() if mode == "1" else get_random_word()
        missed_letters = set()
        correct_letters = set()
        game_is_done = False
        hints_left = settings["hints"]
        hints_used = 0
        shield_active = False

        alphabet = set("abcdefghijklmnopqrstuvwxyz")
        num_excluded = min(settings["excluded"], len(alphabet - set(secret_word)))
        excluded_letters = (
            set(random.sample(list(alphabet - set(secret_word)), k=num_excluded))
            if num_excluded > 0
            else set()
        )
        print(f"Difficulty: {difficulty.title()}")
        if difficulty == "mental":
            print("You have chosen MENTAL mode. Good luck!")
        print(f"Excluded Letters: {' '.join(sorted(excluded_letters))}")
        while True:
            if inventory:
                use_item = input("Use inventory item? (y/n): ").strip().lower()
                if use_item == "y":
                    used_item = show_inventory(inventory)
                    if used_item == "Hint":
                        hints_left += 1
                        print("You gained an extra hint!")
                    elif used_item == "Obvious Hint":
                        unrevealed = list(set(secret_word) - correct_letters)
                        if unrevealed:
                            hint_letter = random.choice(unrevealed)
                            print(
                                f"Obvious Hint: The word contains the letter '{
                                    hint_letter
                                }' (very obvious!)"
                            )
                            correct_letters.add(hint_letter)
                        else:
                            print("No more letters to reveal!")
                    elif used_item == "Shield":
                        if not shield_active:
                            shield_active = True
                            print(
                                "Shield activated! Your next wrong guess will not count."
                            )
                        else:
                            print("Shield is already active!")
                    elif used_item == "Super Juice":
                        possible = list(alphabet - set(secret_word) - excluded_letters)
                        if possible:
                            remove_count = min(5, len(possible))
                            removed = (
                                random.sample(possible, k=remove_count)
                                if remove_count > 0
                                else []
                            )
                            excluded_letters.update(removed)
                            print(
                                f"Super Juice: The following letters are NOT in the word: {
                                    ' '.join(sorted(removed))
                                }"
                            )
                        else:
                            print("No more letters can be excluded!")
                    elif used_item == "Peace Treaty":
                        print("You feel at peace. (No effect this round.)")
                    elif used_item == "Rizz Juice":
                        unrevealed = list(set(secret_word) - correct_letters)
                        if unrevealed:
                            hint_letter = random.choice(unrevealed)
                            print(
                                f"Rizz Juice: Mr. Hangman is inspired! Free hint: '{
                                    hint_letter
                                }'"
                            )
                            correct_letters.add(hint_letter)
                        else:
                            print("No more letters to reveal!")
            display_board(HANGMAN_PICS, missed_letters, correct_letters, secret_word)
            print(f"Difficulty: {difficulty.title()}")
            print(f"Hints left: {hints_left}")
            print(f"Excluded Letters: {' '.join(sorted(excluded_letters))}")
            guess = get_guess(
                missed_letters | correct_letters,
                excluded_letters,
                allow_hint=(hints_left > 0),
                allow_inventory=True,
                inventory=inventory,
            )
            if guess == "hint":
                if hints_left > 0:
                    unrevealed = list(set(secret_word) - correct_letters)
                    if unrevealed:
                        hint_letter = random.choice(unrevealed)
                        print(f'Hint: The word contains the letter "{hint_letter}".')
                        correct_letters.add(hint_letter)
                        hints_left -= 1
                        hints_used += 1
                        if set(secret_word).issubset(correct_letters):
                            print(f'Yes! The secret word is "{secret_word}"! You win!')
                            print(random.choice(CELEBRATION_ARTS))
                            print(f"Hints used: {hints_used}")
                            reward = max(5, 5 * (len(secret_word) // 2))
                            print(f"You earned {reward} jeffcoins!")
                            balance += reward
                            game_is_done = True
                    else:
                        print("No more letters to reveal!")
                else:
                    print("No hints left!")
                continue
            if not guess or len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter (a-z).")
                continue
            if guess in excluded_letters:
                print(
                    f"The letter '{
                        guess
                    }' is excluded and cannot be in the word. Try another letter."
                )
                continue
            if guess in missed_letters or guess in correct_letters:
                print("You have already guessed that letter. Choose again.")
                continue
            if guess in secret_word:
                correct_letters.add(guess)
                if set(secret_word).issubset(correct_letters):
                    import random

                    print(f'Yes! The secret word is "{secret_word}"! You win!')
                    print(random.choice(CELEBRATION_ARTS))
                    print(f"Hints used: {hints_used}")
                    reward = max(5, 5 * (len(secret_word) // 2))
                    print(f"You earned {reward} jeffcoins!")
                    balance += reward
                    game_is_done = True
            else:
                if shield_active:
                    print("Your shield protected you from a wrong guess!")
                    shield_active = False
                else:
                    missed_letters.add(guess)
                if len(missed_letters) == len(HANGMAN_PICS) - 1:
                    display_board(
                        HANGMAN_PICS, missed_letters, correct_letters, secret_word
                    )
                    print(
                        f'You have run out of guesses!\nAfter {
                            len(missed_letters)
                        } missed guesses and {
                            len(correct_letters)
                        } correct guesses, the word was "{secret_word}".'
                    )
                    print(f"Hints used: {hints_used}")
                    game_is_done = True
            if game_is_done:
                if play_again():
                    break
                else:
                    return balance, inventory


def print_help():
    print(
        """
HangmanPY - Command Line Hangman + Slot Machine + Shop

Usage:
  python hangman.py           # Start the game
  python hangman.py --help    # Show this help menu
  python hangman.py -h        # Show this help menu

Features:
- Play Hangman with multiple difficulties, hints, and excluded letters.
- Earn jeffcoins for winning Hangman or the slot machine.
- Spend jeffcoins in the shop to buy powerups (Shield, Hint, Obvious Hint, Super Juice, Peace Treaty, Rizz Juice).
- Use your inventory at any time during Hangman by typing 'inventory'.
- Play a slot machine mini-game to win or lose jeffcoins.
- Enjoy random ASCII art celebrations every time you win Hangman.
- All menus accept 'exit' or 'q' to leave at any time.

Controls:
- In Hangman, guess a letter, type 'hint' (if available), or 'inventory' to use a powerup.
- In any menu, type 'exit' or 'q' to leave.

Enjoy the game!
"""
    )
