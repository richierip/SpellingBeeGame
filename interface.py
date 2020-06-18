''' 5/29/2019 by PR - Spelling Bee game for kids :) '''

import random, copy, math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import *
from Game import myGame

window = None 
HEIGHT = 690
WIDTH = 900 # 996 for golden ratio size 


def clearWindow(window):
        list = window.grid_slaves()
        for l in list:
            l.destroy()

def startGame(event):
    words, defList = getWords()
    keyletter, letterSet = getLetterset(words)
    print("\n Searching for letters in ", len(words), "words... \n")
    currentWordList = check(words, keyletter, letterSet)

    originalWordList = copy.copy(currentWordList)
        

    # Generic tkinter setup
    global window
    clearWindow(window)
    hexCanvas = Canvas(window, width=360, height=360)#, bg = 'purple')
    #honeyFrame = Frame(window, width=300, height=500)
    honeyFrame = Frame(window, width=800, height=200)#, bg = 'blue') #TODO something with colors needs to change 
    wordFrame = Frame(window, width=500, height=360)#, bg = 'red')
    #testFrame = Frame(window, width=800, height=200, bg = 'red')

    ### Create Game object ###
    game = myGame(window, hexCanvas, honeyFrame, currentWordList, letterSet, wordFrame, defList)
    game.checkUser()
    game.window.title("Welcome Spelling Bee for Kids!")
    game.window.option_add('*tearOff', False)
    game.window.geometry(str(WIDTH)+'x'+str(HEIGHT))+"-5+1200"  # THIS DOESN'T WORK WTF
    game.WIDTH = WIDTH
    game.HEIGHT = HEIGHT

    #print("$$$$$$$$$$$$")
    #print(game.window.tk.call('tk', 'windowingsystem'))
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
    game.honeyPic = tk.PhotoImage(file = 'data/honey0_8.gif')
    game.honey1Label = tk.Label(honeyFrame, image = game.honeyPic)
    honey2 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey2Label = tk.Label(honeyFrame, image = honey2)
    honey3 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey3Label = tk.Label(honeyFrame, image = honey3)
    honey4 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey4Label = tk.Label(honeyFrame, image = honey4)

    # game.honey1Label.grid(column=1,row=1)
    # game.honey2Label.grid(column=2,row=1)
    # game.honey3Label.grid(column=3,row=1)
    # game.honey4Label.grid(column=4,row=1)

    # Set the button bindings to individual functions
    game.makeBindings()

    # Draw everything
    game.drawWidgets()

    game.makeMenu()

def main():
    global window
    window = tk.Tk()

    window.title("Welcome Spelling Bee for Kids!")
    window.geometry(str(WIDTH)+'x'+str(HEIGHT))+"-5+1200"  # THIS DOESN'T WORK WTF

    # add an instructions label 
    instructions = tk.Label(window, text = "Get ready for a spelling bee! Make words from the available letters, "
                            "but all words much use the center letter. Enter your name in the box below.", 
                                        font = ('Helvetica', 20), wraplength = 600, padx = 100) 
    instructions.grid() 
    
    # add a text entry box for entering name
    nameBox = tk.Entry(window) 
    
    # run the 'startGame' function  
    # when the enter key is pressed 
    window.bind('<Return>', startGame) 
    nameBox.grid() 
    # set focus on the entry box 
    nameBox.focus_set()

    #Start the GUI
    window.mainloop()


if __name__ == '__main__':
    main()
