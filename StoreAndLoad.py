''' This file holds the user controlled information and methods to store that info persistently'''

import pickle

class userPresets:
    def __init__(self, name, color1, color2, highScoreTable, allTimeTable):
        self.name = name
        self.color1 = color1
        self.color2 = color2
        self.highScoreTable = highScoreTable
        self.allTimeTable = allTimeTable
        self.difficulty = 'Bee'

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

