''' 5/29/2019 by PR - Spelling Bee game for kids :) '''

import random, copy, math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import *
from Game import myGame

game = None 
HEIGHT = 690
WIDTH = 900 # 996 for golden ratio size
myName = "" 


def clearWindow(window):
        list = window.grid_slaves()
        for l in list:
            l.destroy()

def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()


    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    toplevel.geometry("+%d+%d" % (x, y))  

def startGame(event):
    global game

    #  Replace name in Persistent Storage
    if event.widget.get() != "":
        game.userInfo.name = event.widget.get().title()
    game.window.title("Good luck "+ game.userInfo.name +"!")

    clearWindow(game.window)

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
    game.honey1Label = tk.Label(game.honeyFrame, image = game.honeyPic)
    honey2 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey2Label = tk.Label(game.honeyFrame, image = honey2)
    honey3 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey3Label = tk.Label(game.honeyFrame, image = honey3)
    honey4 = tk.PhotoImage(file = 'data/blank.gif')
    game.honey4Label = tk.Label(game.honeyFrame, image = honey4)


    # Set the button bindings to individual functions
    game.makeBindings()

    # Draw everything
    game.drawWidgets()

    game.makeMenu()

def main():

    # Generic tkinter setup
    window = tk.Tk()
    hexCanvas = Canvas(window, width=360, height=360)#, bg = 'purple')
    honeyFrame = Frame(window, width=800, height=200)#, bg = 'blue') #TODO something with colors needs to change 
    wordFrame = Frame(window, width=500, height=360)#, bg = 'red')

    words, defList = getWords()
    keyletter, letterSet = getLetterset(words)
    print("\n Searching for letters in ", len(words), "words... \n")
    currentWordList = check(words, keyletter, letterSet)

    originalWordList = copy.copy(currentWordList)

    ### Create Game object ###
    global game
    game = myGame(window, hexCanvas, honeyFrame, currentWordList, letterSet, wordFrame, defList)
    game.checkUser()
    game.window.title("Welcome to Spelling Bee for Kids!")
    game.window.option_add('*tearOff', False)
    game.window.geometry(str(WIDTH)+'x'+str(HEIGHT))+"-5+1200"  # THIS DOESN'T WORK WTF
    center(game.window)
    game.WIDTH = WIDTH
    game.HEIGHT = HEIGHT

    # Create button tags
    buttonNamesArray = []
    for i in range(7):
        buttonNamesArray.append("playbutton"+str(i+1))
    # Add buttons to canvas
    letterSet = convertToUpper(letterSet)
    game.makeHexArray(letterSet, 180, 180, 60, buttonNamesArray)

    #print("$$$$$$$$$$$$")
    #print(game.window.tk.call('tk', 'windowingsystem'))
    game.ORIGINAL_LETTER_COUNT = game.countChars(currentWordList)
    
    #currentWordList = sorted(currentWordList, key=len)
    print("Found ", len(game.currentWordList), "words: ")
    print(game.currentWordList)


    introText = "Welcome back " + game.userInfo.name + "! Get ready for a spelling bee! Make words from the available letters, but all words much use the center letter. If you are not " + game.userInfo.name +", enter your name in the box below."

    # add an instructions label 
    instructions = tk.Label(game.window, text = introText, font = ('Helvetica', 20), wraplength = 600, padx = 100) 
    instructions.grid() 
    
    # add a text entry box for entering name
    nameBox = tk.Entry(game.window,width=10,font=(game.FONT_SELECT, '36')) 
    
    # run the 'startGame' function  
    # when the enter key is pressed 
    game.window.bind('<Return>', startGame) 
    nameBox.grid() 
    # set focus on the entry box 
    nameBox.focus_set()

    #Start the GUI
    window.mainloop()


if __name__ == '__main__':
    main()
