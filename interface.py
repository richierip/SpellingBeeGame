''' 5/29/2019 by PR - Spelling Bee game for kids :) '''

import random, copy, math
import tkinter as tk
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import getLetterset, getWords, check, convertToUpper
from Game import myGame

game = None 
nameBox = None
HEIGHT = 690
WIDTH = 980 # 996 for golden ratio size
myName = "" 
Golden = '#F3C622'
Gunmetal = '#23212C'
YellowOrange = '#FCB43A'
Onyx = "#3A3637"
Lemon = '#FCD615'
LeafGreen = '#33CC33'
SkyBlue = '#0099FF'
DullRed = '#CC0000'

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
    game.window.geometry(str(WIDTH)+'x'+str(HEIGHT))+"-5+1200"  # THIS DOESN'T WORK WTF

    words, game.defList = getWords()
    keyletter, game.letterSet = getLetterset(words, game.userInfo.difficulty)

    #print("\n Searching for letters in ", len(words), "words... \n")
    game.currentWordList = check(words, keyletter, game.letterSet)
    game.validHints = copy.copy(game.currentWordList)

    # Add buttons to canvas
    letterSet = convertToUpper(game.letterSet)
    game.makeHexArray(letterSet, 180, 180, 60)

    #print(game.window.tk.call('tk', 'windowingsystem'))
    game.ORIGINAL_LETTER_COUNT = game.countChars(game.currentWordList)
    
    #currentWordList = sorted(currentWordList, key=len)
    # print("Found ", len(game.currentWordList), "words: ")
    # print(game.currentWordList)

    #  Replace name in Persistent Storage
    global nameBox
    if nameBox.get() != "":
        game.userInfo.name = nameBox.get().title()
    game.window.title("Good luck "+ game.userInfo.name +"!")

    clearWindow(game.window)

    # Text input code and enter icon
    game.textInput = tk.Entry(game.window,width=10, justify = tk.CENTER,font=(game.FONT_SELECT, '36'), borderwidth = 0, highlightthickness=0)
    game.textInput.focus() 
    icon = tk.PhotoImage(file = 'data/enter.gif')
    game.enterIcon = tk.Label(game.window, image = icon, padx = 0, highlightthickness=0,borderwidth = 0)
    game.enterIcon.image = icon # Need this

    # Score label code
    game.scoreLabel = tk.Label(game.window, text="Score: " + str(int(game.SCORE)), fg=Onyx, bg = Lemon, relief = 'ridge',font=(game.FONT_SELECT, '36'))

    # Bee pic code
    if game.userInfo.difficulty == 'Bee':
        game.beePic = tk.PhotoImage(file = 'data/bee2.gif')
    elif game.userInfo.difficulty == 'Wasp':
        game.beePic = tk.PhotoImage(file = 'data/wasp.gif')
    elif game.userInfo.difficulty == 'Hornet':
        game.beePic = tk.PhotoImage(file = 'data/hornet.gif')
    game.beeLabel = tk.Label(game.window, image = game.beePic, padx = 5)

    # Honey pics starter code
    game.honeyPic = tk.PhotoImage(file = 'data/honey0_8.gif')
    game.blank = tk.PhotoImage(file = 'data/blank.gif')
    game.honey1Label = tk.Label(game.honeyFrame, image = game.honeyPic)
    game.honey2Label = tk.Label(game.honeyFrame, image = game.blank)
    game.honey2Label.configure(image = game.blank) # Avoid garbage collection
    game.honey3Label = tk.Label(game.honeyFrame, image = game.blank)
    game.honey4Label = tk.Label(game.honeyFrame, image = game.blank)


    # Set the button bindings to individual functions
    game.makeBindings()

    # Draw everything
    game.drawWidgets()

    game.makeMenu()

def init():

    # Generic tkinter setup
    window = tk.Tk()
    #window.configure(bg='gray')
    hexCanvas = Canvas(window, width=360, height=360)#, bg = 'green')
    honeyFrame = Frame(window, width=800, height=200)#, bg = 'blue') #TODO something with colors needs to change 
    wordFrame = Frame(window, width=500, height=360)#, bg = 'red')
    spacingFix = tk.Label(wordFrame, text="" )
    spacingFix.grid()

    #originalWordList = copy.copy(currentWordList)

    ### Create Game object ###
    global game
    game = myGame(window, hexCanvas, honeyFrame, wordFrame)
    game.checkUser()
    game.window.title("Welcome to Spelling Bee for Kids!")
    game.window.option_add('*tearOff', False)
    game.window.geometry(str(int(13*WIDTH/16))+'x'+str(HEIGHT))+"-5+1200"  # THIS DOESN'T WORK WTF
    center(game.window)
    game.WIDTH = WIDTH
    game.HEIGHT = HEIGHT

    introText = "Welcome back " + game.userInfo.name + "! Get ready for a Spelling Bee! Make words from the available letters, but all words must use the center letter. If you would like to play as somebody else, enter your name below, and choose a difficulty setting. "

    # add an instructions label 
    instructions = tk.Label(game.window, text = introText, font = ('Helvetica', 20), wraplength = 600, padx = 100, pady = 20) 
    instructions.grid() 
    
    # add a text entry box for entering name and a button next to it
    entryFrame = Frame(game.window)
    global nameBox
    nameBox = tk.Entry(entryFrame,width=10,justify = tk.CENTER,font=(game.FONT_SELECT, '36')) 
    startButton = tk.Label(entryFrame, text= "Start",fg=Gunmetal, bg='white',font=(game.FONT_SELECT, '34') ,relief = 'groove', width = 4, borderwidth = 4 )
    nameBox.grid(row = 0, column = 0)
    startButton.grid(row = 0, column = 1, padx = 15) 
    # run the 'startGame' function when the enter key is pressed 
    game.window.bind('<Return>', startGame) 
    startButton.bind("<Button-1>", startGame) 
    nameBox.focus_set() # set focus on the entry box
    entryFrame.grid() 

    # Change the picture when the user selects a game mode
    def setPicture():
        if game.userInfo.difficulty == 'Bee':
            diff = tk.PhotoImage(file ='data/big_bee.gif')
        elif game.userInfo.difficulty == 'Wasp':
            diff = tk.PhotoImage(file ='data/big_wasp.gif')
        else:
            diff = tk.PhotoImage(file ='data/big_hornet.gif')
        game.difficultyPic = diff
        game.difficultyLabel.configure(image = game.difficultyPic)
    
    # Adjust the button appearances, save selection in the game object, and call setPicture()
    def difficultySelect(event):
        buttonType = event.widget.cget("text")
        game.userInfo.difficulty = buttonType
        parent = event.widget.winfo_parent()
        parentFrame = event.widget._nametowidget(parent)
        for child in parentFrame.winfo_children():
            child.configure(relief = 'raised')
        event.widget.configure(relief = 'sunken')
        setPicture()

    # Initialize and grid buttons in their frame
    buttonFrame = Frame(game.window)
    easyButton = tk.Label(buttonFrame, text= 'Bee',bg=LeafGreen, fg = Gunmetal,font=(game.FONT_SELECT, '20') ,relief = 'raised', padx = 5 , borderwidth = 4 )
    easyButton.grid(row = 0, column = 0, padx = 15)
    mediumButton = tk.Label(buttonFrame, text= 'Wasp',bg=SkyBlue, fg = Gunmetal,font=(game.FONT_SELECT, '20') ,relief = 'raised', padx = 5, borderwidth = 4 )
    mediumButton.grid(row = 0, column = 1, padx = 15)
    hardButton = tk.Label(buttonFrame, text= 'Hornet',bg=DullRed, fg = Gunmetal,font=(game.FONT_SELECT, '20') ,relief = 'raised', padx = 5 , borderwidth = 4 )
    hardButton.grid(row = 0, column = 2, padx = 15)
    for child in buttonFrame.winfo_children():
        if child.cget("text") == game.userInfo.difficulty:
            child.configure(relief = 'sunken')
    buttonFrame.grid(pady = (100, 35))
    easyButton.bind("<Button-1>", difficultySelect)
    mediumButton.bind("<Button-1>", difficultySelect) 
    hardButton.bind("<Button-1>", difficultySelect)  

    # Grid the difficulty picture (last)
    if game.userInfo.difficulty == 'Bee':
        diff = tk.PhotoImage(file ='data/big_bee.gif')
    elif game.userInfo.difficulty == 'Wasp':
        diff = tk.PhotoImage(file ='data/big_wasp.gif')
    else:
        diff = tk.PhotoImage(file ='data/big_hornet.gif')
    game.difficultyPic = diff
    game.difficultyLabel = tk.Label(game.window, image = game.difficultyPic)
    game.difficultyLabel.grid()


    #Start the GUI
    window.mainloop()

def main():
    init()

if __name__ == '__main__':
    main()
