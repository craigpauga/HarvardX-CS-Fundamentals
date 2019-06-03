from sys import argv

# initialize height
height = input("Height?\n")

# continue until the user gives positive int
while (not height.isnumeric()) or int(height) <= 0 or int(height) >= 9:

    height = input("Height?\n")

# Loop through height
height = int(height)
for i in range(1, height+1):
    for j in range(1, height+1):
        if j > height - i:
            print("#", end='')
        else:
            print(" ", end='')
    print('')
