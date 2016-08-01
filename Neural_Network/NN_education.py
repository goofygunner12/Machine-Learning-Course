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
    trainingData = np.array(rawData)
    trainingData = trainingData.astype(float)
    # for everyRow in trainingData:
    #     everyRow[0] = float(everyRow[0]) / float(100.0)
    #     everyRow[1] = float(everyRow[1]) / float(100.0)
    #     everyRow[2] = float(everyRow[2]) / float(100.0)
    #     everyRow[3] = float(everyRow[3]) / float(100.0)
    #     everyRow[4] = float(everyRow[4]) / float(100.0)
    #     everyRow[5] = float(everyRow[5]) / float(100.0)
    trainingData = np.divide(trainingData, float(100.0))
    #print trainingData.shape[1]-1

    # get xI from the training data
    xI = np.delete(trainingData, trainingData.shape[1]-1, 1)

    # get the target t column from the training data
    t = trainingData[:, trainingData.shape[1]-1]
    t = np.reshape(t, (t.shape[0], 1))

    # initialise random weights
    # wIJ --> weights connecting between the input and hidden nodes
    # wJK --> weights connecting between the hidden and output nodes
    numHiddenUnits = 3
    wIJ_ = np.random.uniform(-0.1, 0.1, (xI.shape[1], numHiddenUnits))
    wJK_ = np.random.uniform(-0.1, 0.1, (numHiddenUnits, 1))

    # initialise learning rate
    lr = 0.01

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
        delta_k = diff_t_OK * OK_der

        # get delta j
        sum_deltaK_wJK = delta_k.dot(np.transpose(wJK))
        OJ_der = OJ * (1 - OJ)
        delta_j = sum_deltaK_wJK * OJ_der

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
    testingData = np.array(rawTestData)
    testingData = testingData.astype(float)
    testingData = np.divide(testingData, 100.0)

    # Calculate the output
    OI_Test = testingData
    OJ_Test = sigmoid(np.dot(OI_Test, wIJ_Test))
    OK_Test = sigmoid(np.dot(OJ_Test, wJK_Test))
    OK_Test = np.multiply(OK_Test, 100.0)

    # print the output
    for i in range(0, OK_Test.shape[0]):
        sys.stdout.write("\n%s" % OK_Test[i][0])

# Sigmoid function to calculate sigmoid of a matrix
def sigmoid(matrix):
    # sigma(n) = 1 / (1 + e^-x)
    return 1.0 / (1.0 + np.exp(-1.0 * matrix))

# Calling main()
if __name__ == "__main__":
    main()