# -*- coding: utf-8 -*-
"""
Created on Wed Aug 4

@author: sinanozdemir
adapted from https://www.wakari.io/sharing/bundle/nkorf/MapReduce%20Example
"""

# this function should turn a string into a list of (word, 1)
def mapper(line):
    result = []
    # remove leading and trailing whitespace
    line = line.strip()
    # remove odd symbols from the text
    words = line.split(" ")
    # insert the cleaned words into the results list
    for word in words:
        result.append((word, 1))
    return result
    # output is a list of (key, value) pairs

mapper("Hi everyone Hi Hi")
# [('Hi', 1), ('everyone', 1), ('Hi', 1), ('Hi', 1)]
# note that duplicates are expected
   
   

# the shuffle function gathers up the like key words
# once it gathers them up, it calls the reduce function!
# I have sorted everything by key for you
# run through the words one by one and create a dictionary
# where the word is the key and the value is the total count
# this is essentially a rehashed Counter but our own :)
def reducer(words):
    # sorting the words
    sorted_keys = sorted(words)
    tmp = ""
    value = ''
    for i in sorted_keys:
        if i[0] != tmp or tmp == "":  # saw a new word!
            print tmp, value
            value = 1
            tmp = i[0]
        else:
            value += 1
    print tmp, value
reducer([('Hi', 1), ('everyone', 1), ('Hi', 1), ('Hi', 1), ('sinan', 1), ('sinan', 1)])

    
sentences = ['hello big data big big big data ',
             'big data is the best',
             'big data is the best data big',
             'hello big data how are data',
             'big big big data',
             'data data big big']
# list of sentences to analyze   

# get the first sentence
first_sentence = sentences[0]

# map the first sentence
mapper(first_sentence)

#send the mapped sequence to the mapper/reducer
reducer(mapper(first_sentence))


# now do it for all of the sentences one by one
output_map =[]
for sentence in sentences:
    output_map +=mapper(sentence)

# total (key: value) pairs in one list
output_map

# call the shuffle function, which also calls the reduce function
reducer(output_map)


