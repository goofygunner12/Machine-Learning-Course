import csv
import sys
import numpy as np
import time

# main function
def main():

    # Read the raw training data from argv[1]
    rawData = []
    with open(sys.argv[1], 'rb') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for everyRow1 in fileReader:
            rawData.append([element.strip() for element in everyRow1])

    # convert the raw data to numpy array
    rawData.pop(0)
    for everyRow in rawData:
        everyRow[0] = float(everyRow[0]) / float(2000.0)
        everyRow[1] = float(everyRow[1]) / float(7.0)
    trainingData = np.array(rawData)
    trainingData[trainingData == 'yes'] = '1'
    trainingData[trainingData == 'no'] = '0'
    trainingData = trainingData.astype(float)

    # get xI from the training data
    xI = np.delete(trainingData, trainingData.shape[1]-1, 1)

    # get the target t column from the training data
    t = trainingData[:, trainingData.shape[1]-1]
    t = np.reshape(t, (t.shape[0], 1))

    # initialise random weights
    # wIJ --> weights connecting between the input and hidden nodes
    # wJK --> weights connecting between the hidden and output nodes
    numHiddenUnits = 3
    wIJ_ = np.random.uniform(-0.25, 0.25, (xI.shape[1], numHiddenUnits))
    wJK_ = np.random.uniform(-0.25, 0.25, (numHiddenUnits, 1))

    # initialise learning rate
    lr = 0.005

    # call the back-propagation function to train the network
    wIJ_Test, wJK_Test = recursiveBackPropagation(lr, xI, t, wIJ_, wJK_)
    sys.stdout.write("TRAINING COMPLETED! NOW PREDICTING.")
    networkTesting(wIJ_Test, wJK_Test)

# Recursive Back-Propagation Algorithm
def recursiveBackPropagation(lr, xI, t, wIJ_, wJK_):
    wIJ = np.copy(wIJ_)
    wJK = np.copy(wJK_)
    OI = xI
    timeLimit = time.time() + 70
    while time.time() < timeLimit:
        # compute output of each layer (OI, OJ, and OK)
        OJ = []; OK = []
        OJ = sigmoid(np.dot(OI, wIJ))
        OK = sigmoid(np.dot(OJ, wJK))

        # get delta k
        diff_t_OK = t - OK
        OK_der = OK * (1 - OK)
        delta_k = OK_der * diff_t_OK

        # get delta j
        sum_deltaK_wJK = delta_k.dot(np.transpose(wJK))
        OJ_der = OJ * (1 - OJ)
        delta_j = OJ_der * sum_deltaK_wJK

        # update weights
        delta_wIJ = lr * np.transpose(OI).dot(delta_j)
        delta_wJK = lr * np.transpose(OJ).dot(delta_k)
        wIJ += delta_wIJ
        wJK += delta_wJK

        # calculate the error equation summation(t - OK)^2
        error = t*t + OK*OK - 2*t*OK
        sys.stdout.write("%s\n" % str(np.mean(np.abs(error))))
    # return trained weights
    return wIJ, wJK

# function to test the network
def networkTesting(wIJ_Test, wJK_Test):

    # read the testing data file
    rawTestData = []
    with open(sys.argv[2], 'rb') as csvfile:
        fileReader1 = csv.reader(csvfile, delimiter=',', quotechar='|')
        for everyRow in fileReader1:
            rawTestData.append([element.strip() for element in everyRow])

    # convert the raw data to numpy array
    rawTestData.pop(0)
    for everyRow in rawTestData:
        everyRow[0] = float(everyRow[0]) / float(2000.0)
        everyRow[1] = float(everyRow[1]) / float(7.0)
    testingData = np.array(rawTestData)
    testingData[testingData == 'yes'] = '1'
    testingData[testingData == 'no'] = '0'
    testingData = testingData.astype(float)

    # Calculate the output
    OI_Test = testingData
    OJ_Test = sigmoid(np.dot(OI_Test, wIJ_Test))
    OK_Test = sigmoid(np.dot(OJ_Test, wJK_Test))
    for i in range(0, OK_Test.shape[0]):
        if OK_Test[i] >= 0.4:
            sys.stdout.write("\nyes")
        else:
            sys.stdout.write("\nno")

# Sigmoid function to calculate sigmoid of a matrix
def sigmoid(matrix):
    # sigma(n) = 1 / (1 + e^-x)
    return 1.0 / (1.0 + np.exp(-1.0 * matrix))

# Calling main()
if __name__ == "__main__":
    main()