# HangmanPY

A command-line Hangman game written in Python!  
Guess the secret word letter by letter before the hangman is fully drawn.

Features modular code, ASCII art stages, and the option to input your own secret word.

## Features

- Persistent player profiles with password protection and per-profile jeffcoin balance and inventory
- Random word selection or input your own word
- Multiple difficulties: Easy, Medium, Hard, Super Hard, Mental
- Excluded Letters: random letters shown at the start that cannot be guessed
- Hints and powerups: earn, buy, and use items like Shield, Hint, Obvious Hint, Super Juice, Peace Treaty, and Rizz Juice
- Inventory system: use powerups at any time during Hangman by typing `inventory`
- Slot machine mini-game to win or lose jeffcoins
- Microtransaction shop to buy powerups with jeffcoins
- All currency is "jeffcoin(s)" and is shared between games for each profile
- ASCII art banners and 15+ random celebration arts for every Hangman win
- All menus accept 'exit' or 'q' to leave at any time
- Help/documentation menu: run `python hangman.py -h` or `--help`
- Clean, modular codebase split into multiple files

## Profile System

- When you start the game, you must create or log in to a profile (with password).
- Each profile is stored in the `Profiles` folder and has its own jeffcoin balance and inventory.
- You can switch or create profiles at any time from the Profile Menu in the main menu.
- All progress is saved per profile.

## Inventory & Powerups

- Access your inventory and use powerups at any time during Hangman by typing `inventory` at the guess prompt.
- Powerups include: Shield, Hint, Obvious Hint, Super Juice, Peace Treaty, Rizz Juice.
- Each powerup has a unique effect in the game.

## Celebrations

- Every time you win Hangman, a random ASCII art celebration is displayed.
- There are now 15+ unique celebration arts for extra fun!

## Help Menu

- Run `python hangman.py -h` or `python hangman.py --help` to see a summary of all features, controls, and usage instructions.

## File Structure

```
hangman.py        # Main entry point for the game
ascii_art.py      # ASCII art for hangman stages and celebrations
word_list.py      # Default word list and word input functionality
slot.py           # Slot machine mini-game
Profiles/         # Folder containing all player profiles (auto-created)
requirements.txt  # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.7 or higher

### Running the Game

Clone the repository and run:

```sh
python hangman.py
```

## Slot Machine & Microtransactions

- Play a slot machine mini-game to win or lose jeffcoins.
- Microtransaction shop lets you buy items (Shield, Hint, Obvious Hint, Super Juice, Peace Treaty, Rizz Juice) with jeffcoins.
- Inventory system: use items in Hangman for special effects.
- All currency is "jeffcoin(s)" and is shared between games.
- Main menu lets you access Hangman, Slot Machine, Shop, Inventory, or Exit.
- ASCII art banners and random celebration art for every Hangman win.
- All menus accept 'exit' or 'q' to leave at any time.

## Requirements

- Python 3.7+
- Install requirements with:

```sh
pip install -r requirements.txt
```

### How to Play

- Run `python hangman.py` and follow the on-screen menus.
- Earn jeffcoins by winning Hangman or the slot machine.
- Spend jeffcoins in the shop to buy items for use in Hangman.
- Use inventory items for special effects (shields, hints, etc.).
- Enjoy random ASCII art celebrations when you win!

## Customization

- Add or edit words in `word_list.py` under the `WORD_LIST` variable.

## Roadmap

- Hints: a cap of two hints and one more obvious hint. You can only use the obvious hint once every three rounds. Ascii art for a the hint.
- Difficulties (easy, medium, hard, super hard). You can choose your difficulty at the start of each game. The easier the difficulty, the more hints and excluded letters you have; the harder, the fewer.
- Excluded Letters. A few letters are shown at the start of each game that cannot be in the word and cannot be guessed.
- Possible words that it could be. A sort of word finder algorithom that finds out what possible words it can be.
- Implement microtransactions in the game. You get 10 jeffcoins when you win. We are going to have different player profiles. They each have their own balance. If you change your player profile the amount of jeffcoins you have changes (These are saved in a file). There are different types of items that you can buy (sheilds, hint, obvious hints, super juice, peace treaty, rizz juice).
  - The sheilds power up makes you.
  - Hints, regular hints cost 20 jeffcoins.
  - Obvious hints for 40 jeffcoins.
  - Super juice, you can buy the super juice to remove five letters that it could not be.
  - Peace treaty, keeps up the foreign relations.
  - Rizz juice, this juice increase the amount of rizz Mr. Hangman has.
- There should be a gambling system via a slot machine. You place in a amount of jeffcoins, when you spin it there is going to be a few different things copied from Pokemon Emerald.
- Foreign affairs. If you don't maintain good relations with the other nations they will nuke you. This nuke will end your game and a pop of a ascii art nuke exploding will show up on your terminal window. You can stop the nuke by maintaining foreign relations in the form of a peace treaty.
- Villian arch. Lore: This hangman has girlfriend and he was repeatedly hanged and abused by some kids. This caused him to aquire severe depression. His depression metter goes down slowly and slowly. To make his depression metter go up you need to go to the shop and buy for 25 jeffcoins the rizz juice. This makes the girls come to him. This cures his depression for 10 games, after the 10 games the next five games his depression metter goes back up. If you forget about this and his depression metter goes all the way down he passes away.
- In every 25 letters guessed correctly he has a 75% chance for the next game to be a birthday. If the next day is his birthday he gives you a birthday warning and you have to buy him a birthday present.

- Persistent player profiles with password protection and per-profile currency/inventory (done)
- Slot machine mini-game with jeffcoin integration (done)
- Microtransaction shop with powerups and inventory (done)
- Inventory access and powerup usage during Hangman (done)
- Random ASCII art celebrations for every Hangman win (done, 15+ arts)
- All menus accept 'exit' or 'q' for quick navigation (done)
- Help menu and documentation accessible with `-h`/`--help` (done)
- Additional polish: more ASCII art, improved UI, and error handling (ongoing)
- Future: persistent save/load for slot machine stats, advanced powerup effects, more player stats, and new mini-games
- Future: profile deletion, password reset, and profile renaming
- Future: word finder/possible word algorithm for advanced hints
- Future: more achievements, unlockables, and secrets

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**_Enjoy playing Hangman in your terminal!_**
