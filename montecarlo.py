import numpy as np

N   = 900
pts = np.random.random((N,2))

# Select the points according to your condition
idx = (pts**2).sum(axis=1)  < 1.0
print pts[idx], idx.sum()
