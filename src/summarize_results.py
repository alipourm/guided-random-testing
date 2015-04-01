import os
import pickle
import numpy as np
import pandas as pd
import sys


def dumpnpyfiles(dir):
  for root, dirnames, filenames in os.walk(dir):
    linecov= np.array([])
    branchcov = np.array([])
    functioncov = np.array([])
    numinf = np.array([0]) # for the sake of uniformity
    for f in filenames:
        if f.endswith('.js'):
            f = os.path.join(root, f)
            print f
            try:
                lcov = np.array(pickle.load(open(f + '.lcov')))
                bcov = np.array(pickle.load(open(f + '.bcov')))
                fcov = np.array(pickle.load(open(f + '.fcov')))
                if linecov.size == 0:
                    linecov = lcov
                else:
                    linecov += lcov

                if branchcov.size == 0:
                    branchcov = bcov
                else:
                    branchcov += bcov

                if functioncov.size == 0:
                    functioncov = fcov
                else:
                    functioncov = np.union1d(functioncov, fcov)

            except IOError:
                print 'IOError:', f
                numinf += 1
    np.save(os.path.join(root, 'linecov'), linecov)
    np.save(os.path.join(root, 'branchcov'), branchcov)
    np.save(os.path.join(root, 'functioncov'), functioncov)
    np.save(os.path.join(root, 'numinf'), numinf)


def gathernypfiles(dir):
	coverage = {}
	for root, dirs, filenames in os.walk(dir):
		if 'linecov.npy' in filenames:
			data = {}
			covs = [f for f in filenames if f.endswith('.npy')]
			for c in covs:
				print c
				data[c] = ''.join(map(lambda n: str(n), np.load(os.path.join(root, c)).tolist()))
			coverage[root] = data
	return pd.DataFrame(coverage)

df = gathernypfiles(sys.argv[1])
df.to_csv('goodsummary.csv')
