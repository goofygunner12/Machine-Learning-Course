import sys
import collections

# Assign the path of the text document to a variable.
text_doc_path = sys.argv[1]

# Open the text document after obtaining its path.
text_doc_read = open(text_doc_path, "r")

# Assign the read text from the document to a list.
# Convert the words to lower case and split the words by " "
list_of_all_words = text_doc_read.read().lower().split()

# Initialise a set() to store repetitive words 
# and a list[] to store the count of occurance(s) of a word
repeting_words = set()
word_counter_list = []

# Form a string of key-value pair
# i.e word and word count pair as a string
for word in list_of_all_words:
    if word not in repeting_words:
        repeting_words.add(word)
        key_value_pair = word + ":" + str(list_of_all_words.count(word))
        word_counter_list.append(key_value_pair)
    
# Now, sort the list of all words in reverse order.
word_counter_list = sorted(word_counter_list, reverse=True)

#print every word and its occurance count from the list of words
sys.stdout.write(",".join(word_counter_list))
sys.stdout.flush()
