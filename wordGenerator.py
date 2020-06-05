''' 5/29/2019 by PR - Spelling Bee game for kids :) '''

import random
MIN_WORD_SIZE = 3
MIN_WORDS_REQUIRED = 25
DICT_FILE = 'data\small_dict.txt'
DEF_FILE = 'data/azdictionary.txt'






def addToDictionary(newWord):
    outF = open(DICT_FILE, "a")
    # write line to output file
    outF.write(newWord + "\n")
    outF.close()

def checkForRules(words, letters):
    hardLetters = ['q','z','x','v','j']
    if len(check(words,letters[0],letters)) < MIN_WORDS_REQUIRED:
        return False
    # Make sure there aren't annoying letters in the same set
    elif len([i for i in hardLetters if i in letters]) >= 2:
        return False
    return True

def getLetterset(words):
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    vowels = ['a','e','i','o','u']
    while True:
        twoVowels = random.sample(vowels, 2)
        fiveConsonants = random.sample(consonants,5)
        testLetterSet = twoVowels + fiveConsonants # Mandate that letterset has 2 vowels and five consonants
        if(checkForRules(words, testLetterSet)):
            print("LETTERSET", testLetterSet)
            return testLetterSet[0], testLetterSet

def convertToUpper(letterset):
    newSet = []
    for i in range(len(letterset)):
        newSet.append(letterset[i].upper())

    return newSet

# def getInput():
#     wordset = input("\n Enter center letter first, followed by other letters : ")
#     keyletter = wordset[0]
#     otherletters = []
#     for i in range(len(wordset)):
#         otherletters.append(wordset[i])
#     return keyletter, otherletters


def getWords():
    '''Reads dictionary text file as input in command line'''

    dataset = []
    fileName = DICT_FILE
    with open(fileName, newline = '') as file:
        for line in file:
            dataset.append(line)

    dataset2 = []
    fileName = DEF_FILE
    with open(fileName, newline = '') as file:
        definition = ""
        for line in file:
            if line == "\n":
                dataset2.append(definition)
                definition = ""
            else:
                definition += line
            
    return dataset , dataset2

#TODO This is disgusting
def trimLine(line):
    return line.replace('\n','').lstrip().replace('  ',' ').replace('  ',' ')

def lookup(fullDict, word):
    word = word.lower()
    found = []
    test = True
    doubleCheck = 0
    for i in range(len(fullDict)):
        test = False
        currentKey = ""

        # Grab just the word out of the definition and test it
        for j in range(len(fullDict[i])-1):
            if fullDict[i][j] == '(':
                if word == currentKey.strip().lower():
                    test = True
                break
            currentKey += fullDict[i][j]

        # grab whole definition if it's a match
        if test:
            print("CURRENT KEY IS :", currentKey)
            found.append(trimLine(fullDict[i][0:-1]))

            if doubleCheck < 10: # Check the next 10 entries as well
                doubleCheck +=1
                continue
            break
    return found

def check(words, keyletter, otherletters):
    found = []
    test = True
    for i in range(len(words)):
        test = True
        if keyletter not in words[i]:
            continue
        for j in range(len(words[i])-1):
            if words[i][j] not in otherletters:
                test = False
                break
        if test:
            if len(words[i][0:-1]) >= MIN_WORD_SIZE:
                found.append(words[i][0:-1])
    return found



