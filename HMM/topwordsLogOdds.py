import csv
import sys
import itertools
import math
from collections import defaultdict
import operator

# main function
def main():
    # Initialise the variables
    rawData = []; libCount = 0; conCount = 0; totalCount = 0
    dictLib = defaultdict(int); dictCon = defaultdict(int)
    correct = 0; wrong = 0

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

    # get values to calculate probability
    nVocab = len(vocabulary)
    nLib = sum(dictLib.values()) + nVocab
    nCon = sum(dictCon.values()) + nVocab

    #
    dictOfProbLib = getProbValues(nLib, nCon, dictLib, dictCon)
    dictOfProbCon = getProbValues(nCon, nLib, dictCon, dictLib)

    # sort the dictionaries
    sortedDictLib = sorted(dictOfProbLib.items(), key = operator.itemgetter(1), reverse = True)
    sortedDictCon = sorted(dictOfProbCon.items(), key = operator.itemgetter(1), reverse = True)

    gettop20Prob(sortedDictLib)
    sys.stdout.write("\n\n")
    gettop20Prob(sortedDictCon)

# calculate the probability
def getProbValues(n1, n2, dict1, dict2):
    nkLib = 0; nkCon = 0; probWkLib = 0; probWkCon = 0; dictOfProb = defaultdict(int)
    for everyWord in dict1:
        nk1 = dict1[everyWord.lower().strip()] + 1
        nk2 = dict2[everyWord.lower().strip()] + 1

        wk1 = float(nk1) / float(n1)
        wk2 = float(nk2) / float(n2)

        probWkLib = math.log(wk1)
        probWkCon = math.log(wk2)

        dictOfProb[everyWord.lower().strip()] = float(probWkLib) - float(probWkCon)
    return dictOfProb

# calculate the probability
def gettop20Prob(sortedDict1):
    for i in range(0,20):
        sys.stdout.write("%s " % sortedDict1[i][0])
        sys.stdout.write("%s" % round(sortedDict1[i][1], 4))
        if i <19:
            sys.stdout.write("\n")


# Calling main()
if __name__ == "__main__":
    main()