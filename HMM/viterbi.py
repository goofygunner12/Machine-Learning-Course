import sys
import csv
import numpy as np
import math
from math import *
from itertools import chain, izip

# main function
def main():
    # Read the tran, emit, and prior data
    # Store them in a numpy matrix
    A  = getMatrix(2)
    B = getMatrix(3)
    pi, statIndex = getMatrix(4)
    # Get the N and T values
    N = len(statIndex)
    # Read the input observation file
    ObservationSequenceList = getObservationSymbols(1)
    psi =[]; list3 = []
    # FOWARD ALGORITHM
    text_file = open("OutputA1.txt", "w")
    for O in ObservationSequenceList:
        T = len(O)
        alphaMatrix = np.zeros((N, T))
        # Step 1: Initialisation
        for n in range(0, N):
            alphaMatrix[n, 0] =  log(float(pi[statIndex[n]])) + log(float(B[statIndex[n], O[0]]))
        list2 =[];list1 = []; logSum = [0] * N; maxIndex=[-1] * N
        for t in range(1, T):
            maxState = -1
            for i in range(0, N):
                for j in range(0, N):
                    logSum[j] = (alphaMatrix[j, t-1]) + log(float(A[statIndex[j], statIndex[i]])) + log(float(B[statIndex[i], O[t]]))
                alphaMatrix[i, t] =  max(logSum)
                maxIndex[i] = logSum.index(max(logSum))
            psi.append(maxIndex[(alphaMatrix[:,t].argmax(axis=0))])
            sys.stdout.write("%s" %O[t-1])
            sys.stdout.write("_%s " % statIndex[maxIndex[(alphaMatrix[:,t].argmax(axis=0))]])
            if t == T - 1:
                sys.stdout.write("%s" %O[t])
                sys.stdout.write("_%s " % statIndex[(alphaMatrix[:,t].argmax(axis=0))])
        sys.stdout.write("\n")
    text_file.close()

# Get Observation Symbols from dev file
def getObservationSymbols(n):
    data = []; finalData = []
    with open(sys.argv[n], 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for eachRow in file:
            data.append([d1.strip().split() for d1 in eachRow])
        for everyrow in data:
            finalData.append(list(chain(*everyrow)))
    return finalData

# Get Probability Matrix
def getMatrix(n):
    fName = sys.argv[n]
    matrix ={}; stateIndex = {}; i = 0
    with open(fName, 'rb') as f:
        for everyLine in f:
            splitLine = everyLine.split()
            if (n == 4):
                stateIndex[i] = (splitLine[0])
                matrix[(splitLine[0])] = ",".join(splitLine[1:])
                i += 1
            else:
                for keyValuePair in splitLine[1:]:
                    (key, value) = keyValuePair.split(":")
                    matrix[(splitLine[0]), key] = value
    if (n != 4):
        return matrix
    else:
        return matrix, stateIndex

# Calling main()
if __name__ == "__main__":
    main()