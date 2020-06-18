''' This file holds the user controlled information and methods to store that info persistently'''

# import random, copy, math
# import tkinter as tk
# from tkinter import scrolledtext
# from tkinter import Menu
# from tkinter import Canvas
# from tkinter import Frame
# from wordGenerator import *

import pickle

class userPresets:
    def __init__(self, name, color1, color2, highScoreTable):
        self.name = name
        self.color1 = color1
        self.color2 = color2
        self.highScoreTable = highScoreTable

def storeObject(obj, filename):
    try:
        outfile = open(filename, 'wb' )
        pickle.dump(obj, outfile)
        outfile.close()
        return True
    except:
        return False
        
def loadObject(filename):
    try:
        infile = open(filename,'rb')
        new_obj = pickle.load(infile)
        infile.close()
        return new_obj
    except:
        return None 

