import os
import pickle
import numpy as np
import sys

for root, dirnames, filenames in os.walk(sys.argv[1]):
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


