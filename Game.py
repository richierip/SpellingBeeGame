''' This file holds the Game object class instantiated in interface.py'''

import random, copy, math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import *
import StoreAndLoad

class myGame:
    def __init__(self, window, hexCanvas, honeyFrame, currentWordList, letterSet, wordFrame, defList):
        self.WIDTH = None
        self.HEIGHT = None
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
        self.trackResult = tk.StringVar()
        self.rootMenu = None
        self.honey1Label = None
        self.honey2Label = None
        self.honey3Label = None
        self.honey4Label = None
        self.scoreLabel = None
        self.beeLabel = None
        self.beePic = None
        self.honeyPic = None
        self.customLabel = None

        # Pickle user values. put in new class in a bit
        self.userInfo = StoreAndLoad.loadObject('data/userInfo')
    
    def checkUser(self):
        if self.userInfo == None:
            self.userInfo = StoreAndLoad.userPresets('Ken', 'Yellow', 'Black', [])
        else:
            pass

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

    def countChars(self, wordList):
        count = 0
        for elem in wordList:
            count += len(elem)
        return count

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
            self.FOUND.append(guess.title())
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

        if self.SCORE >=999:
            self.endGame()

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
        self.hexCanvas.grid(column = 1, row = 2, columnspan = 2, padx = 50)
        #honeyFrame.grid(column = 3, row = 2)
        self.honeyFrame.grid(column = 1, row = 3, columnspan = 3, padx = 30)
        self.wordFrame.grid(column = 3, row = 2, columnspan = 2)
        #testFrame.grid(column = 1, row = 3, columnspan = 3)

        #These are drawn INSIDE the honeyFrame, has its own gridding system
        self.honey1Label.grid(column=1,row=1)
        self.honey2Label.grid(column=2,row=1)
        self.honey3Label.grid(column=3,row=1)
        self.honey4Label.grid(column=4,row=1)

    #######################################
    #               End Game              #
    #######################################


    def clearWindow(self):
        list = self.window.grid_slaves()
        for l in list:
            l.destroy()

    def endGame(self):
        self.userInfo.highScoreTable.append((self.userInfo.name, int(self.SCORE )))
        self.userInfo.highScoreTable.sort(key=lambda x: x[1])

        # Clear everything, delete the Endgame menu option
        self.clearWindow()
        self.rootMenu.delete(3) # THIS NEEDS TO BE THE LAST ITEM IN THE MENU OR ELSE
        endFrame = Frame(self.window, width=400, height =  self.HEIGHT)
        #self.beeLabel.grid(column = 0, row = 2)


        for i in range(len(self.userInfo.highScoreTable)):
            if i % 2 ==0:
                bgColor = 'black'
                textColor = 'white'
            else:
                bgColor = 'white'
                textColor = 'black'

            currentObject = self.userInfo.highScoreTable[i]

            for j in range(len(currentObject)):
                if j ==1:
                    displayLabel = tk.Label(endFrame, text= currentObject[j], bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), width = 20)
                else:
                    displayLabel = tk.Label(endFrame, text= currentObject[j], bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), padx = 30)
                displayLabel.grid(column = j, row = i+1)
        endFrame.pack()
        StoreAndLoad.storeObject(self.userInfo, 'data/userInfo')


    #######################################
    #          Definition Handlers        #
    #######################################

    #TODO something with style consistency in here

    def displayDefinition(self, word):
        defArray = lookup(self.defList, word)
        print("Definition : ", defArray)
        w = tk.Toplevel(width = self.WIDTH/2, height = self.HEIGHT/2, takefocus = True)
        w.title("Dictionary" )
        w.focus()

        # Put the bee there I guess
        #beeImg2 = tk.PhotoImage(file = 'data/bee2.gif')
        beeLabel2 = tk.Label(w, image = self.beePic)
        beeLabel2.pack()

        # If no definition is found, say so
        if defArray == []:
            displayLabel = tk.Label(w, text= "Sorry, I could not find this word in my dictionary ...", fg='Black',font=(self.FONT_SELECT, '14'))
            displayLabel.pack()

        else:
            if len(defArray) == 1:
                message = "I found one definition for " + word + " : "
            else:
                message = "I found " + str(len(defArray)) + " definitions for " + word + " : "

            displayLabel = tk.Label(w, text= message, fg='Black',font=(self.FONT_SELECT, '14'), padx = 10, pady = 10) 
            displayLabel.pack()
            for l in defArray:
                displayLabel = tk.Label(w, text= l, fg='Black',font=(self.FONT_SELECT, '14'), wraplength = 600 ) # WHY 600????
                displayLabel.pack()

        '''
        popupTextInput = tk.Entry(w,width=10,font=(self.FONT_SELECT, '36'))
        popupTextInput.focus() 
        popupTextInput.pack()
        '''

    def wordLabelClicked(self, event):
        self.displayDefinition(event.widget.cget("text"))

        #TODO Why the hell is this frame resizing itself
        print("FRAME WIDTH IS ",self.wordFrame.cget("width"))
        print("FRAME HEIGHT IS ",self.wordFrame.cget("height"))

    def clearWordFrame(self):
        list = self.wordFrame.grid_slaves()
        for l in list:
            l.destroy()

    def updateWordFrame(self):
        # Sort found words list show they show up alphabetically
        self.FOUND.sort()
        # Wipe frame
        self.clearWordFrame()

        #Regrid everything with new bindings   #TODO dynamically size the text?
        num = math.ceil(math.sqrt(len(self.FOUND)))
        for i in range(len(self.FOUND)):
            self.customLabel = tk.Label(self.wordFrame, text=self.FOUND[i], fg='Black',font=(self.FONT_SELECT, '20'), padx = 4, pady = 3)
            self.customLabel.bind("<Button-1>", self.wordLabelClicked)
            #print("current lable column: ", int(i%num), ", row: ", int(i/num))
            self.customLabel.grid(column = int(i%num), row = int(i/num))

    #######################################
    #          MENU Handlers        #
    #######################################

    def addWordToDict(self, event):
        word = event.widget.get().lower()
        event.widget.selection_clear()
        event.widget.delete(0,tk.END)
        
        isValid = True
        if self.letterSet[0] in word:
            for i in range(len(word)):
                if word[i] not in self.letterSet:
                    isValid = False
        if isValid:
            self.currentWordList.append(word)
            self.ORIGINAL_LETTER_COUNT += len(word)
            self.SCORE = self.updateScore(self.currentWordList)

        if addedToDictionary(word):
            message = "Success! You have added " + word +" to the dictionary."
        else:
            message = "Something went wrong :( . Close the program and try again, or edit the small_dict.txt file directly. "    
        self.trackResult.set(message)
        

    def addHandler(self):
        w = tk.Toplevel(width = self.WIDTH/2, height = self.HEIGHT/2, takefocus = True)
        w.title("Add a word to the Dictionary!" )
        w.bind('<Return>', self.addWordToDict)
        w.focus()

        # Put the bee there I guess 
        beeLabel2 = tk.Label(w, image = self.beePic)
        beeLabel2.pack()

        message = "Please enter a word you would like to add : "
        self.trackResult.set(message)
        displayLabel = tk.Label(w, textvariable= self.trackResult, fg='Black',font=(self.FONT_SELECT, '14'), padx = 10, pady = 10) 
        displayLabel.pack()
        
        popupTextInput = tk.Entry(w,width=10,font=(self.FONT_SELECT, '36'))
        popupTextInput.focus() 
        popupTextInput.pack()




    def removeWord(self, event):
        word = event.widget.get().lower()
        event.widget.selection_clear()
        event.widget.delete(0,tk.END)
        
        if word in self.currentWordList:
            self.currentWordList.remove(word)
            self.ORIGINAL_LETTER_COUNT -= len(word)
            self.SCORE = self.updateScore(self.currentWordList)

        if removedFromDictionary(word):
            message = "Success! You have removed " + word +" from the dictionary."
        else:
            message = "Whoops! Couldn't find " + word +  " in the dictionary"    
        self.trackResult.set(message)
        

    def removeHandler(self):
        w = tk.Toplevel(width = self.WIDTH/2, height = self.HEIGHT/2, takefocus = True)
        w.title("Remove a word to the Dictionary!" )
        w.bind('<Return>', self.removeWord)
        w.focus()

        # Put the bee there I guess 
        beeLabel2 = tk.Label(w, image = self.beePic)
        beeLabel2.pack()

        message = "Please enter a word you would like to remove : "
        self.trackResult.set(message)
        displayLabel = tk.Label(w, textvariable= self.trackResult, fg='Black',font=(self.FONT_SELECT, '14'), padx = 10, pady = 10) 
        displayLabel.pack()
        
        popupTextInput = tk.Entry(w,width=10,font=(self.FONT_SELECT, '36'))
        popupTextInput.focus() 
        popupTextInput.pack()

        
        

    def makeMenu(self):
        self.rootMenu = Menu(self.window)
        new_item = Menu(self.rootMenu)
        #new_item.add_command(label='New')
        second_item = Menu(self.rootMenu)
        #second_item.add_command(label = "click", command = self.addWordToDict)
        self.rootMenu.add_cascade(label='File', menu=new_item)
        self.rootMenu.add_cascade(label='Add a word to the dictionary',command = self.addHandler)
        self.rootMenu.add_cascade(label='Remove a word to the dictionary',command = self.removeHandler)
        self.rootMenu.add_cascade(label='End Game',command = self.endGame)
        self.window.config(menu=self.rootMenu)




