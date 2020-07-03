''' This file holds the Game object class instantiated in interface.py'''

import random, copy, math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Canvas
from tkinter import Frame
from wordGenerator import *
import StoreAndLoad
#import interface

Golden = '#F3C622'
ActiveGolden = '#FAE69E'
Gunmetal = '#23212C'
ActiveGunmetal = '#C7C5D3'
YellowOrange = '#FCB43A'
ActiveYellowOrange = '#FDD99B'
Onyx = "#3A3637"
ActiveOnyx = '#B6AFB1'
Lemon = '#FCD615'

class myGame:
    def __init__(self, window, hexCanvas, honeyFrame, wordFrame):
        self.WIDTH = None
        self.HEIGHT = None
        self.letterSet = None
        self.currentWordList = []
        self.textInput = None
        self.FONT_SELECT = 'Comic Sans'
        self.SCORE = 0
        self.hintPenalty = 0
        self.ORIGINAL_LETTER_COUNT = 0
        self.FOUND = []
        self.defList = []

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
        self.difficultyPic = None
        self.difficultyLabel = None
        self.shuffleIcon = None
        self.enterIcon = None
        self.deleteIcon = None
        self.customLabel = None
        self.blank = None

        # Pickle user values. put in new class in a bit
        self.userInfo = StoreAndLoad.loadObject('data/userInfo')
    
    # If no data yet (first time running the game), this is the default user
    def checkUser(self):
        if self.userInfo == None:
            self.userInfo = StoreAndLoad.userPresets('Ken', YellowOrange, Onyx, [], [])
        else:
            pass

    #######################################################################################
    #                               Hex Canvas Handlers                                   #
    #######################################################################################


    # This is done in a silly way, but it works for this. Hexagon colors change when mouse hovers over, 
    # even if it's technically over the text element and not the actual hexagon
    def _changeColor(self, event, colorPicked):
        element_id = self.hexCanvas.find_withtag(tk.CURRENT)
        currentTag = self.hexCanvas.gettags(element_id)
        if currentTag[0][-1] == 'l':
            self.hexCanvas.itemconfig(currentTag[0].rstrip('l'), fill=colorPicked)
        else:
            self.hexCanvas.itemconfig(tk.CURRENT, fill=colorPicked)

    def handle_enter(self, event):
        self._changeColor(event, ActiveOnyx)

    def handle_leave(self, event):
        self._changeColor(event, Onyx)

    def handle_enter_center(self, event):
        self._changeColor(event, ActiveGolden)

    def handle_leave_center(self, event):
        self._changeColor(event,Golden)
    
    def handle_enter_shuffle(self, event):
        self._changeColor(event,Golden)

    def handle_leave_shuffle(self, event):
        self._changeColor(event,'white')

    def handle_enter_delete(self, event):
        self._changeColor(event,Golden)

    def handle_leave_delete(self, event):
        self._changeColor(event,'white')

    def makeHexButton(self, letter, offsetx, offsety, sidelength, tagName):

        self.hexCanvas.create_polygon(sidelength+offsetx,offsety, (sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, 
                                        (-sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, (-sidelength)+offsetx,offsety,  
                                        (-sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, (sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, 
                                        fill = Onyx, outline = Gunmetal, tags=tagName)
        self.hexCanvas.create_text(offsetx, offsety, text=letter, font=(self.FONT_SELECT, 26), fill=Golden,tags=tagName + 'l')

    def makeHexCenterButton(self, letter, offsetx, offsety, sidelength, tagName):

        self.hexCanvas.create_polygon(sidelength+offsetx,offsety, (sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, 
                                        (-sidelength/2)+offsetx,((math.sqrt(3)*sidelength)/2)+offsety, (-sidelength)+offsetx,offsety,  
                                        (-sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, (sidelength/2)+offsetx,(-(math.sqrt(3)*sidelength)/2)+offsety, 
                                        fill = Golden, outline = 'white', tags=tagName)
        self.hexCanvas.create_text(offsetx, offsety, text=letter, font=(self.FONT_SELECT, 26), fill=Gunmetal,tags=tagName +'l')

    def deleteFromEntry(self, entry):
        txt = self.textInput.get()[:-1]
        self.textInput.delete(0, tk.END)
        self.textInput.insert(0, txt)

    def makeDeleteCircle(self):
        self.deleteIcon = icon = tk.PhotoImage(file = 'data/left-arrow.gif') # Have to do this to prevent garbage collection
        myWidth = int(self.hexCanvas.cget("width"))
        circumference = myWidth / 8
        self.hexCanvas.create_oval(circumference + 3, 5 , circumference*2 + 3, circumference + 5, fill = 'white', outline = Gunmetal, tags = 'delete')
        #self.hexCanvas.create_text(myWidth - (circumference/2), 5 + circumference/2, text='S', font=(self.FONT_SELECT, 17), fill=Onyx,tags='shuffle')
        self.hexCanvas.create_image((3 + 3*circumference/2, (5 + circumference/2)), image = self.deleteIcon ,tags='deletel')

    def shuffle(self, event):
        for item in self.hexCanvas.find_all(): 
            self.hexCanvas.delete(item) # Delete each item on the canvas

        centerLetter = self.letterSet[0]
        others = self.letterSet[1:]
        random.shuffle(others) # Rearrage everything except the center letter
        others.insert(0, centerLetter)
        self.letterSet = others # Important to set the class value
        self.makeHexArray(convertToUpper(others), 180, 180, 60) # Presets copied from main()  
    
    def makeShuffleCircle(self):
        
        self.shuffleIcon = icon = tk.PhotoImage(file = 'data/refresh-icon.gif') # Have to do this to prevent garbage collection
        myWidth = int(self.hexCanvas.cget("width"))
        circumference = myWidth / 8

        self.hexCanvas.create_oval(myWidth - circumference*2, 5 , myWidth-circumference, circumference + 5, fill = 'white', outline = Gunmetal, tags = 'shuffle')
        #self.hexCanvas.create_text(myWidth - (circumference/2), 5 + circumference/2, text='S', font=(self.FONT_SELECT, 17), fill=Onyx,tags='shuffle')
        self.hexCanvas.create_image((myWidth - (3*circumference/2), 5 + circumference/2), image = self.shuffleIcon ,tags='shufflel')

    def makeHexArray(self, letters, centerX, centerY, sidelength):
        self.makeDeleteCircle()
        self.makeShuffleCircle()

        # Create button tags
        tagNames = []
        for i in range(7):
            tagNames.append("playbutton"+str(i+1))
        
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
    def updateScore(self):
        totalFound = self.ORIGINAL_LETTER_COUNT - self.countChars(self.currentWordList)
        scalar = 1000 / self.ORIGINAL_LETTER_COUNT # Max score considered 1000 here
        self.SCORE = (totalFound * scalar) - self.hintPenalty

        self.scoreLabel.configure(text="SCORE: " + str(int(self.SCORE)))
        print("SCORE is : ", self.SCORE)
        self.updateHoney(self.SCORE)

    def clearHoneyFrame(self):
        print("$$$$$$$$$$")
        #self.blank = tk.PhotoImage(file = 'data/bee2.gif')
        if self.SCORE <750:
            self.honey4Label.configure(image = self.blank)
            self.honey4Label.image = self.blank
            self.honey4Label.grid(column=4,row=1)
        if self.SCORE <500:
            self.honey3Label.configure(image = self.blank)
            self.honey3Label.image = self.blank
            self.honey3Label.grid(column=3,row=1)
        if self.SCORE <250:
            self.honey2Label.configure(image = self.blank)
            self.honey2Label.image = self.blank
            self.honey2Label.grid(column=2,row=1)


    def updateHoney(self, score):
        self.clearHoneyFrame()
        maxScore = 1000 # subject to change so coding relative to this #TODO
        if score <= maxScore/4: # Only draw one jar
            conversion = 8 * (score / (maxScore/4))
            conversion = int(conversion)
            choice = 'data/honey' + str(conversion) +'_8.gif'
            newPic = tk.PhotoImage(file =choice)
            self.honey1Label.configure(image = newPic)
            self.honey1Label.image = newPic # Seems redundant, but needed to stop garbage collection
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

    def resetInputColor(self):
        self.textInput.configure(bg = 'white')

    def flashCorrect(self):
        self.textInput.configure(bg = 'green')
        self.window.after(150, self.resetInputColor)

    def flashIncorrect(self):
        self.textInput.configure(bg = 'red')
        self.window.after(150, self.resetInputColor)

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
            self.updateScore()
            self.flashCorrect()
        else:
            print("DARN!") 
            self.flashIncorrect()
        self.textInput.selection_clear()
        self.textInput.delete(0,tk.END)
            

        if self.currentWordList == []:
            if self.SCORE < 1000:
                self.SCORE = 1000
            self.endGame()

    def makeBindings(self):
        self.hexCanvas.tag_bind("playbutton1","<Button-1>",self.clicked1)
        self.hexCanvas.tag_bind("playbutton2","<Button-1>",self.clicked2)
        self.hexCanvas.tag_bind("playbutton3","<Button-1>",self.clicked3)
        self.hexCanvas.tag_bind("playbutton4","<Button-1>",self.clicked4)
        self.hexCanvas.tag_bind("playbutton5","<Button-1>",self.clicked5)
        self.hexCanvas.tag_bind("playbutton6","<Button-1>",self.clicked6)
        self.hexCanvas.tag_bind("playbutton7","<Button-1>",self.clicked7)
        self.hexCanvas.tag_bind("playbutton1l","<Button-1>",self.clicked1)
        self.hexCanvas.tag_bind("playbutton2l","<Button-1>",self.clicked2)
        self.hexCanvas.tag_bind("playbutton3l","<Button-1>",self.clicked3)
        self.hexCanvas.tag_bind("playbutton4l","<Button-1>",self.clicked4)
        self.hexCanvas.tag_bind("playbutton5l","<Button-1>",self.clicked5)
        self.hexCanvas.tag_bind("playbutton6l","<Button-1>",self.clicked6)
        self.hexCanvas.tag_bind("playbutton7l","<Button-1>",self.clicked7)
        self.hexCanvas.tag_bind("shuffle","<Button-1>",self.shuffle)
        self.hexCanvas.tag_bind("delete","<Button-1>",self.deleteFromEntry)
        self.hexCanvas.tag_bind("shufflel","<Button-1>",self.shuffle)
        self.hexCanvas.tag_bind("deletel","<Button-1>",self.deleteFromEntry)
        self.window.bind('<Return>', self.enterWord) 
        self.enterIcon.bind("<Button-1>", self.enterWord) 

        self.hexCanvas.tag_bind('shuffle', '<Enter>', self.handle_enter_shuffle)
        self.hexCanvas.tag_bind('shufflel', '<Enter>', self.handle_enter_shuffle)
        self.hexCanvas.tag_bind('shuffle', '<Leave>', self.handle_leave_shuffle)
        self.hexCanvas.tag_bind('shufflel', '<Leave>', self.handle_leave_shuffle)
        self.hexCanvas.tag_bind('delete', '<Enter>', self.handle_enter_delete)
        self.hexCanvas.tag_bind('deletel', '<Enter>', self.handle_enter_delete)
        self.hexCanvas.tag_bind('delete', '<Leave>', self.handle_leave_delete)
        self.hexCanvas.tag_bind('deletel', '<Leave>', self.handle_leave_delete)

        self.hexCanvas.tag_bind('playbutton1', '<Enter>', self.handle_enter_center)
        self.hexCanvas.tag_bind('playbutton1l', '<Enter>', self.handle_enter_center)
        self.hexCanvas.tag_bind('playbutton1', '<Leave>', self.handle_leave_center)
        self.hexCanvas.tag_bind('playbutton1l', '<Leave>', self.handle_leave_center)
        for i in range(2,8):
            name = "playbutton"+str(i)
            self.hexCanvas.tag_bind(name, '<Enter>', self.handle_enter)
            self.hexCanvas.tag_bind(name +'l', '<Enter>', self.handle_enter)
            self.hexCanvas.tag_bind(name, '<Leave>', self.handle_leave)
            self.hexCanvas.tag_bind(name +'l', '<Leave>', self.handle_leave)

    def drawWidgets(self):
        self.beeLabel.grid(column = 1, row = 1)
        self.textInput.grid(column = 2, row = 1, padx = (50,0))
        self.enterIcon.grid(column = 3,row = 1, padx = (0, 50))
        self.scoreLabel.grid(column=4, row= 1, padx = (130,0))
        self.hexCanvas.grid(column = 1, row = 2, columnspan = 2, padx = (50, 0))
        #honeyFrame.grid(column = 3, row = 2)
        self.honeyFrame.grid(column = 1, row = 3, columnspan = 4)#, padx = 30)
        self.wordFrame.grid(column = 3, row = 2, columnspan = 3, pady = (40,0))
        #testFrame.grid(column = 1, row = 3, columnspan = 3)

        #These are drawn INSIDE the honeyFrame, has its own gridding system
        self.honey1Label.grid(column=1,row=1)
        self.honey2Label.grid(column=2,row=1)
        self.honey3Label.grid(column=3,row=1)
        self.honey4Label.grid(column=4,row=1)

    #######################################################################################
    #                                     End Game                                        #
    #######################################################################################


    def clearWindow(self):
        list = self.window.grid_slaves()
        for l in list:
            l.destroy()

    # Helper fxn to grab table length up to 15 entries
    def getProperLength(self, length):
        if length < 15:
            return length
        else:
            return 15

    def createHSFrame(self, parent, w, h):
        highScoreFrame = Frame(parent, width=w, height = h)
        #self.beeLabel.grid(column = 0, row = 2)
        
        # Display the leaderboard title
        displayLabel = tk.Label(highScoreFrame, text= "Single-Game Leaderboard", fg=Gunmetal, bg = Lemon,font=(self.FONT_SELECT, '20'), width = 20, relief = 'groove')
        displayLabel.grid(row = 0, column = 0, columnspan = 3, pady = (15,30))

        for i in range(self.getProperLength(len(self.userInfo.highScoreTable))): #Picking the top 15 instead of len(self.userInfo.highScoreTable)
            if i % 2 ==0:
                bgColor = Onyx
                textColor = YellowOrange
            else:
                bgColor = YellowOrange
                textColor = Onyx

            currentObject = self.userInfo.highScoreTable[i]
            if int(self.SCORE) == currentObject[1] and self.userInfo.name == currentObject[0]:
                textColor = 'green' # Highlight the score for the game that just happened
            # For each row, name and associated score get own label, placed next to each other, with the same color scheme
            displayLabel = tk.Label(highScoreFrame, text= str(i+1) + "." , bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), width = 5)
            displayLabel.grid(column = 0, row = i+1)
            for j in range(len(currentObject)):
                if j ==1:
                    displayLabel = tk.Label(highScoreFrame, text= currentObject[j], bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), width = 20)
                else:
                    displayLabel = tk.Label(highScoreFrame, text= currentObject[j], bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), width = 10)
                displayLabel.grid(column = j+1, row = i+1)

        # Even if they're out of the top 15 put them on the list at the end
        if len(self.userInfo.highScoreTable) > 15 and self.SCORE < self.userInfo.highScoreTable[14][1]:
            # Find position in the table:
            pos = 0
            for i in range(len(self.userInfo.highScoreTable)):
                if int(self.SCORE) == self.userInfo.highScoreTable[i][1]:
                    pos = i
                    break
            
            displayLabel = tk.Label(highScoreFrame, text= str(pos+1) + ".", bg = Onyx, fg='red',font=(self.FONT_SELECT, '14'), width = 5, pady = 5)
            displayLabel.grid(column = 0, row = 16)
            displayLabel = tk.Label(highScoreFrame, text= self.userInfo.name, bg = Onyx, fg='red',font=(self.FONT_SELECT, '14'), width = 10, pady = 5)
            displayLabel.grid(column = 1, row = 16)
            displayLabel = tk.Label(highScoreFrame, text= str(int(self.SCORE)), bg = Onyx, fg='red',font=(self.FONT_SELECT, '14'), width = 20, pady = 5)
            displayLabel.grid(column = 2, row = 16)

        return highScoreFrame

    def createATFrame(self, parent, w, h, allTimeScore):
        allTimeFrame = Frame(parent, width=w, height = h)

        # Display the leaderboard title
        displayLabel = tk.Label(allTimeFrame, text= "All Time Leaderboard",fg=Gunmetal, bg=Lemon,font=(self.FONT_SELECT, '20'), width = 20 ,relief = 'groove' )
        displayLabel.grid(row = 0, column = 0, columnspan = 3, pady = (15,30))

        # Go through the all time array
        for i in range(self.getProperLength(len(self.userInfo.allTimeTable))): 
            if i % 2 ==0:
                bgColor = Onyx
                textColor = YellowOrange
            else:
                bgColor = YellowOrange
                textColor = Onyx

            currentObject = self.userInfo.allTimeTable[i]
            if self.userInfo.name == currentObject[0]:
                textColor = 'green' # Highlight your profile's score
            # For each row, name and associated score get own label, placed next to each other, with the same color scheme
            displayLabel = tk.Label(allTimeFrame, text= str(i+1) + "." , bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), width = 5)
            displayLabel.grid(column = 0, row = i+1)
            for j in range(len(currentObject)):
                if j ==1:
                    displayLabel = tk.Label(allTimeFrame, text= currentObject[j], bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), width = 20)
                else:
                    displayLabel = tk.Label(allTimeFrame, text= currentObject[j], bg = bgColor, fg=textColor,font=(self.FONT_SELECT, '14'), width = 10)
                displayLabel.grid(column = j+1, row = i+1)
        
        # Even if they're out of the top 15 put them on the list at the end 
        if len(self.userInfo.allTimeTable) > 15 and allTimeScore < self.userInfo.allTimeTable[14][1]:
            # Find position in the table:
            pos = 0
            for i in range(len(self.userInfo.allTimeTable)):
                if allTimeScore == self.userInfo.allTimeTable[i][1]:
                    pos = i
                    break
            displayLabel = tk.Label(allTimeFrame, text= str(pos+1) + "." , bg = Onyx, fg='red',font=(self.FONT_SELECT, '14'), width = 5, pady = 5)
            displayLabel.grid(column = 0, row = 16)

            displayLabel = tk.Label(allTimeFrame, text= self.userInfo.name, bg = Onyx, fg='red',font=(self.FONT_SELECT, '14'), width = 10, pady = 5)
            displayLabel.grid(column = 1, row = 16)
            displayLabel = tk.Label(allTimeFrame, text= str(allTimeScore), bg = Onyx, fg='red',font=(self.FONT_SELECT, '14'), width = 20, pady = 5)
            displayLabel.grid(column = 2, row = 16)

        return allTimeFrame
    
    def startOver(self, event):
        self.window.destroy()
        import interface
        interface.init()

    def showSolution(self, event):
        import scrollableFrame
        # Create new window and necesary Frames and scrollbar
        w = tk.Toplevel(width = self.WIDTH/2, height = 2*self.HEIGHT/3, takefocus = True)
        w.title("Puzzle Solution")
        masterFrame = Frame(w, width = self.WIDTH/2, height = 2*self.HEIGHT/3)
        foundFrame = scrollableFrame.ScrollableFrame(masterFrame, height = 2*self.HEIGHT/3)
        notFoundFrame = scrollableFrame.ScrollableFrame(masterFrame, height = 2*self.HEIGHT/3)

        def _on_mousewheel(event):
            x,y = masterFrame.winfo_pointerxy()
            widget = masterFrame.winfo_containing(x,y)
            widget.yview_scroll(int(-1*(event.delta/12)), "units")
        w.bind_all("<MouseWheel>", _on_mousewheel)

        # Create labels for every word and put them in the appropriate Frame
        for word in self.FOUND:
            displayLabel = tk.Label(foundFrame.scrollable_frame, text= word, fg=Onyx,font=(self.FONT_SELECT, '14'), pady = 5) 
            displayLabel.pack()

        for word in self.currentWordList:
            displayLabel = tk.Label(notFoundFrame.scrollable_frame, text= word.title(), fg=Onyx,font=(self.FONT_SELECT, '14'), pady = 5) 
            displayLabel.pack()

        # Put the bee there I guess 
        # beeLabel2 = tk.Label(w, image = self.beePic)
        # beeLabel2.pack()

        # Make and pack the Toplevel label and Frames
        message = "You found " + str(len(self.FOUND)) + " out of " + str(len(self.FOUND) + len(self.currentWordList)) + " possible words. "
        topLabel = tk.Label(w, text= message, fg=Onyx,font=(self.FONT_SELECT, '14'), padx = 10, pady = 5)
        leftLabel = tk.Label(masterFrame, text= 'Found', fg=Onyx,font=(self.FONT_SELECT, '14'), padx = 10, pady = 5) 
        rightLabel = tk.Label(masterFrame, text= 'Not Found', fg=Onyx,font=(self.FONT_SELECT, '14'), padx = 10, pady = 5)  
        leftLabel.grid(row = 0, column = 0, padx = 10)
        rightLabel.grid(row = 0, column = 1, padx = 10)
        foundFrame.grid(row = 1, column = 0, padx = 10, sticky=tk.N)
        notFoundFrame.grid(row = 1, column = 1, padx = 10, sticky=tk.N)
        topLabel.pack()
        masterFrame.pack()

    def endGame(self):
        # Add current user's score to the high score table, and re-sort it
        self.userInfo.highScoreTable.append((self.userInfo.name, int(self.SCORE )))
        self.userInfo.highScoreTable.sort(key=lambda x: x[1], reverse = True)

        # Add current user's score to their row in the all time table, or create a new row if needed, and re-sort it
        found = False
        allTimeScore = 0
        for i in range(len(self.userInfo.allTimeTable)):
            if self.userInfo.allTimeTable[i][0] != self.userInfo.name:
                continue
            else:
                # Have to reconstruct tuple for some reason
                allTimeScore = self.userInfo.allTimeTable[i][1] + int(self.SCORE)
                self.userInfo.allTimeTable[i] = (self.userInfo.allTimeTable[i][0],allTimeScore) 
                found = True
                break
        if not found:
            allTimeScore = int(self.SCORE)
            self.userInfo.allTimeTable.append((self.userInfo.name, int(self.SCORE )))
        self.userInfo.allTimeTable.sort(key=lambda x: x[1], reverse = True)

        # Clear everything, delete the Endgame menu option and Hint option
        self.clearWindow()
        self.rootMenu.delete(4) # THIS NEEDS TO BE THE LAST ITEM IN THE MENU OR ELSE
        self.rootMenu.delete(3) 
        
        leaderboardsFrame = Frame(self.window, width=880, height = self.HEIGHT )
        highScoreFrame = self.createHSFrame(leaderboardsFrame, 400, self.HEIGHT)
        allTimeFrame = self.createATFrame(leaderboardsFrame, 400, self.HEIGHT, allTimeScore)
        buttonFrame = Frame(self.window, width=880, height = 100 , pady = 45)

        # Initialize and grid buttons in their frame
        solutionButton = tk.Label(buttonFrame, text= "Show Solution",fg=Gunmetal, bg='white',font=(self.FONT_SELECT, '20'), width = 20 ,relief = 'groove', padx = 5 )
        solutionButton.grid(row = 0, column = 0, padx = 15)
        playAgainButton = tk.Label(buttonFrame, text= "Play Again",fg=Gunmetal, bg='white',font=(self.FONT_SELECT, '20'), width = 20 ,relief = 'groove', padx = 5  )
        playAgainButton.grid(row = 0, column = 1, padx = 15)

        # Bindings for buttons
        solutionButton.bind("<Button-1>", self.showSolution) 
        playAgainButton.bind("<Button-1>", self.startOver) 
        
        # High score on the left, all time on the right
        highScoreFrame.grid(row = 1, column = 1, padx = 35, sticky=tk.N)
        allTimeFrame.grid(row = 1, column = 2, padx = 35, sticky=tk.N)
        leaderboardsFrame.pack()
        buttonFrame.pack()

        # Use Pickle to store the tables persistently
        StoreAndLoad.storeObject(self.userInfo, 'data/userInfo')


    #######################################################################################
    #                                Definition Handlers                                  #
    #######################################################################################

    #TODO something with style consistency in here

    def displayDefinition(self, word):
        result = lookup(self.defList, word)
        defArray = result[0]
        word = result[1]

        print("Definition : ", defArray)
        w = tk.Toplevel(width = self.WIDTH/2, height = self.HEIGHT/2, takefocus = True)
        w.title("Dictionary" )
        w.focus()

        # Put the bee there I guess
        beeLabel2 = tk.Label(w, image = self.beePic)
        beeLabel2.pack()

        # If no definition is found, say so
        if defArray == []:
            displayLabel = tk.Label(w, text= "Sorry, I could not find this word in my dictionary ...", fg=Onyx,font=(self.FONT_SELECT, '14'))
            displayLabel.pack()

        else:
            if len(defArray) == 1:
                message = "I found one definition for " + word + " : "
            else:
                message = "I found " + str(len(defArray)) + " definitions for " + word + " : "

            displayLabel = tk.Label(w, text= message, fg=Onyx,font=(self.FONT_SELECT, '14'), padx = 10, pady = 10) 
            displayLabel.pack()
            for l in defArray:
                displayLabel = tk.Label(w, text= l, fg=Onyx,font=(self.FONT_SELECT, '14'), wraplength = 600 ) # WHY 600????
                displayLabel.pack()

        '''
        popupTextInput = tk.Entry(w,width=10,font=(self.FONT_SELECT, '36'))
        popupTextInput.focus() 
        popupTextInput.pack()
        '''

    def wordLabelClicked(self, event):
        print(event.widget)
        self.displayDefinition(event.widget.cget("text"))

        #TODO Why the hell is this frame resizing itself
        print("FRAME WIDTH IS ",self.wordFrame.cget("width"))
        print("FRAME HEIGHT IS ",self.wordFrame.cget("height"))

    def clearWordFrame(self):
        list = self.wordFrame.grid_slaves()
        for l in list:
            l.destroy()

    def makeActiveColor(self, event):
        event.widget.configure(bg = YellowOrange)

    def resetColor(self, event):
        event.widget.configure(bg = self.wordFrame.cget("bg"))

    def updateWordFrame(self):
        # Sort found words list show they show up alphabetically
        self.FOUND.sort()
        # Wipe frame
        self.clearWordFrame()

        #Regrid everything with new bindings   #TODO dynamically size the text?
        num = math.ceil(math.sqrt(len(self.FOUND)))
        fontSize = str(int(10/num + 18 ))
        for i in range(len(self.FOUND)):
            self.customLabel = tk.Label(self.wordFrame, text=self.FOUND[i], fg=Onyx, font=(self.FONT_SELECT, fontSize), padx = 4, pady = 3)
            self.customLabel.bind("<Button-1>", self.wordLabelClicked)
            self.customLabel.bind("<Enter>", self.makeActiveColor)
            self.customLabel.bind("<Leave>", self.resetColor)
            #print("current lable column: ", int(i%num), ", row: ", int(i/num))
            self.customLabel.grid(row = int(i%num), column = int(i/num))

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
            self.updateScore()

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
        displayLabel = tk.Label(w, textvariable= self.trackResult, fg=Onyx,font=(self.FONT_SELECT, '14'), padx = 10, pady = 10) 
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
            self.updateScore()

        if removedFromDictionary(word):
            message = "Success! You have removed " + word +" from the dictionary."
        else:
            message = "Whoops! Couldn't find " + word +  " in the dictionary"    
        self.trackResult.set(message)
        

    def removeHandler(self):
        w = tk.Toplevel(width = self.WIDTH/2, height = self.HEIGHT/2, takefocus = True)
        w.title("Remove a word from the Dictionary!" )
        w.bind('<Return>', self.removeWord)
        w.focus()

        # Put the bee there I guess 
        beeLabel2 = tk.Label(w, image = self.beePic)
        beeLabel2.pack()

        message = "Please enter a word you would like to remove : "
        self.trackResult.set(message)
        displayLabel = tk.Label(w, textvariable= self.trackResult, fg=Onyx,font=(self.FONT_SELECT, '14'), padx = 10, pady = 10) 
        displayLabel.pack()
        
        popupTextInput = tk.Entry(w,width=10,font=(self.FONT_SELECT, '36'))
        popupTextInput.focus() 
        popupTextInput.pack()

    def hintHandler(self):
        w = tk.Toplevel(width = self.WIDTH/2, height = self.HEIGHT/2, takefocus = True)
        w.title("Need some help?")

        # Put the bee there I guess 
        beeLabel2 = tk.Label(w, image = self.beePic)
        beeLabel2.pack()

        # Choose a random word
        candidates = copy.copy(self.currentWordList)

        # Find a word that has an acceptable definition to give as a hint, if there is one
        for i in range(len(candidates)):
            choice = random.choice(candidates)
            candidates.remove(choice)

            #Find a definition and possibly modified keyword
            result = lookup(self.defList, choice)
            defArray = result[0]
            if defArray == []: # Nothing to check if the dictionary has no results
                continue 
            choice = result[1].title()

            # Trim each definition : remove index words, or whole entry if the word is used in the entry (too easy to solve then)
            approvedDefinitions = []
            for line in defArray:
                    if type(line) == type([]):
                        continue
                    line = line.replace(choice, '')
                    if choice.lower() not in line:
                        approvedDefinitions.append(line)
            
            if approvedDefinitions != []:
                break

        # if no definition, print an anagram? For now, do nothing
        if defArray == []:
            displayLabel = tk.Label(w, text= "Sorry, I could not find this word in my dictionary ...", fg=Onyx,font=(self.FONT_SELECT, '14'))
            displayLabel.pack()

        else:
            # Dock some points
            self.hintPenalty += self.SCORE/15 #TODO decide appropriate penalty

            # Make and pack the labels
            if len(approvedDefinitions) == 1:
                message = "I took "+ str(int(self.SCORE/15)) +" points in exchange for a definition of a word you haven't found yet : "
            else:
                message = "I took "+ str(int(self.SCORE/15)) +" points in exchange for these definitions of a word you haven't found yet : "

            displayLabel = tk.Label(w, text= message, fg=Onyx,font=(self.FONT_SELECT, '14'), padx = 10, pady = 10) 
            displayLabel.pack()

            for line in approvedDefinitions: # Each line is a definition, already parsed and proofread
                displayLabel = tk.Label(w, text= line, fg=Onyx,font=(self.FONT_SELECT, '14'), wraplength = 600 ) # WHY 600????
                displayLabel.pack()
            # Finally, update the score display and honey jars
            self.updateScore()
     

    def makeMenu(self):
        self.rootMenu = Menu(self.window)
        new_item = Menu(self.rootMenu)
        #new_item.add_command(label='New')
        second_item = Menu(self.rootMenu)
        #second_item.add_command(label = "click", command = self.addWordToDict)
        self.rootMenu.add_cascade(label='File', menu=new_item)
        self.rootMenu.add_cascade(label='Add a word to the dictionary',command = self.addHandler)
        self.rootMenu.add_cascade(label='Remove a word from the dictionary',command = self.removeHandler)
        self.rootMenu.add_cascade(label='Hint',command = self.hintHandler)
        self.rootMenu.add_cascade(label='End Game',command = self.endGame)
        self.window.config(menu=self.rootMenu)




