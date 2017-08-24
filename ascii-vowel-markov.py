# Code to encode ASCII strings as English words
# By Hannah Newman <HN860433@wcupa.edu>

import random

# input: a text string
# output: binary stored as a string with letters replaced with either 1 or 0
def word_to_bin(string):
    # string is converted to lowercase since uppercase and lowercase letters are equivalent
    string = string.lower()
    # binary is stored as string to conserve leading zeroes
    binary = ""
    for letter in string:
        if is_zero(letter):
            binary += "0"
        else:
            binary += "1"
    return binary

# input: an ASCII string
# output: each character's ASCII index in 8 bits, as a string
def str_to_bin(string):
    binary = ""
    for char in string:
        binary += str(format(ord(char), "b")).zfill(8) # adds leading zeroes until length 8
    return binary

# input: a character
# output: whether or not the letter should be replaced with 0
def is_zero(letter):
    return letter in "aeiouy"

# get lines from a file
word_file = open("corpus.txt")
lines = word_file.readlines()
word_file.close()

# remove trailing whitespace from each line
lines = [line.rstrip() for line in lines]

# make a list of all space-delimited words in order of appearance
words = []
for line in lines:
    words += line.split(" ")


# keys: words in the text
# values: dicts of binary values and words which encode them
# (subdict keys: binary values stored as strings)
# (subdict values: the strings which represent these binary strings)
markov = dict()

# initializes current maximum length
maxlen = len(words[0])

# initializes most recent word processed
last_word = ""

# adds words to the dict markov
for word in words:
    # finds actual maximum length
    if len(word) > maxlen:
        maxlen = len(word)
    # if key not in dict, initialize it
    if last_word not in markov:
        markov[last_word] = dict()
    # adds word to the subdict under the correct binary value
    if word_to_bin(word) not in markov[last_word]:
        markov[last_word][word_to_bin(word)] = [word]
    else:
        markov[last_word][word_to_bin(word)] += [word]
    if word_to_bin(word) not in markov[""]:
        markov[""][word_to_bin(word)] = [word]
    else:
        markov[""][word_to_bin(word)] += [word]
    # updates word we are working with
    last_word = word


# input: plaintext ASCII string
# output: ciphertext matching the ASCII
def binary_encode(string):
    sbin = str_to_bin(string)
    result = ""
    last_word = markov.keys()[random.randint(0,len(markov.keys())-1)]
    # if string is empty, translation is done
    while sbin != "":
        # the length of words to start trying is either the length of the longest word,
        # or the length of the string being encoded, whichever is shorter
        length = min(maxlen, len(sbin))
        # this loop tries lengths from longest to shortest
        while length > 0:
            # if there's a matching string of binary, use a word corresponding to it
            if sbin[:length] in markov[last_word]:
                substring = sbin[:length]
                # adds random word from list of acceptable ones
                idx = random.randint(0, len(markov[last_word][substring]) - 1)
                word = markov[last_word][substring][idx]
                # add the found word to the result string
                result += word + " "
                # update most recent word used and remaining string to translate
                sbin = sbin[length:]
                # if we've found a word, break the inner while loop
                last_word = word
                break
            # if there is no match, decrement length and try again
            length -= 1
        if length == 0:
            # if there is no match for the word, reset it
            last_word = ""
            # (if there is no match for the word, change to a new random word)
            # this has a lower success rate than the above, usually, but makes it more interesting
            # comment in (and comment out the above) if desired
            # last_word = markov.keys()[random.randint(0, len(markov.keys()) - 1)]
    return result.rstrip()


# reverse conversion function
# input: ciphertext
# output: plaintext
def binary_decode(string):
    # remove spaces from the string
    string = string.replace(" ", "")
    string = word_to_bin(string)
    plaintext = ""
    # convert each group of 8 binary digits to a character and add to plaintext
    for i in range(0, len(string), 8):
        plaintext += chr(int(string[i:i+8], 2))
    return plaintext

# prints encoded version of user-input string
print binary_encode(raw_input("What text would you like to encode?\n>"))
