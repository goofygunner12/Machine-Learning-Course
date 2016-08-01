import sys
import math
import numpy as np

num_attributes = 4

# Calculate the input space value.
# |X| = No_of_attributes_of_x1 * ... * No_of_attributes_of_xn
# Since each attribute has two possible values, we use 2^num_attributes
input_space = int(math.pow(2, num_attributes))

# Calculate the concept space value. |C| = 2^|X|
concept_space = int(math.pow(2, input_space))

# Calculate the Hypothesis Space
hypothesis_space = concept_space

# Print the size of the input space
sys.stdout.write("%s\n" % input_space)

# Print the size of the hypothesis space
sys.stdout.write("%s\n" % hypothesis_space)

# Function to get binary value for a base 10 digit
get_binary_value = lambda x, n: format(x, 'b').zfill(n)

# the list of concept space (alos hypothesis space) is converted into list of binary values
list_n = []
for i in range(0, concept_space):
    item = get_binary_value(i, 16)
    list_n.append(item)

# list of binary values converted hypothesis space is converted into single char list of lists
i=0
new_list=[]
for i in range(0, len(list_n)):
    items = (map(int, str(list_n[i])))
    new_list.append(items)

# Initialise a set of attribute names and assign values.
# This set will be used to remove all the attribute names
# and keep the attribute values only from the inpute data.
attribute_names_set = {'gender', 'age', 'student?', 'previouslydeclined?', 'risk'}

# Assign the path of the input file to a variable.
input_train_path = "4Cat-Train.labeled"

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
items_new = []

# Append all the attribute values of a single row list into list of lists
for every_values in attribute_values_list:
    items = every_values.split()
    attr_values_list_of_lists.append(items)

for every_item_list in attr_values_list_of_lists:
    for every_item in every_item_list:
        if every_item == "Male" or every_item == "Young" or every_item == "Yes" :
            every_item = 1
        elif every_item == "Female" or every_item == "Old" or every_item == "No" :
            every_item = 0
        items_new.append(every_item)

# list of tuples. each tuple is training instance
attr_values_list_of_lists =  zip(*[iter(items_new)]*5)

#join function for attr_values_list_of_lists[]
concat_nums = lambda nums: int(''.join(str(i) for i in nums))

# loop that eliminates the those h(x) != c(x). Where h(x) is from the training data.
for every_attribute_row in attr_values_list_of_lists:
    j = concat_nums(every_attribute_row[:-1])
    k = int(str(j), 2)
    i = 0
    for every_row in new_list:
        if (every_attribute_row[-1] == "low" and new_list[i][k] != 0) or (every_attribute_row[-1] == "high" and new_list[i][k] != 1):
            new_list.pop(i)
            i = i - 1
        i = i + 1


for every_attribute_row in attr_values_list_of_lists:
    j = concat_nums(every_attribute_row[:-1])
    k = int(str(j), 2)
    i = 0
    for every_row in new_list:
        if (every_attribute_row[-1] == "low" and new_list[i][k] != 0) or (every_attribute_row[-1] == "high" and new_list[i][k] != 1):
            new_list.pop(i)
            i = i - 1
        i = i + 1


for every_attribute_row in attr_values_list_of_lists:
    j = concat_nums(every_attribute_row[:-1])
    k = int(str(j), 2)
    i = 0
    for every_row in new_list:
        if (every_attribute_row[-1] == "low" and new_list[i][k] != 0) or (every_attribute_row[-1] == "high" and new_list[i][k] != 1):
            new_list.pop(i)
            i = i - 1
        i = i + 1

# PartB(3) number of hypotheses in version space 
sys.stdout.write("%s" % len(new_list))


# Assign the path of the input file to a variable.
input_test_path =  sys.argv[1]
#input_test_path = "4Cat-Dev.labeled"

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
test_items = []
for every_item_list in attr_values_test_list_of_lists:
    for every_item in every_item_list:
        if every_item == "Male" or every_item == "Young" or every_item == "Yes" :
            every_item = 1
        elif every_item == "Female" or every_item == "Old" or every_item == "No" :
            every_item = 0
        test_items.append(every_item)

# list of tuples
attr_values_test_list_of_lists =  zip(*[iter(test_items)]*5)
for every_attribute_row in attr_values_test_list_of_lists:
    j = concat_nums(every_attribute_row[:-1])
    k = int(str(j), 2)
    i = 0
    high = 0
    low = 0
    for every_row in new_list:
        if every_attribute_row[-1] == "low" and new_list[i][k] == 0 :
            low = low + 1
        elif every_attribute_row[-1] == "low" and new_list[i][k] == 1 :
            high = high + 1
        elif every_attribute_row[-1] == "high" and new_list[i][k] == 1 :
            high = high + 1
        elif every_attribute_row[-1] == "high" and new_list[i][k] == 0 :
            low = low + 1
        i = i + 1
    sys.stdout.write("\n%s " % high)
    sys.stdout.write(" %s" % low)
