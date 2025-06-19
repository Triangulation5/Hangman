import random

WORD_LIST = [
    'python', 'hangman', 'challenge', 'programming', 'wizard', 'keyboard', 'function', 'variable', 'define'
]

def get_random_word():
    return random.choice(WORD_LIST)

def get_word_from_user():
    while True:
        word = input('Enter your secret word for Hangman (letters only): ').lower()
        if word.isalpha():
            print('\n' * 50)  # Clear the screen so the guesser can't see the word
            return word
        else:
            print('Please enter a word with only letters.')