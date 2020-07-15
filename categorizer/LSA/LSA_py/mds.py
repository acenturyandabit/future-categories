import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA

import csv

f=open("output.csv")
reader=csv.reader(f)
data=list(reader)

similarities=np.zeros((len(data),len(data)))

for ii,i in enumerate(data):
    for ij,j in enumerate(data):
        closeness=0
        for u in range(len(j)):
            try:
                closeness+=float(i[u])*float(j[u])
            except Exception:
                pass
        similarities[ii][ij]=closeness
        #print(closeness)

print("sims done")

mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9,
                   dissimilarity="precomputed", n_jobs=1)
pos = mds.fit(similarities).embedding_

# Rotate the data
clf = PCA(n_components=2)

pos = clf.fit_transform(pos)

fig = plt.figure(1)
ax = plt.axes([0., 0., 1., 1.])

s = 100
plt.scatter(pos[:, 0], pos[:, 1], color='turquoise', s=s, lw=0, label='MDS')
plt.legend(scatterpoints=1, loc='best', shadow=False)
plt.show()