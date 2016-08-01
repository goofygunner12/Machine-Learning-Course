import csv
import sys
import math as m
import numpy as np

def main():
    ## Initialise variables
    oneValuedList = ['y', 'democrat', 'A', 'before1950', 'yes', 'fast', 'expensive', 'high', 'Two', 'large', 'morethan3min']
    zeroValuedList = ['n', 'notA', 'republican', 'after1950', 'no', 'slow', 'lessthan3min', 'cheap', 'low', 'MoreThanTwo', 'small']
    rawDataList = []; attributeLabels = []; dataListOfLists = []; zeroListOfLists = []
    oneListOfLists = []; EntropyValueListOfLists = []; initialEntropyValueList = []
    countValuesList = []; decisionTree = []; attPosValueLabels =[]; attNegValueLabels =[]
    zeroesCount = []; onesCount = []; formulaList =[]; testDataList =[]; testData = []
    initialEntropy = True; getZeroes = True
    ## Read the CSV File and append it to a rawDataList
    with open(sys.argv[1], 'rb') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for everyRow in fileReader:
            rawDataList.append(everyRow)
            #rawDataList.append([element.strip() for element in everyRow])

    for i in range(0, len(rawDataList[0])):
        attPosValueLabels.append("-")
        attNegValueLabels.append("-")
    ## Read the Raw Data and append it to a binaryFormDataList
    for everyRow in rawDataList:
        dataList = []
        i = 0
        for eachElement in everyRow:
            if eachElement in oneValuedList:
                dataList.append(1)
                if eachElement not in attPosValueLabels[i]:
                    attPosValueLabels[i] = (eachElement)
            elif eachElement in zeroValuedList:
                dataList.append(0)
                if eachElement not in attNegValueLabels[i]:
                    attNegValueLabels[i] =(eachElement)
            else:
                dataList.append(eachElement)
            i = i + 1
        dataListOfLists.append(dataList)
    ## assign values to attribute labels
    attributeLabels = dataListOfLists[0]
    dataListOfLists.pop(0)
    ## convert raw data to binary form
    for i in range(0, len(dataListOfLists[0])):
        countValues, entropyValue = classEntropy(i, dataListOfLists, initialEntropy, len(attributeLabels)-1)
        initialEntropyValueList.append(entropyValue)
        countValuesList.append(countValues)
    ## get the root key and value
    #print min(initialEntropyValueList)
    if  initialEntropyValueList[-1] - min(initialEntropyValueList)>= 0.1:
        rootKey = initialEntropyValueList.index(min(initialEntropyValueList))
        rootValue = min(initialEntropyValueList)
        decisionTree.append(rootKey)
        initialEntropy = False
    #print initialEntropyValueList
    #print decisionTree
    ##
    if len(decisionTree) == 1:
        if getZeroes == True:
            entropyValueLists = []
            zeroList = getDataList(getZeroes, rootKey, dataListOfLists)
            zeroListOfLists.append(zeroList)        
            for i in range(0, len(dataListOfLists[0])-1):
                countZeroValuesRoot, entropyZeroValueRoot = classEntropy(i, zeroList, initialEntropy, rootKey)
                entropyValueLists.append(entropyZeroValueRoot)
                zeroesCount.append(countZeroValuesRoot)
            EntropyValueListOfLists.append(entropyValueLists)

            entropyValueLists = []
            getZeroes = False
            oneList = getDataList(getZeroes, rootKey, dataListOfLists)
            oneListOfLists.append(oneList)        
            for i in range(0, len(dataListOfLists[0])-1):
                countOneValuesRoot, entropyOneValueRoot = classEntropy(i, oneList, initialEntropy, rootKey)
                entropyValueLists.append(entropyOneValueRoot)
                onesCount.append(countOneValuesRoot)

            EntropyValueListOfLists.append(entropyValueLists)
            getZeroes = True


    if  EntropyValueListOfLists[0][decisionTree[0]] - min(EntropyValueListOfLists[0])>= 0.1:
        rootKeyNew = EntropyValueListOfLists[0].index(min(EntropyValueListOfLists[0]))
        rootValue = min(EntropyValueListOfLists[0])
        decisionTree.append(rootKeyNew)
    else:
        decisionTree.append(-1)
    if  EntropyValueListOfLists[1][decisionTree[0]] - min(EntropyValueListOfLists[1])>= 0.1:
        rootKeyNew2 = EntropyValueListOfLists[1].index(min(EntropyValueListOfLists[1]))
        rootValue = min(EntropyValueListOfLists[1])
        decisionTree.append(rootKeyNew2)
    else:
        decisionTree.append(-1)

    sys.stdout.write("[%s+/" % countValuesList[-1][-1])
    sys.stdout.write("%s-]\n" % countValuesList[-1][0])

    sys.stdout.write("%s = " % attributeLabels[decisionTree[0]])
    sys.stdout.write("%s: " % attPosValueLabels[decisionTree[0]])
    sys.stdout.write("[%s+/" % countValuesList[decisionTree[0]][-1])
    sys.stdout.write("%s-]\n" % countValuesList[decisionTree[0]][-2])
    depth1PosRes =  np.argmax([countValuesList[decisionTree[0]][-2],countValuesList[decisionTree[0]][-1]])
    if len(decisionTree) == 3 and decisionTree[2] != -1 :
        sys.stdout.write("| %s = " % attributeLabels[decisionTree[2]])
        sys.stdout.write("%s: " % attPosValueLabels[decisionTree[2]])
        sys.stdout.write("[%s+/" % onesCount[decisionTree[2]][-1])
        sys.stdout.write("%s-]\n" % onesCount[decisionTree[2]][-2])
        depth2PosPosRes = np.argmax([onesCount[decisionTree[2]][-2],onesCount[decisionTree[2]][-1]])


        sys.stdout.write("| %s = " % attributeLabels[decisionTree[2]])
        sys.stdout.write("%s: " % attNegValueLabels[decisionTree[2]])
        sys.stdout.write("[%s+/" % onesCount[decisionTree[2]][-3])
        sys.stdout.write("%s-]\n" % onesCount[decisionTree[2]][-4])
        depth2PosNegRes = np.argmax([onesCount[decisionTree[2]][-4],onesCount[decisionTree[2]][-3]])

    sys.stdout.write("%s = " % attributeLabels[decisionTree[0]])
    sys.stdout.write("%s: " % attNegValueLabels[decisionTree[0]])
    sys.stdout.write("[%s+/" % countValuesList[decisionTree[0]][-3])
    sys.stdout.write("%s-]\n" % countValuesList[decisionTree[0]][-4])
    depth1NegRes =  np.argmax([countValuesList[decisionTree[0]][-4],countValuesList[decisionTree[0]][-3]])
    if len(decisionTree) >= 2 and decisionTree[1] != -1 :
        sys.stdout.write("| %s = " % attributeLabels[decisionTree[1]])
        sys.stdout.write("%s: " % attPosValueLabels[decisionTree[1]])
        sys.stdout.write("[%s+/" % zeroesCount[decisionTree[1]][-1])
        sys.stdout.write("%s-]\n" % zeroesCount[decisionTree[1]][-2])
        depth2NegPosRes = np.argmax([zeroesCount[decisionTree[1]][-2],zeroesCount[decisionTree[1]][-1]])

        sys.stdout.write("| %s = " % attributeLabels[decisionTree[1]])
        sys.stdout.write("%s: " % attNegValueLabels[decisionTree[1]])
        sys.stdout.write("[%s+/" % zeroesCount[decisionTree[1]][-3])
        sys.stdout.write("%s-]\n" % zeroesCount[decisionTree[1]][-4])
        depth2NegNegRes = np.argmax([zeroesCount[decisionTree[1]][-4],zeroesCount[decisionTree[1]][-3]])
    dummyFormula =[]
    for i in range(len(rawDataList[0])):
        dummyFormula.append(-1)

    if -1 not in decisionTree:
        formula1 = dummyFormula[:]
        formula1[decisionTree[0]] = 0
        formula1[decisionTree[1]] = 0
        formula1[-1] = depth2NegNegRes
        formulaList.append(formula1)

        formula2 = dummyFormula[:]
        formula2[decisionTree[0]] = 0
        formula2[decisionTree[1]] = 1
        formula2[-1] = depth2NegPosRes
        formulaList.append(formula2)

        formula3 = dummyFormula[:]
        formula3[decisionTree[0]] = 1
        formula3[decisionTree[2]] = 0
        formula3[-1] = depth2PosNegRes
        formulaList.append(formula3)

        formula4 = dummyFormula[:]
        formula4[decisionTree[0]] = 1
        formula4[decisionTree[2]] = 1
        formula4[-1] = depth2PosPosRes
        formulaList.append(formula4)

    elif decisionTree[1] == -1:
        formula1 = dummyFormula[:]
        formula1[decisionTree[0]] = 0
        formula1[-1] = depth1NegRes
        formulaList.append(formula1)

        formula3 = dummyFormula[:]
        formula3[decisionTree[0]] = 1
        formula3[decisionTree[2]] = 0
        formula3[-1] = depth2PosNegRes
        formulaList.append(formula3)

        formula4 = dummyFormula[:]
        formula4[decisionTree[0]] = 1
        formula4[decisionTree[2]] = 1
        formula4[-1] = depth2PosPosRes
        formulaList.append(formula4)

    elif decisionTree[2] == -1:
        formula1 = dummyFormula[:]
        formula1[decisionTree[0]] = 0
        formula1[decisionTree[1]] = 0
        formula1[-1] = depth2NegNegRes
        formulaList.append(formula1)

        formula2 = dummyFormula[:]
        formula2[decisionTree[0]] = 0
        formula2[decisionTree[1]] = 1
        formula2[-1] = depth2NegPosRes
        formulaList.append(formula2)

        formula3 = dummyFormula[:]
        formula3[decisionTree[0]] = 1
        formula3[-1] = depth1PosRes
        formulaList.append(formula3)

    with open(sys.argv[2], 'rb') as csvfile:
        fileReader1 = csv.reader(csvfile, skipinitialspace=False, delimiter=',', quotechar='|')
        for everyRow in fileReader1:
            testData = []
            for eachElement in everyRow:
                if eachElement in oneValuedList:
                    testData.append(1)
                elif eachElement in zeroValuedList:
                    testData.append(0)
                else:
                    testData.append(eachElement)
            testDataList.append(testData)
    testDataList.pop(0)
    error_train = getError(np.array(formulaList), np.array(dataListOfLists))
    error_test = getError(np.array(formulaList), np.array(testDataList))
    sys.stdout.write("error(train): %s\n" % error_train )
    sys.stdout.write("error(test): %s" % error_test )

def getError(formulaList1, dataList1):
    correct = 0.0
    errorValue = 0.0
    #print dataList
    for everyFormula in formulaList1:
        for each_attribute_list in dataList1:
            if (each_attribute_list[:][everyFormula != -1] ==  everyFormula[everyFormula != -1]).all():
                correct = correct + 1
    errorValue = (len(dataList1)-correct)/ float(len(dataList1))
    return errorValue

## Method to get entropy values for the list
def classEntropy(i, dataList, initialEntropy, rootKey):
    ## Initialise variables
    zeroZeroCount = 0; oneOneCount = 0; oneZeroCount = 0; zeroOneCount = 0
    totalEntropy = 0; zeroEntropy = 0; oneEntropy = 0
    oneError = 0; zeroError = 0; zeroCorrect = 0; oneCorrect = 0
    countList = []

    ## Check if the index i equals to the index of the class/result column
    ## If not, then perform entropy calculation as below.
    if i != len(dataList[0])-1:
        for everyRow in dataList:
            if(everyRow[i] == 1 and everyRow[-1] == 1):
                oneOneCount = oneOneCount + 1
            elif(everyRow[i] == 0 and everyRow[-1] == 1):
                zeroOneCount = zeroOneCount + 1
            elif(everyRow[i] == 1 and everyRow[-1] == 0):
                oneZeroCount = oneZeroCount + 1
            elif(everyRow[i] == 0 and everyRow[-1] == 0):
                zeroZeroCount = zeroZeroCount + 1

        totalOneAttribute = sum([oneZeroCount, oneOneCount])
        totalZeroAttribute = sum([zeroZeroCount, zeroOneCount])
        totalSum = sum([totalZeroAttribute, totalOneAttribute])
        #print totalOneAttribute, oneZeroCount, oneOneCount


        if totalOneAttribute != 0:
            oneError =  (float(oneZeroCount)/float(totalOneAttribute))
            oneCorrect = (float(oneOneCount)/float(totalOneAttribute))
        if totalZeroAttribute != 0:
            zeroError = (float(zeroZeroCount)/float(totalZeroAttribute))
            zeroCorrect = (float(zeroOneCount)/float(totalZeroAttribute))
        
        ## Converting all zero values to one, because of DIV by Zero issue.
        ## Also, converting to one would still result in zero when we take the log in calculations
        if oneError == 0: oneError = 1
        if zeroError == 0: zeroError = 1
        if zeroCorrect == 0: zeroCorrect = 1
        if oneCorrect == 0: oneCorrect = 1

        if i != rootKey:
            zeroEntropy = ((float(totalOneAttribute)/float(totalSum))*((float(oneError) * m.log(float(1/float(oneError)),2)) + (float(oneCorrect) * m.log(float(1/float(oneCorrect)), 2))))
            oneEntropy = ((float(totalZeroAttribute)/float(totalSum))*((float(zeroError) * m.log(float(1/float(zeroError)),2)) + (float(zeroCorrect) * m.log(float(1/float(zeroCorrect)), 2))))
            totalEntropy = float(zeroEntropy) + float(oneEntropy)
        elif i == rootKey:
            #print "wewexrx"
            zeroEntropy = (((oneError * m.log(float(1/oneError),2)) + (oneCorrect * m.log(float(1/oneCorrect), 2))))
            oneEntropy = (((zeroError * m.log(float(1/zeroError),2)) + (zeroCorrect * m.log(float(1/zeroCorrect), 2))))
            totalEntropy = float(zeroEntropy) + float(oneEntropy)
    ## If this is a initial entropy, we need to calculate
    elif initialEntropy == True:
        for everyRow in dataList:
            if(everyRow[-1] == 1):
                oneOneCount = oneOneCount + 1
            elif(everyRow[-1] == 0):
                zeroZeroCount = zeroZeroCount + 1
        zeroError = (float(zeroZeroCount)/float(zeroZeroCount+oneOneCount))
        oneCorrect = (float(oneOneCount)/float(zeroZeroCount+oneOneCount))
        totalEntropy = (zeroError * m.log(float(1/zeroError),2)) + (oneCorrect * m.log(float(1/oneCorrect), 2))
    countList.append(zeroZeroCount)
    countList.append(zeroOneCount)
    countList.append(oneZeroCount)
    countList.append(oneOneCount)

    return countList, totalEntropy

## Method to get the data list for the root key
def getDataList(getZeroes, index, dataList):
    setDataList = []
    for everyRow in dataList:
        if everyRow[index] == 0 and getZeroes == True:
            setDataList.append(everyRow)
        elif everyRow[index] == 1 and getZeroes == False:
            setDataList.append(everyRow)
    return setDataList

## Calling main()
if __name__ == "__main__":
    main()
