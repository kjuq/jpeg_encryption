import random

for _y in range(4):
    for _x in range(4):
        print(str(random.randrange(256)).zfill(3), end='')
    print('')
