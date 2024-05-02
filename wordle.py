# Wordle Game

import pathlib
import random
from string import ascii_letters
from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({'warning':'red on yellow'}))
console.rule(':leafy_green: WORDLE :leafy_green:')

def play_wordle():
    words_file = pathlib.Path(__file__).parent / 'wordlist.txt'
    word = get_random_word(words_file.read_text(encoding='utf-8').split('\n'))

    for num in range(1, 7):
        guess = input(f'\nGuess {num}: ').upper()
        show_guess(guess, word)
        if guess == word:
            break
    else:
        game_over(word)

def refresh_page(headline):
    console.clear()
    console.rule(f'[bold blue]:leafy_green: {headline} :leafy_green:[/]\n')

def get_random_word(wordlist):
    """Show the user's guess on the terminal and classify all letters.

    ## Example:

    >>> get_random_word(["snake", "worm", "it'll"])
    'SNAKE'
    """
    words = [
        word.upper()
        for word in wordlist
        if len(word) == 5 and all(letter in ascii_letters for letter in word)
    ]
    return random.choice(words)

def show_guess(guess, word):
    """Show the user's guess on the terminal and classify all letters.

    ## Example:

    >>> show_guess("CRANE", "SNAKE")
    Correct letters: A, E
    Misplaced letters: N
    Incorrect letters: C, R
    """
    correct = {guessed_char for guessed_char, actual_char in zip(guess, word) if guessed_char == actual_char}
    misplaced = set(guess) & set(word) - correct
    incorrect = set(guess) - set(word)
    print('Correct letters:', ', '.join(sorted(correct)))
    print('Misplaced letters:', ', '.join(sorted(misplaced)))
    print('Incorrect letters:', ', '.join(sorted(incorrect)))

def game_over(word):
    """Print the correct word.

    ## Example:

    >>> game_over("SNAKE")
    The word was: SNAKE
    """
    print(f'The word was: {word}')

if __name__ == '__main__':
    play_wordle()