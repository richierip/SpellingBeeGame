''' 5/29/2019 by PR - Spelling Bee game for kids :) '''

import random
MIN_WORD_SIZE = 3
MIN_WORDS_REQUIRED = 25
DICT_FILE = 'data\small_dict.txt'
DEF_FILE = 'data/azdictionary.txt'


def addedToDictionary(newWord):
    try:
        outF = open(DICT_FILE, "a")
        # write line to output file
        outF.write(newWord + "\n")
        outF.close()
        return True
    except:
        return False

def removedFromDictionary(word):
    retVal = False
    try:
        with open(DICT_FILE, "r") as f:
            lines = f.readlines()
        with open(DICT_FILE, "w") as f:
            for line in lines:
                if line.strip("\n") != word:
                    f.write(line)
                else:
                    retVal = True
        return retVal
    except:
        return False

def checkForRules(words, letters):
    hardLetters = ['q','z','x','v','j']
    if len(check(words,letters[0],letters)) < MIN_WORDS_REQUIRED:
        print("FAILED: TOO FEW WORDS FOUND")
        print(len(check(words,letters[0],letters)))
        return False
    # Make sure there aren't annoying letters in the same set
    elif len([i for i in hardLetters if i in letters]) >= 2:
        print("FAILED: ANNOYING LETTERS")
        return False
    return True

def getLetterset(words):
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    vowels = ['a','e','i','o','u']
    while True:
        print("In loop")
        twoVowels = random.sample(vowels, 2)
        fiveConsonants = random.sample(consonants,5)
        testLetterSet = twoVowels + fiveConsonants # Mandate that letterset has 2 vowels and five consonants
        print(testLetterSet)
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
    # Remove a trailing 's' from the word since only the root is in the dicionary
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
                
                # Parse the key for a comparison
                currentKey = currentKey.strip().lower()
                if word == currentKey:
                    test = True
                break
            currentKey += fullDict[i][j]

        # grab whole definition if it's a match
        if test:
            print("CURRENT KEY IS :", currentKey)
            print("LAST CHAR IS :", currentKey[-1])
            found.append(trimLine(fullDict[i][0:-1]))

            if doubleCheck < 10: # Check the next 10 entries as well
                doubleCheck +=1
                continue
            break
    
    if found == []:
        if word[-1] == 's':
            word = word[:-1]
            found = lookup(fullDict, word)
    return found

def check(words, keyletter, otherletters):
    found = []
    testPassed = True
    for i in range(len(words)):
        currentWord = words[i].strip()
        testPassed = True
        if keyletter not in currentWord:
            continue
        for j in range(len(currentWord)):
            if currentWord[j] not in otherletters:
                testPassed = False
                break
        if testPassed:
            print(currentWord)
            if len(currentWord) >= MIN_WORD_SIZE:
                found.append(currentWord)
    return found



