import sys
import math
import numpy as np

# Get the number of attributes
num_attributes = 9

# Calculate the input space value.
# |X| = No_of_attributes_of_x1 * ... * No_of_attributes_of_xn
# Since each attribute has two possible values, we use 2^num_attributes
input_space = int(math.pow(2, num_attributes))

# Calculate the concept space value. |C| = 2^|X|
concept_space = math.pow(2, input_space)

# Calculate the number of decimal digits
num_decimal_digits = int(math.log10(concept_space))+1

# Calculate the Hypothesis Space
hypothesis_space = int(math.pow(3, num_attributes))+1

# Print the size of the input space
sys.stdout.write("%s" % input_space)

# Print the size of the concept space
sys.stdout.write("\n%s" % num_decimal_digits)

# Print the size of the hypothesis space
sys.stdout.write("\n%s" % hypothesis_space)


# Initialise a set of attribute names and assign values.
# This set will be used to remove all the attribute names
# and keep the attribute values only from the inpute data.
attribute_names_set = {'gender', 'age', 'student?', 'previouslydeclined?',
                       'hairlength', 'employed?', 'typeofcolateral',
                       'firstloan', 'lifeinsurance', 'risk'}

# Assign the path of the input file to a variable.
input_train_path = "9Cat-Train.labeled"

# Open the input file after obtaining its path.
input_train_read = open(input_train_path, "r")

# Read the input file data
list_of_all_train_inputs = input_train_read.readlines()

# A list that contains attribute values only.
attribute_values_list = [' '.join(word for word in list_of_train_inputs.split()
                  if word.lower() not in attribute_names_set)
         for list_of_train_inputs in list_of_all_train_inputs]

# Initialise the list that stores the lists of attribute values.
attr_values_list_of_lists = []

# Append all the attribute values of a single row list into list of lists
for every_values in attribute_values_list:
    items = every_values.split()
    attr_values_list_of_lists.append(items)
    

# Find-S Algorithm
hypothesis_list_lists =[]
hypothesis = ['-','-','-','-','-','-','-','-','-']
counter = 0
for each_attribute_list in attr_values_list_of_lists:
    if each_attribute_list[9] == "high":
        i = 0        
        for each_attribute_hypothesis in hypothesis: 
            if each_attribute_hypothesis == "-":
                hypothesis[i] = each_attribute_list[i]
            elif each_attribute_hypothesis != each_attribute_list[i]:
                hypothesis[i] = "?"
            i = i + 1                
    counter = counter + 1
    if counter == 30:
        counter = 0
        hypothesis_list_lists.append(hypothesis[:])

# Print the list of hypothesis saved at every 30 instances into a file
with open('partA4.txt', 'w') as file:
    file.writelines('\t'.join(i) + '\n' for i in
                    hypothesis_list_lists)

# Assign the path of the input file to a variable.
input_dev_path = "9Cat-Dev.labeled"

# Open the input file after obtaining its path.
input_dev_read = open(input_dev_path, "r")

# Read the input file data
list_of_all_dev_inputs = input_dev_read.readlines()

# A list that contains attribute values only.
attribute_values_list_dev = [' '.join(word for word in list_of_dev_inputs.split()
                  if word.lower() not in attribute_names_set)
         for list_of_dev_inputs in list_of_all_dev_inputs]

# Initialise the list that stores the lists of attribute values.
attr_values_dev_list_of_lists = []

# Append all the attribute values of a single row list into list of lists
for every_values in attribute_values_list_dev:
    items = every_values.split()
    attr_values_dev_list_of_lists.append(items)

dev_list = np.array(attr_values_dev_list_of_lists)
test_hypothesis = np.array(hypothesis)
correct = 0.0
incorrect = 0.0

for each_attribute_list in dev_list:
    if (each_attribute_list[:-1][test_hypothesis != '?'] ==  test_hypothesis[test_hypothesis != '?']).all():
        if each_attribute_list[-1].lower() == "high":
            correct = correct + 1.0
        else:
            incorrect = incorrect + 1.0
    else:
        if each_attribute_list[-1].lower() == "low":
            correct = correct + 1.0
        else:
            incorrect = incorrect + 1.0

misclassification = float(incorrect/(correct+incorrect))
sys.stdout.write("\n%s" % misclassification)

# Assign the path of the input file to a variable.
input_test_path = sys.argv[1]

# Open the input file after obtaining its path.
input_test_read = open(input_test_path, "r")

# Read the input file data
list_of_all_test_inputs = input_test_read.readlines()

# A list that contains attribute values only.
attribute_values_list_test = [' '.join(word for word in list_of_test_inputs.split()
                  if word.lower() not in attribute_names_set)
         for list_of_test_inputs in list_of_all_test_inputs]

# Initialise the list that stores the lists of attribute values.
attr_values_test_list_of_lists = []

# Append all the attribute values of a single row list into list of lists
for every_values in attribute_values_list_test:
    items = every_values.split()
    attr_values_test_list_of_lists.append(items)

test_list = np.array(attr_values_test_list_of_lists)

for each_attribute_list in test_list:
    sys.stdout.write("\n")
    if (each_attribute_list[:-1][test_hypothesis != '?'] ==  test_hypothesis[test_hypothesis != '?']).all():
        sys.stdout.write("high")
    else:
        sys.stdout.write("low")

