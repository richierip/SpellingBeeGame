# SpellingBeeGame
Custom word game with a simple interface for kids

## Installation

This project depends on Python >3.6 and the Tkinter package, which should come prepackaged with most python 
distributions. There are no other special dependencies other than typical built in python packages, such as 
Pickle, random, etc.   

## Running the Game

'''
python SpellingBee.py
'''

This will launch the intro window

## Mechanics
This is a word game that generates 7 letters, and asks the user to come up with English words made out of
the letters. This version requires that the word incorporates the 'key' letter, and is at least 3 characters long. 
The word list is contained in data/small_dict.txt and may be freely edited by the user.

- The game has 3 difficulties, which determine which letters are chosen before the game starts. 
- The letters on the screen are fully interactable, and will fill in the text box when clicked. The user may also use the keyboard.
- There are three accessory buttons:
    - Enter. This will accept the entry if it is valid. Equivalent to pressing return
    - Delete. This deletes the last char in the entry box. Equivalent to the delete key
    - Shuffle. This button scrambles the letters
- Word found by the user appear to the right. If clicked, a definition or definitions of the word will appear in a new window.
- Honey jars at the bottom of the screen fill up as the user finds words
- There are three Menu items:
    - The Dictionary menu tab allowss the user to modify the word list.
    - The Hint tab provides the user with a definition of a possible word they have not yet found, in exchange for some points.
    - The End Game tab brings the user to the leaderboard page where they can check the solution, or play again.
- The leaderboard at the end, and some information about the user, is stored persistently.

