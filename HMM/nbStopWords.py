import csv
import sys
import itertools
import math
from collections import defaultdict
import operator

# main function
def main():
    # Initialise the variables
    rawData = []; libCount = 0; conCount = 0; totalCount = 0; N = int(sys.argv[3])
    dictLib = defaultdict(int); dictCon = defaultdict(int); libCountPrime = 0; conCountPrime = 0

    # Read the raw training data from argv[1]
    with open(sys.argv[1], 'rb') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for fNames in fileReader:
            rawData.append([element.strip() for element in fNames])
    fileNames = list(itertools.chain(*rawData))

    # Store words in Liberals, Conservatives, and Vocabulary List
    for everyFName in fileNames:
        readFile = []
        with open(everyFName, 'r') as f:
            readFile = f.readlines()
            f.close()
        # Store the word list from Liberals file to libList
        if "con" in everyFName:
            conCount += 1
            for eachLine1 in readFile:
                dictCon[eachLine1.lower().strip()] += 1
        # Store the word list from Conservatives file to conList
        elif "lib" in everyFName:
            libCount += 1
            for eachLine2 in readFile:
                dictLib[eachLine2.lower().strip()] += 1
    # store the unique words into vocabulary list
    vocabulary = dictCon.copy()
    vocabulary.update(dictLib)
    sortedVocab = sorted(vocabulary.items(), key = operator.itemgetter(1), reverse = True)
    sortedVocab_ = sortedVocab[:N]

    for eachStopWord in sortedVocab_:
        if eachStopWord[0].lower().strip() in dictLib:
            #libCountPrime += dictLib[eachStopWord[0].lower().strip()]
            del dictLib[eachStopWord[0].lower().strip()]
        if eachStopWord[0].lower().strip() in dictCon:
            #conCountPrime += dictCon[eachStopWord[0].lower().strip()]
            del dictCon[eachStopWord[0].lower().strip()]

    totalCount = libCount + conCount

    probLib = float(libCount) / float(totalCount)
    probCon = float(conCount) / float(totalCount)
    nVocab = len(vocabulary) - N
    nLib = sum(dictLib.values()) + nVocab #- float(libCountPrime)
    nCon = sum(dictCon.values()) + nVocab #- float(conCountPrime)
    testNBClassifier(probLib, probCon, nLib, nCon, dictLib, dictCon, sortedVocab_)

# function to test Naive Bayes classifier
def testNBClassifier(probLib, probCon, nLib, nCon, dictLib, dictCon, sortedVocab_):
    rawData = []; correct = 0; wrong = 0
    with open(sys.argv[2], 'rb') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for fNames in fileReader:
            rawData.append([element.strip() for element in fNames])
    fileNames = list(itertools.chain(*rawData))
    for everyFName in fileNames:
        nkLib = 0; nkCon = 0; probWkLib = probLib; probWkCon = probCon
        readFile = []
        with open(everyFName, 'r') as f:
            readFile = f.readlines()
            f.close()
        for everyWord in readFile:
            if (everyWord.lower().strip() in dictLib or everyWord.lower().strip() in dictCon):
                if everyWord.lower().strip() not in sortedVocab_:
                    nkLib = dictLib[everyWord.lower().strip()] + 1
                    nkCon = dictCon[everyWord.lower().strip()] + 1

                    wkLib = float(nkLib) / float(nLib)
                    wkCon = float(nkCon) / float(nCon)

                    probWkLib += math.log(wkLib)
                    probWkCon += math.log(wkCon)
        # Check the Prob(Lib) and Prob(Con)
        probWkLib += math.log(probLib)
        probWkCon += math.log(probCon)

        if probWkLib > probWkCon and "lib" in everyFName:
            correct += 1
            sys.stdout.write("L\n")
        elif probWkLib > probWkCon and "con" in everyFName:
            wrong += 1
            sys.stdout.write("L\n")
        elif probWkLib < probWkCon and "con" in everyFName:
            correct += 1
            sys.stdout.write("C\n")
        elif probWkLib < probWkCon and "lib" in everyFName:
            wrong += 1
            sys.stdout.write("C\n")
    accuracy = float(correct) / float(correct + wrong)
    sys.stdout.write("Accuracy: %s" % round(accuracy, 4))

# Calling main()
if __name__ == "__main__":
    main()