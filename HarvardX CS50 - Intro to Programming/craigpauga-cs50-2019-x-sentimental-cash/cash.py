# Craig Pauga
# CS50 Cash
# Yer

from cs50 import get_float


def main():

    # first ask
    cash = get_float("Change Owed:")

    # while user does not obey master
    while cash < 0:
        cash = get_float("Change Owed:")

    # Initialize Count
    count = 0

    # multiple by 100
    cash = cash * 100

    # greedy algorithm
    while cash > 0:

        # Take a quarter
        if cash >= 25:
            cash -= 25
            count += 1

        # Take a dime
        elif (cash < 25 and cash >= 10):
            cash -= 10
            count += 1

        # Take a nickel
        elif (cash < 10 and cash >= 5):
            cash -= 5
            count += 1

        # Take a penny
        else:
            cash -= 1
            count += 1

    # Print answer
    print(count)


if __name__ == '__main__':
    main()