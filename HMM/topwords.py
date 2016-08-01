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
    totalCount = libCount + conCount

    # sort the dictionaries
    sortedDictLib = sorted(dictLib.items(), key = operator.itemgetter(1), reverse = True)
    sortedDictCon = sorted(dictCon.items(), key = operator.itemgetter(1), reverse = True)

    # get values to calculate probability
    probLib = float(libCount) / float(totalCount)
    probCon = float(conCount) / float(totalCount)
    nVocab = len(vocabulary)
    nLib = sum(dictLib.values()) + nVocab
    nCon = sum(dictCon.values()) + nVocab

    gettop20Prob(sortedDictLib, nLib, probLib)
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    gettop20Prob(sortedDictCon, nCon, probCon)

# calculate the probability
def gettop20Prob(sortedDict, n, prob):
    for i in range(0,20):
        nk = sortedDict[i][1] + 1
        wk = float(nk) / float(n)
        probWkLog = math.log(wk)
        probWk = math.exp(probWkLog)
        sys.stdout.write("%s " % sortedDict[i][0])
        sys.stdout.write("%s" % round(probWk, 4))
        if i <19:
            sys.stdout.write("\n")

# Calling main()
if __name__ == "__main__":
    main()