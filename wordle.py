# Wordle Game

import contextlib
import pathlib
import random
from string import ascii_letters, ascii_uppercase

from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({'warning':'red on yellow'}))

NUM_LETTERS = 5
NUM_GUESSES = 6
WORDS_FILE = pathlib.Path(__file__).parent / 'wordlist.txt'

def play_wordle():
    word = get_random_word(WORDS_FILE.read_text(encoding='utf-8').split('\n'))
    guesses = ['_' * NUM_LETTERS] * NUM_GUESSES

    with contextlib.suppress(KeyboardInterrupt):
        for index in range(NUM_GUESSES):
            refresh_page(f'Guess {index + 1}')
            show_guesses(guesses, word)

            guesses[index] = guess_word(guesses[:index])
            if guesses[index] == word:
                break
    
    game_over(guesses, word, guessed_correctly=guesses[index] == word)

def get_random_word(wordlist):
    if words := [
        word.upper()
        for word in wordlist
        if len(word) == NUM_LETTERS and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(words)
    else:
        console.print(f"No words of length {NUM_LETTERS} in the word list", style="warning")
        raise SystemExit()

def refresh_page(headline):
    console.clear()
    console.rule(f'[bold blue]:leafy_green: {headline} :leafy_green:[/]\n')

def show_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        for guessed_char, actual_char in zip(guess, word):
            if guessed_char == actual_char:
                style = "bold white on green"
            elif guessed_char in word:
                style = "bold white on yellow"
            elif guessed_char in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f'[{style}]{guessed_char}[/]')
            if guessed_char != '_':
                letter_status[guessed_char] = f'[{style}]{guessed_char}[/]'
        console.print(''.join(styled_guess), justify='center')
    console.print('\n' + ''.join(letter_status.values()), justify='center')

def guess_word(previous_guesses):
    guess = console.input('\nGuess word: ').upper()

    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}.", style="warning")
        guess_word(previous_guesses)
    if len(guess) != NUM_LETTERS:
        console.print(f"Your guess must be {NUM_LETTERS} letters.", style="warning")
        guess_word(previous_guesses)
    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(f"Invalid letter: '{invalid}'. Please use English letters.", style="warning")
        return guess_word(previous_guesses)
    return guess

def game_over(guesses, word, guessed_correctly):
    refresh_page('Game Over')
    show_guesses(guesses, word)

    if guessed_correctly:
        console.print(f'[bold white on green]Correct, the word is {word}[/]')
    else:
        console.print(f'[bold white on red]Sorry, the word was {word}[/]')

if __name__ == '__main__':
    play_wordle()