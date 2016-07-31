import sys

# Assign the path of the text document to a variable.
text_doc_path = sys.argv[1]

# Open the text document after obtaining its path.
text_doc_read = open(text_doc_path, "r")

# Assign the read text from the document to a list.
# Convert the words to lower case and split the words by " "
list_of_all_words = text_doc_read.read().lower().split()

# Now, sort the list of all words in reverse order.
list_of_all_words = sorted(list_of_all_words, reverse=True)

# Initialise a set() to store repetitive words 
# and a list[] to store the unique words 
repeting_words = set()
unique_words = []

# Filter the repeating words from list of all words.
for word in list_of_all_words:
    if word not in repeting_words:
        unique_words.append(word)
        repeting_words.add(word)

#print every unique word from the list of words
sys.stdout.write(",".join(unique_words))
sys.stdout.flush()
