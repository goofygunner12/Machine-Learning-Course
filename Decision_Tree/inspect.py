import csv
import sys
import math as m

## Initialise Variables
democratCount = 0
republicanCount = 0

## Read the 'example1.csv' file
## Count the number of republican and democrat votes
with open(sys.argv[1], 'rb') as csvfile:
    fileReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for everyRow in fileReader:
        if(everyRow[-1].lower() == "democrat" or everyRow[-1].lower() == "a"):
            democratCount = democratCount + 1
        elif(everyRow[-1].lower() == "republican" or everyRow[-1].lower() == "nota"):
            republicanCount = republicanCount + 1
            

## Get the min, max and sum of attribute(democrat and republican)
minAttribute = min([republicanCount, democratCount])
maxAttribute = max([republicanCount, democratCount])
totalAttribute = sum([republicanCount, democratCount])

## Calculate the error, correct, and entropy values
error = (float(minAttribute)/float(totalAttribute))
correct = (float(maxAttribute)/float(totalAttribute))
entropy = (error * m.log(float(1/error),2)) + (correct * m.log(float(1/correct), 2))

## Print the entropy and error
sys.stdout.write("entropy: %s\n" % entropy )
sys.stdout.write("error: %s" % error)
