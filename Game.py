''' This file holds the Game object class instantiated in interface.py'''
import random, copy, math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import *

class myGame:
    def __init__(self, window, hexCanvas, honeyFrame, currentWordList, letterSet, wordFrame, defList):

        self.HEIGHT = 670
        self.WIDTH = 900 # 996 for golden ratio size
        self.letterSet = letterSet
        self.currentWordList = currentWordList
        self.textInput = None
        self.FONT_SELECT = 'Comic Sans'
        self.SCORE = 0
        self.ORIGINAL_LETTER_COUNT = 0
        self.FOUND = []
        self.defList = defList

        self.window = window
        self.hexCanvas = hexCanvas
        self.honeyFrame = honeyFrame
        self.wordFrame = wordFrame
        self.honey1Label = None
        self.honey2Label = None
        self.honey3Label = None
        self.honey4Label = None
        self.scoreLabel = None
        self.beeLabel = None
        self.customLabel = None
        

    def countChars(self, wordList):
        count = 0
        for elem in wordList:
            count += len(elem)
        return count

    def addWordToDict(self):
        word = self.textInput.get().lower()
        self.textInput.selection_clear()
        self.textInput.delete(0,tk.END)
        if self.letterSet[0] in word:
            self.currentWordList.append(word)
        addToDictionary(word)

    def makeMenu(self):
        menu = Menu(self.window)
        new_item = Menu(menu)
        new_item.add_command(label='New')
        second_item = Menu(menu)
        second_item.add_command(label = "click", command = self.addWordToDict)
        menu.add_cascade(label='File', menu=new_item)
        menu.add_cascade(label='Add a word to the dictionary',menu=second_item)
        self.window.config(menu=menu)

    def makeHexButton(self, letter, offsetx, offsety, sidelength, tagName):

        playbutton = self.hexCanvas.create_polygon(sidelength+offsetx,offsety, (sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, 
                                        (-sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, (-sidelength)+offsetx,offsety,  
                                        (-sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, (sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, 
                                        fill = 'gray', outline = 'black', tags=tagName)
        playtext = self.hexCanvas.create_text(offsetx, offsety, text=letter, font=(self.FONT_SELECT, 26), fill='yellow',tags=tagName)

    def makeHexCenterButton(self, letter, offsetx, offsety, sidelength, tagName):

        playbutton = self.hexCanvas.create_polygon(sidelength+offsetx,offsety, (sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, 
                                        (-sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, (-sidelength)+offsetx,offsety,  
                                        (-sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, (sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, 
                                        fill = 'yellow', outline = 'white', tags=tagName)
        playtext = self.hexCanvas.create_text(offsetx, offsety, text=letter, font=(self.FONT_SELECT, 26), fill='black',tags=tagName)

    def makeHexArray(self, letters, centerX, centerY, sidelength, tagNames ):
        
        d1 = (math.sqrt(3)*sidelength)/2
        h = (2*d1) * math.sin(math.radians(30))
        l = (2*d1) * math.cos(math.radians(30))

        # Seven total Honeycomb Buttons
        self.makeHexButton(letters[1], centerX, centerY - (2*d1), sidelength, tagNames[1])
        self.makeHexButton(letters[2], centerX+l, centerY - h, sidelength, tagNames[2])
        self.makeHexButton(letters[3], centerX+l, centerY+h, sidelength, tagNames[3])
        self.makeHexButton(letters[4], centerX, centerY+ (2*d1), sidelength, tagNames[4])
        self.makeHexButton(letters[5], centerX-l, centerY+h, sidelength, tagNames[5])
        self.makeHexButton(letters[6], centerX-l, centerY- h, sidelength, tagNames[6])

        # Center button is special
        self.makeHexCenterButton(letters[0], centerX, centerY, sidelength, tagNames[0])


    def insertLetter(self, pos):
        if self.textInput.get() == "":
            self.textInput.insert(tk.END,self.letterSet[pos].upper())
        else:
            self.textInput.insert(tk.END,self.letterSet[pos].lower())

    def clicked1(self, *args):
        self.insertLetter(0)

    def clicked2(self, *args):
        self.insertLetter(1)

    def clicked3(self, *args):
        self.insertLetter(2)

    def clicked4(self, *args):
        self.insertLetter(3)

    def clicked5(self, *args):
        self.insertLetter(4)

    def clicked6(self, *args):
        self.insertLetter(5)

    def clicked7(self, *args):
        self.insertLetter(6)

    # Maps score out of 1000 possible. Maybe do something else?
    def updateScore(self, currentWordList):
        totalFound = self.ORIGINAL_LETTER_COUNT - self.countChars(currentWordList)
        scalar = 1000 / self.ORIGINAL_LETTER_COUNT
        return totalFound * scalar

    def updateHoney(self, score):
        maxScore = 1000 # subject to change so coding relative to this
        if score <= maxScore/4: # Only draw one jar
            conversion = 8 * (score / (maxScore/4))
            #print(" Initial calculation :",conversion)
            conversion = int(conversion)
            #print(" Now an int :",conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            #print(" Chosen picture is : ", choice)
            newPic = tk.PhotoImage(file =choice)
            self.honey1Label.configure(image = newPic)
            self.honey1Label.image = newPic
            self.honey1Label.grid(column=1,row=1)

        elif score <= maxScore/2: # Draw two jars
            conversion = 8 * ((score - (maxScore/4)) / (maxScore/4))
            conversion = int(conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            newPic = tk.PhotoImage(file =choice)
            self.honey2Label.configure(image = newPic)
            self.honey2Label.image = newPic
            self.honey2Label.grid(column=2,row=1)
            # Mandate previous jar is full
            newPic = tk.PhotoImage(file ='data/honey8_8.gif')
            self.honey1Label.configure(image = newPic)
            self.honey1Label.image = newPic
            self.honey1Label.grid(column=1,row=1)

        elif score <= 3* maxScore/4: # Draw three jars
            conversion = 8 * ((score - (maxScore/2)) / (maxScore/4))
            conversion = int(conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            newPic = tk.PhotoImage(file =choice)
            self.honey3Label.configure(image = newPic)
            self.honey3Label.image = newPic
            self.honey3Label.grid(column=3,row=1)
            # Mandate previous jar is full
            newPic = tk.PhotoImage(file ='data/honey8_8.gif')
            self.honey2Label.configure(image = newPic)
            self.honey2Label.image = newPic
            self.honey2Label.grid(column=2,row=1)
        
        elif score <= maxScore: # Draw four jars
            conversion = 8 * ((score - (3* maxScore/4)) / (maxScore/4))
            conversion = int(conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            newPic = tk.PhotoImage(file =choice)
            self.honey4Label.configure(image = newPic)
            self.honey4Label.image = newPic
            self.honey4Label.grid(column=4,row=1)
            # Mandate previous jar is full
            newPic = tk.PhotoImage(file ='data/honey8_8.gif')
            self.honey3Label.configure(image = newPic)
            self.honey3Label.image = newPic
            self.honey3Label.grid(column=3,row=1)

    def enterWord(self, event):
        guess = self.textInput.get().lower()
        if guess in self.currentWordList:
            print("")
            print("GOT ONE!")
            #print("Definition : ")
            #print(lookup(defList, guess))

            # Take the word out of list and put it in FOUND
            self.currentWordList.remove(guess)
            self.FOUND.append(guess)
            print(self.currentWordList)

            self.updateWordFrame()
            
            #TODO UPDATE SCORE
            self.SCORE = self.updateScore(self.currentWordList)
            self.scoreLabel.configure(text="SCORE: " + str(int(self.SCORE)))
            print("SCORE is : ", self.SCORE)
            self.updateHoney(self.SCORE)
        else:
            print("DARN!") 
        self.textInput.selection_clear()
        self.textInput.delete(0,tk.END)

    def makeBindings(self):
        self.hexCanvas.tag_bind("playbutton1","<Button-1>",self.clicked1)
        self.hexCanvas.tag_bind("playbutton2","<Button-1>",self.clicked2)
        self.hexCanvas.tag_bind("playbutton3","<Button-1>",self.clicked3)
        self.hexCanvas.tag_bind("playbutton4","<Button-1>",self.clicked4)
        self.hexCanvas.tag_bind("playbutton5","<Button-1>",self.clicked5)
        self.hexCanvas.tag_bind("playbutton6","<Button-1>",self.clicked6)
        self.hexCanvas.tag_bind("playbutton7","<Button-1>",self.clicked7)
        self.window.bind('<Return>', self.enterWord) 

    def drawWidgets(self):
        self.beeLabel.grid(column = 1, row = 1)
        self.textInput.grid(column = 2, row = 1)
        self.scoreLabel.grid(column=3, row= 1)
        self.hexCanvas.grid(column = 1, row = 2, columnspan = 2)
        #honeyFrame.grid(column = 3, row = 2)
        self.honeyFrame.grid(column = 1, row = 3, columnspan = 3, padx = 30)
        self.wordFrame.grid(column = 3, row = 2, columnspan = 2)
        #testFrame.grid(column = 1, row = 3, columnspan = 3)


    def printWord(self, word):
        print(word)
        print("Definition : ")
        print(lookup(self.defList, word))

    def wordLabelClicked(self, event):
        self.printWord(event.widget.cget("text"))

    def clearWordFrame(self):
        list = self.wordFrame.grid_slaves()
        for l in list:
            l.destroy()

    def updateWordFrame(self):
        # Wipe frame, then add word
        self.clearWordFrame()
        num = math.ceil(math.sqrt(len(self.FOUND)))
        for i in range(len(self.FOUND)):
            self.customLabel = tk.Label(self.wordFrame, text=self.FOUND[i], fg='Black',font=(self.FONT_SELECT, '20'))
            self.customLabel.bind("<Button-1>", self.wordLabelClicked)
            print("current lable column: ", int(i%num), ", row: ", int(i/num))
            self.customLabel.grid(column = int(i%num), row = int(i/num))




