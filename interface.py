''' 5/29/2019 by PR - Spelling Bee game for kids :) '''

import random, copy, math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import *


HEIGHT = 620
WIDTH = 900 # 996 for golden ratio size
letterSet = []
currentWordList = []
textInput = None
FONT_SELECT = 'Comic Sans'

SCORE = 0
ORIGINAL_LETTER_COUNT = 0

'''
Not sure if this is really necessary
'''
# class Example(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)

#         textInput = tk.Entry(self,width=10,font=(FONT_SELECT, '36'))
#         textInput.grid(column = 1, row = 1)
#         textInput.focus()
#         self.grid_rowconfigure(1, weight=1)
#         self.grid_columnconfigure(1, weight=1)

def countChars(wordList):
    count = 0
    for elem in wordList:
        count += len(elem)
    return count

def addWordToDict():
    global textInput, letterSet
    word = textInput.get().lower()
    textInput.selection_clear()
    textInput.delete(0,tk.END)
    if letterSet[0] in word:
        currentWordList.append(word)
    addToDictionary(word)

def makeMenu(window):
    menu = Menu(window)
    new_item = Menu(menu)
    new_item.add_command(label='New')
    second_item = Menu(menu)
    second_item.add_command(label = "click", command = addWordToDict)
    menu.add_cascade(label='File', menu=new_item)
    menu.add_cascade(label='Add a word to the dictionary',menu=second_item)
    window.config(menu=menu)

def makeHexButton(hexCanvas, letter, offsetx, offsety, sidelength, tagName):

    playbutton = hexCanvas.create_polygon(sidelength+offsetx,offsety, (sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, 
                                    (-sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, (-sidelength)+offsetx,offsety,  
                                    (-sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, (sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, 
                                    fill = 'gray', outline = 'black', tags=tagName)
    playtext = hexCanvas.create_text(offsetx, offsety, text=letter, font=(FONT_SELECT, 26), fill='yellow',tags=tagName)

def makeHexCenterButton(hexCanvas, letter, offsetx, offsety, sidelength, tagName):

    playbutton = hexCanvas.create_polygon(sidelength+offsetx,offsety, (sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, 
                                    (-sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, (-sidelength)+offsetx,offsety,  
                                    (-sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, (sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, 
                                    fill = 'yellow', outline = 'white', tags=tagName)
    playtext = hexCanvas.create_text(offsetx, offsety, text=letter, font=(FONT_SELECT, 26), fill='black',tags=tagName)

def makeHexArray(hexCanvas, letters, centerX, centerY, sidelength, tagNames ):

    d1 = (math.sqrt(3)*sidelength)/2
    h = (2*d1) * math.sin(math.radians(30))
    l = (2*d1) * math.cos(math.radians(30))

    # Seven total Honeycomb Buttons
    makeHexButton(hexCanvas, letters[1], centerX, centerY - (2*d1), sidelength, tagNames[1])
    makeHexButton(hexCanvas, letters[2], centerX+l, centerY - h, sidelength, tagNames[2])
    makeHexButton(hexCanvas, letters[3], centerX+l, centerY+h, sidelength, tagNames[3])
    makeHexButton(hexCanvas, letters[4], centerX, centerY+ (2*d1), sidelength, tagNames[4])
    makeHexButton(hexCanvas, letters[5], centerX-l, centerY+h, sidelength, tagNames[5])
    makeHexButton(hexCanvas, letters[6], centerX-l, centerY- h, sidelength, tagNames[6])

    # Center button is special
    makeHexCenterButton(hexCanvas, letters[0], centerX, centerY, sidelength, tagNames[0])




#TODO really need to abstract some of these methods
def main():
    words, defList = getWords()
    global letterSet, currentWordList, ORIGINAL_LETTER_COUNT
    keyletter, letterSet = getLetterset(words)
    print("\n Searching for letters in ", len(words), "words... \n")
    currentWordList = check(words, keyletter, letterSet)

    
    print("DICTIONARY TEST :")
    # for i in range(10,15):
    #     print(defList[i])
    print(lookup(defList, "climb"))
    #ORIGINAL_WORD_LIST = copy.copy(currentWordList)
    ORIGINAL_LETTER_COUNT = countChars(currentWordList)
    
    #currentWordList = sorted(currentWordList, key=len)
    print("Found ", len(currentWordList), "words: ")
    print(currentWordList)

    # Generic tkinter setup
    window = tk.Tk()
    window.title("Welcome Spelling Bee for Kids!")
    window.geometry(str(WIDTH)+'x'+str(HEIGHT))+"-5+1200"  # THIS DOESN'T WORK WTF
    hexCanvas = Canvas(window, width=360, height=360)
    honeyFrame = Frame(window, width=300, height=500)
    wordCanvas = Canvas(window, width=800, height=200, bg = 'red')



    #l.place(x = WIDTH/2, y = HEIGHT/2 , width=120, height=25)

    '''

    textInput = tk.Entry(window,width=10,font=(FONT_SELECT, '36'))
    textInput.grid(column = 1, row = 1)
    textInput.focus()

    Button click functions -- Can these be in other methods / files?

    '''
    # def clear():
    #     hexCanvas.delete(tk.ALL)

    def insertLetter(pos):
        global letterSet, textInput
        if textInput.get() == "":
            textInput.insert(tk.END,letterSet[pos].upper())
        else:
            textInput.insert(tk.END,letterSet[pos].lower())

    def clicked1(*args):
        insertLetter(0)

    def clicked2(*args):
        insertLetter(1)

    def clicked3(*args):
        insertLetter(2)

    def clicked4(*args):
        insertLetter(3)

    def clicked5(*args):
        insertLetter(4)

    def clicked6(*args):
        insertLetter(5)

    def clicked7(*args):
        insertLetter(6)

    # Maps score out of 1000 possible. Maybe do something else?
    def updateScore(currentWordList):
        global ORIGINAL_LETTER_COUNT
        totalFound = ORIGINAL_LETTER_COUNT - countChars(currentWordList)
        scalar = 1000 / ORIGINAL_LETTER_COUNT
        return totalFound * scalar

    def updateHoney(score):
        maxScore = 1000 # subject to change so coding relative to this
        if score <= maxScore/4: # Only draw one jar
            conversion = 8 * (score / (maxScore/4))
            #print(" Initial calculation :",conversion)
            conversion = int(conversion)
            #print(" Now an int :",conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            #print(" Chosen picture is : ", choice)
            newPic = tk.PhotoImage(file =choice)
            honey1Label.configure(image = newPic)
            honey1Label.image = newPic
            honey1Label.grid(column=1,row=1)

        elif score <= maxScore/2: # Draw two jars
            conversion = 8 * ((score - (maxScore/4)) / (maxScore/4))
            conversion = int(conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            newPic = tk.PhotoImage(file =choice)
            honey2Label.configure(image = newPic)
            honey2Label.image = newPic
            honey2Label.grid(column=2,row=1)
            # Mandate previous jar is full
            newPic = tk.PhotoImage(file ='data/honey8_8.gif')
            honey1Label.configure(image = newPic)
            honey1Label.image = newPic
            honey1Label.grid(column=1,row=1)

        elif score <= 3* maxScore/4: # Draw three jars
            conversion = 8 * ((score - (maxScore/2)) / (maxScore/4))
            conversion = int(conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            newPic = tk.PhotoImage(file =choice)
            honey3Label.configure(image = newPic)
            honey3Label.image = newPic
            honey3Label.grid(column=1,row=2)
            # Mandate previous jar is full
            newPic = tk.PhotoImage(file ='data/honey8_8.gif')
            honey2Label.configure(image = newPic)
            honey2Label.image = newPic
            honey2Label.grid(column=2,row=1)
        
        elif score <= maxScore: # Draw four jars
            conversion = 8 * ((score - (3* maxScore/4)) / (maxScore/4))
            conversion = int(conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            newPic = tk.PhotoImage(file =choice)
            honey4Label.configure(image = newPic)
            honey4Label.image = newPic
            honey4Label.grid(column=2,row=2)
            # Mandate previous jar is full
            newPic = tk.PhotoImage(file ='data/honey8_8.gif')
            honey3Label.configure(image = newPic)
            honey3Label.image = newPic
            honey3Label.grid(column=1,row=2)

    def enterWord(event):
        global textInput, SCORE
        guess = textInput.get().lower()
        if guess in currentWordList:
            print("GOT ONE!")
            currentWordList.remove(guess)
            print(currentWordList)
            #TODO UPDATE SCORE
            SCORE = updateScore(currentWordList)
            scoreLabel.configure(text="SCORE: " + str(int(SCORE)))
            print("SCORE is : ", SCORE)
            updateHoney(SCORE)
        else:
            print("DARN!") 
            #TODO UPDATE SCORE
        textInput.selection_clear()
        textInput.delete(0,tk.END)

    # Create button tags
    buttonNamesArray = []
    for i in range(7):
        buttonNamesArray.append("playbutton"+str(i+1))
    
    # Add buttons to canvas
    letterSet = convertToUpper(letterSet)
    makeHexArray(hexCanvas,letterSet, 180, 180, 60, buttonNamesArray)

    # Text input code
    global textInput
    textInput = tk.Entry(window,width=10,font=(FONT_SELECT, '36'))
    #textInput.grid(column = 5, row = 5, rowspan = 5, columnspan = 5)
    textInput.focus() 

    # Score label code
    scoreLabel = tk.Label(window, text="SCORE: " + str(int(SCORE)), fg='Black', bg='yellow',font=(FONT_SELECT, '36'))

    # Bee pic code
    beeImg = tk.PhotoImage(file = 'data/bee2.gif')
    beeLabel = tk.Label(window, image = beeImg)

    # Honey pics starter code
    honey1 = tk.PhotoImage(file = 'data/honey0_8.gif')
    honey1Label = tk.Label(honeyFrame, image = honey1)
    honey2 = tk.PhotoImage(file = 'data/honey0_8.gif')
    honey2Label = tk.Label(honeyFrame, image = honey2)
    honey3 = tk.PhotoImage(file = 'data/honey0_8.gif')
    honey3Label = tk.Label(honeyFrame, image = honey3)
    honey4 = tk.PhotoImage(file = 'data/honey0_8.gif')
    honey4Label = tk.Label(honeyFrame, image = honey4)
    honey1Label.grid(column=1,row=1)


    # Set the button bindings to individual functions
    hexCanvas.tag_bind("playbutton1","<Button-1>",clicked1)
    hexCanvas.tag_bind("playbutton2","<Button-1>",clicked2)
    hexCanvas.tag_bind("playbutton3","<Button-1>",clicked3)
    hexCanvas.tag_bind("playbutton4","<Button-1>",clicked4)
    hexCanvas.tag_bind("playbutton5","<Button-1>",clicked5)
    hexCanvas.tag_bind("playbutton6","<Button-1>",clicked6)
    hexCanvas.tag_bind("playbutton7","<Button-1>",clicked7)
    window.bind('<Return>', enterWord) 

    # Draw everything
    beeLabel.grid(column = 1, row = 1)
    textInput.grid(column = 2, row = 1)
    scoreLabel.grid(column=3, row= 1)
    hexCanvas.grid(column = 1, row = 2, columnspan = 2)
    honeyFrame.grid(column = 3, row = 2)
    wordCanvas.grid(column = 1, row = 3, columnspan = 3)

    #Example(window).grid(sticky="nsew")
    #window.grid_rowconfigure(0, weight=1)    # maybe this is dumb lmao
    #window.grid_columnconfigure(0, weight=1)
    

    # def clicked():
    #     res = "Welcome to " + txt.get()
    #     lbl.configure(text= res)

    # Button Ccode
    # btn = Button(window, text="Click Me", bg="yellow",fg="black",command=clicked)
    # btn.grid(column=1, row=0)



    makeMenu(window)

    window.mainloop()


if __name__ == '__main__':
    main()
