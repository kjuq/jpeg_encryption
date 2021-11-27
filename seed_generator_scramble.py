import random

random.seed(1234)

perm = [str(i).zfill(3) for i in range(256)]
random.shuffle(perm)

print(*perm, sep='')
