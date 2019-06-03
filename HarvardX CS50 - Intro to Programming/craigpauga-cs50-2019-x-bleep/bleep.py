from cs50 import get_string
from sys import argv


def main():

    # Make sure user inputs correctly
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    # Initialize set of banned wordss
    banned = set()

    # Read lines of banned words
    lines = open(argv[1]).readlines()

    # Add each line to banned set
    for line in lines:
        banned.add(line.strip())

    # Ask user for message
    message = input("What message would you in to censor?\n")

    # Create list of words from message
    words = message.strip().split()

    # Iterate over list of words
    for j, word in enumerate(words):

        bleep = ''
        # Change to lower case
        word = word.lower()

        # If banned word in list
        if word in banned:

            # Repalce all chars with *
            for i in range(len(word)):
                bleep = bleep + '*'

            words[j] = bleep

    # Print redacted messaage
    print(' '.join(words))


if __name__ == "__main__":
    main()
