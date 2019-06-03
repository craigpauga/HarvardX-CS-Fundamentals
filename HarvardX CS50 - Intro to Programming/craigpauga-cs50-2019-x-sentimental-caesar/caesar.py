from sys import argv
from cs50 import get_string


def main():
    # Make sure that user puts in input
    if len(argv) != 2:
        print("Wrong Answer Peasant")
        exit(1)

    # Get key from input
    key = int(argv[1])

    # Get a string from user
    plaintext = get_string("plaintext:")

    # Initialize ciphertext array
    ciphertextarr = []
    ciphertext = ''

    # Enumerate through plaintext
    for c in plaintext:

        # Get ASCII Value
        n = ord(c) + key

        # Consider LowerCase
        if ord(c) >= ord('a') and ord(c) <= ord('z'):
            n = (n - ord('a')) % 26 + ord('a')

            # Change ASCII to char
            c = chr(n)
        # Consider UpperCase
        elif ord(c) >= ord('A') and ord(c) <= ord('Z'):
            n = (n - ord('A')) % 26 + ord('A')
            # Change ASCII to char
            c = chr(n)
        # Ignore all else
        else:
            c = c

        # Append and Create String
        # ciphertextarr.append(c)
        ciphertext = ciphertext + c

    #ciphertext = ''.join(ciphertextarr)

    # Print Answer
    print(f"ciphertext: {ciphertext}")


if __name__ == '__main__':
    main()