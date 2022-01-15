''' Project - Spelling Bee game for kids :)

- Developed by Peter Richieri from scratch with much help from Google and online Tkinter manual pages
- Made on windows but should run fine on mac
- No special packages needed

This file holds the backend functions that parse the text files and generate the letterset used for the games
 '''

import random, copy
MIN_WORD_SIZE = 3
DICT_FILE = 'data/small_dict.txt'
DEF_FILE = 'data/azdictionary.txt'
REQUIRE_PANGRAM = True
PANGRAMS = []

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

def hasPangram(words,letters):
    foundPangram = False
    pangrams = []
    for word in words:
        testSet = copy.copy(letters)
        for character in word:
            if character in testSet: testSet.remove(character)
            if testSet == []:
                foundPangram = True
                pangrams.append(word)
                break
    
    if foundPangram:
        global PANGRAMS 
        PANGRAMS = pangrams

    return foundPangram
    

def checkForRules(words, letters, hardLetterCap, MIN_WORDS_REQUIRED):
    hardLetters = ['q','z','x','v','j']
    # Make sure there aren't annoying letters in the same set
    if len([i for i in hardLetters if i in letters]) >= hardLetterCap:
        #print("FAILED: ANNOYING LETTERS")
        return False
    if 'q' in letters and 'u' not in letters:
        return False

    myWordSet = check(words,letters[0],letters)
    if len(myWordSet) < MIN_WORDS_REQUIRED:
        #print("FAILED: TOO FEW WORDS FOUND")
        #print(len(check(words,letters[0],letters)))
        return False

    if REQUIRE_PANGRAM:
        return hasPangram(myWordSet,letters)
    
    return True

''' 
Center letter always a vowel. No more than 1 "hard letters", always two vowels.
'''
def easyMode(words):
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    vowels = ['a','e','i','o','u']
    while True:
        twoVowels = random.sample(vowels, 2)
        fiveConsonants = random.sample(consonants,5)
        testLetterSet = twoVowels + fiveConsonants # Mandate that letterset has 2 vowels and five consonants
        if(checkForRules(words, testLetterSet, 1, 30)):
            #print("LETTERSET", testLetterSet)
            return testLetterSet[0], testLetterSet, PANGRAMS

''' 
Center letter always a consonant. No more than 2 "hard letters", always two vowels.
'''
def mediumMode(words):
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    vowels = ['a','e','i','o','u']
    while True:
        twoVowels = random.sample(vowels, 2)
        fiveConsonants = random.sample(consonants,5)
        testLetterSet = fiveConsonants + twoVowels # Mandate that letterset has 2 vowels and five consonants
        if(checkForRules(words, testLetterSet, 3, 20)):
            #print("LETTERSET", testLetterSet)
            return testLetterSet[0], testLetterSet, PANGRAMS
'''
Center letter always a hard consonant. One or two vowels. Hard letter cap is 3, min words required is 20.
'''
def hardMode(words):
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    vowels = ['a','e','i','o','u']
    hardLetters = ['q','z','x','v','j', 'k', 'p', 'm', 'w', 'h', 'f']
    while True:
        consonantPool = copy.copy(consonants)
        center = [random.choice(hardLetters)]
        consonantPool.remove(center[0])
        numVowels = random.randint(1,2)
        myVowels = random.sample(vowels, numVowels)
        myConsonants = random.sample(consonantPool,6-numVowels)
        testLetterSet = center + myConsonants + myVowels 
        if(checkForRules(words, testLetterSet, 3, 20)):
            #print("LETTERSET", testLetterSet)
            return testLetterSet[0], testLetterSet, PANGRAMS

def getLetterset(words, difficulty):
    if difficulty == "Bee":
        return easyMode(words)
    elif difficulty == "Wasp":
        return mediumMode(words)
    elif difficulty == "Hornet":
        return hardMode(words)

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
    with open(fileName, encoding="utf8", errors='ignore', newline = '') as file:
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
                
                # Parse the key for a comparison
                currentKey = currentKey.strip().lower()
                if word == currentKey:
                    test = True
                break
            currentKey += fullDict[i][j]

        # grab whole definition if it's a match
        if test:
            found.append(trimLine(fullDict[i][0:-1]))

            if doubleCheck < 10: # Check the next 10 entries as well
                doubleCheck +=1
                continue
            break
    
    if found == []:
        # Try removing a trailing 's' from the word and see if you get a hit
        if word[-1] == 's':
            word = word[:-1]
            found = lookup(fullDict, word)[0] # only the definition to avoid nesting
    return [found,word]

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
            if len(currentWord) >= MIN_WORD_SIZE:
                found.append(currentWord)
    return found



