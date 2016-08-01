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
    # FOWARD ALGORITHM
    for O in ObservationSequenceList:
        T = len(O)
        alphaMatrix = np.zeros((N, T))
        # Step 1: Initialisation
        for n in range(0, N):
            alphaMatrix[n, 0] =  log(float(pi[statIndex[n]])) + log(float(B[statIndex[n], O[0]]))
        # Step 2: Induction
        for t in range(1, T):
            for i in range(0, N):
                logSum = (alphaMatrix[0, t-1]) + log(float(A[statIndex[0], statIndex[i]]))
                for j in range(1, N):
                    logSum = log_sum(logSum, (alphaMatrix[j, t-1]) + log(float(A[statIndex[j], statIndex[i]])))
                alphaMatrix[i, t] =  log(float(B[statIndex[i], O[t]]))+ logSum
        # Step 3: Termination
        logSumProb = alphaMatrix[0,-1]
        for xy in range(1, N):
            logSumProb = log_sum(logSumProb,alphaMatrix[xy,-1])
        sys.stdout.write("%s\n" % logSumProb)

# Get Observation Symbols from dev file
def getObservationSymbols(n):
    data = []; finalData = []
    with open(sys.argv[n], 'rb') as csvfile:
        file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for eachRow in file:
            data.append([d1.strip().split() for d1 in eachRow])
        for everyrow in data:
            finalData.append(list(chain(*everyrow)))
    #print finalData
    return finalData

# Get Probability Matrix
def getMatrix(n):
    fName = sys.argv[n]
    matrix ={}; stateIndex = {}; i = 0
    with open(fName, 'r') as f:
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

#computes log sum of two exponentiated log numbers efficiently
def log_sum(left,right):
	if right < left:
		return left + log1p(exp(right - left))
	elif left < right:
		return right + log1p(exp(left - right));
	else:
		return left + log1p(1)

# Calling main()
if __name__ == "__main__":
    main()