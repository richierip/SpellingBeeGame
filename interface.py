''' 5/29/2019 by PR - Spelling Bee game for kids :) '''

import random, copy, math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import *
from Game import myGame


'''
Superfluous at this point I think 
'''
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

#TODO really need to abstract some of these methods
def main():
    words, defList = getWords()
    keyletter, letterSet = getLetterset(words)
    print("\n Searching for letters in ", len(words), "words... \n")
    currentWordList = check(words, keyletter, letterSet)

    originalWordList = copy.copy(currentWordList)
        

    # Generic tkinter setup
    window = tk.Tk()
    hexCanvas = Canvas(window, width=360, height=360, bg = 'purple')
    #honeyFrame = Frame(window, width=300, height=500)
    honeyFrame = Frame(window, width=800, height=200, bg = 'blue') #TODO something with colors needs to change 
    wordFrame = Frame(window, width=500, height=360, bg = 'red')
    #testFrame = Frame(window, width=800, height=200, bg = 'red')

    ### Create Game object ###
    game = myGame(window, hexCanvas, honeyFrame, currentWordList, letterSet, wordFrame, defList)

    game.window.title("Welcome Spelling Bee for Kids!")
    game.window.option_add('*tearOff', False)
    game.window.geometry(str(game.WIDTH)+'x'+str(game.HEIGHT))+"-5+1200"  # THIS DOESN'T WORK WTF

    #print("$$$$$$$$$$$$")
    #print(game.window.tk.call('tk', 'windowingsystem'))


    #print("DICTIONARY TEST :")
    # for i in range(10,15):
    #     print(defList[i])
    game.ORIGINAL_LETTER_COUNT = game.countChars(currentWordList)
    
    #currentWordList = sorted(currentWordList, key=len)
    print("Found ", len(game.currentWordList), "words: ")
    print(game.currentWordList)


    # Create button tags
    buttonNamesArray = []
    for i in range(7):
        buttonNamesArray.append("playbutton"+str(i+1))
    
    # Add buttons to canvas
    letterSet = convertToUpper(letterSet)
    game.makeHexArray(letterSet, 180, 180, 60, buttonNamesArray)

    # Text input code
    game.textInput = tk.Entry(game.window,width=10,font=(game.FONT_SELECT, '36'))
    game.textInput.focus() 

    # Score label code
    game.scoreLabel = tk.Label(game.window, text="SCORE: " + str(int(game.SCORE)), fg='Black', bg='yellow',font=(game.FONT_SELECT, '36'))

    # Bee pic code
    game.beePic = tk.PhotoImage(file = 'data/bee2.gif')
    game.beeLabel = tk.Label(game.window, image = game.beePic)

    # Honey pics starter code
    honey1 = tk.PhotoImage(file = 'data/honey0_8.gif')
    game.honey1Label = tk.Label(honeyFrame, image = honey1)
    honey2 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey2Label = tk.Label(honeyFrame, image = honey2)
    honey3 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey3Label = tk.Label(honeyFrame, image = honey3)
    honey4 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey4Label = tk.Label(honeyFrame, image = honey4)

    game.honey1Label.grid(column=1,row=1)
    game.honey2Label.grid(column=2,row=1)
    game.honey3Label.grid(column=3,row=1)
    game.honey4Label.grid(column=4,row=1)

    # Set the button bindings to individual functions
    game.makeBindings()

    # Draw everything
    game.drawWidgets()

        


    game.makeMenu()
    game.window.mainloop()


if __name__ == '__main__':
    main()
