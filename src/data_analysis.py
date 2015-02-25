import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt


df = pd.DataFrame.from_csv("data.csv")
relations =[k for k in df.columns if '_relation'in k]
fst = lambda (x,y):x
snd = lambda (x,y):y
tonum = lambda s: int(re.findall("\d+", s)[0])

def compose(f,g):
  return lambda x: f(g(x))



def sort_list(l):
  x = map(compose(tonum, fst), l)
  y = map(snd, l)
  xy = zip(x, y)
  return sorted(xy, key=fst)

def getX(l):
  return np.array(map(fst, l))

def getY(l):
  return np.array(map(snd, l))



suppress_dist = sort_list([(r, len(df[df[r] == 'S'])) for r in relations])
trigger_dist = sort_list([(r, len(df[df[r] == 'T'])) for r in relations])



plt.figure()
width = 0.5
fig, ax = plt.subplots()
rec1 = ax.bar(getX(trigger_dist),getY(trigger_dist), width, color='r')
rec2 = ax.bar(getX(suppress_dist)+width,getY(suppress_dist), width, color='b')
ax.set_ylabel('Number of Targets')
ax.set_xticks(getX(trigger_dist)+width)
ax.set_xticklabels(getX(trigger_dist))
plt.show()
