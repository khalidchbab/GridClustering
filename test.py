from random import randrange
import numpy as np
k = 0.3
f = 0.1

pr=(k/(k+f))**2

print(pr)
ones =[]
pr_i = 1-pr
for i in range(20000):
    r = np.random.choice(np.array([1,0]), p=[pr,pr_i])
    if r == 1:
        ones.append(r)

print(len(ones)/20000)