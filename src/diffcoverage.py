from scipy.spatial import distance
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def getcoveragefile(logfile_list):
    init_covs = []
    target_covs = []
    for logfile in logfile_list:
        for line in open(logfile):
            if 'init' in line:
                initdir = line.strip().split()[-1]
                init_covs.append(os.path.join(initdir, 'covsummary.npy'))
            if 'Directory:' in line and 'Target:' in line and 'no_swarm' in line:
                lparts = line.split()
                for part in lparts:
                    if part.startswith('Directory'):
                        directory = part.replace('Directory:', '')
                        covfile = os.path.join(directory, 'covsummary.npy')
                        target_covs.append(covfile)
    return {'30minlist': init_covs,
            '10minlist': target_covs}


'''
print target_covs
print init_covs
'''
def tobinary(n):
    if n > 0:
        return 1
    else:
        return 0

def normalize(arr):
    return arr/arr.max()
#    vfunct = np.vectorize(tobinary)
#    return vfunct(arr)
#    return (arr - arr.mean())/(arr.max() - arr.min())

def heatmap(arr, labels):
    newlabels = []
    for l in labels:
        print l
        if 'init' in l:
            newlabels.append('Swarm')
        else:
            lparts = l.split('/')
#           newlabels.append('{0}.{1}.{2}'.format(lparts[-2], lparts[-3], lparts[-4]))
            newlabels.append('Targeted'.format(lparts[-2], lparts[-3], lparts[-4]))
    plt.figure(figsize=(2,6))
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(arr, cmap=plt.cm.Blues, vmin=0, vmax=1, alpha=0.9)
    ax.set_xlabel("Lines")
    ax.set_ylabel("Test Suites")

    ax.set_yticks(np.arange(len(labels))+0.5)
    ax.set_yticklabels(newlabels, minor=False)
    fig = plt.gcf()
#    ax.grid(False)
    ax = plt.gca()
    plt.savefig('heatmap.png',dpi=600)
    plt.close()
    
    


def concatarrays(covfiles):
    firsttime = True
    labels = []
    for c in  covfiles:
	try:
            if firsttime:
		arr = np.load(c)
		arr = normalize(arr)
                firsttime = False
            else:
                temparr = normalize(np.load(c))
                arr = np.vstack((arr, temparr))
            labels.append(c)
	except ValueError:
		print 'Value Error {0}'.format(c)
		pass
        except IOError:
		print 'IOExcepion {0}'.format(c)
		pass

    print arr.shape,  len(labels)
#    arr2 = np.transpose(arr)
#    arr = arr2[np.sum(arr2, axis=1) > 0]
#    arr = np.transpose(arr)
#    print arr.shape
#    print arr[np.sum(arr, axis=1) > 0] #, type(arr[arr[:,1]])
    heatmap(arr, labels)


import random
logfile_list =  glob.glob(sys.argv[1])
cc = getcoveragefile(logfile_list)
concatarrays(cc['30minlist'] + random.sample(cc['10minlist'],5))


exit(0)

# print len(initts)	

for i, arr1 in enumerate(initts):
	for arr2 in initts[i+1:]:
		pass #		print distance.braycurtis(arr1, arr2)



# exit()

targetts = []
for c in  target_covs:
	try:
		arr = np.load(c)
		arr = arr/np.max(arr)
		targetts.append(arr)
	except Exception:
		# print 'Cannot open {0}'.format(c)
		pass

#targetts += initts

for i, arr1 in enumerate(targetts):
	for arr2 in targetts[i+1:]:
		print distance.braycurtis(arr1, arr2)


