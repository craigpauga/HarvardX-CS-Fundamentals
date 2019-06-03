#Craig Pauga
#CS50 Alright!

from nltk.tokenize import sent_tokenize

def lines(a, b):

    # Split the strings by new line
    a_lines = a.split('\n')
    b_lines = b.split('\n')

    # Initialize new set
    similarities = set()

    # iterate over each line
    for a_line in a_lines:
        for b_line in b_lines:
            if a_line.rstrip() == b_line.rstrip():
                similarities.add(a_line)
    return similarities


def sentences(a, b):

    #Split the string by sentence
    a_sents = sent_tokenize(a)
    b_sents = sent_tokenize(b)

    # Initilize  set
    similarities = set()

    # iterate over each line
    for a_sent in a_sents:
        for b_sent in b_sents:
            if a_sent.rstrip() == b_sent.rstrip():
                similarities.add(a_sent)
    return similarities


def substrings(a, b, n):

    # Initilize  set
    similarities = set()

    # Return zero if sub is large
    if n > len(a) or n > len(b):
        return similarities

    # Iterate over length
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i:i+n] == b[j:j+n]:
                similarities.add(b[j:j+n])
    return similarities
