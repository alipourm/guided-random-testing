import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt


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

df = pd.DataFrame.from_csv("/scratch/projects/guided-random-testing/src/data.csv")
relations =[k for k in df.columns if '_relation'in k]


# suppress_dist = sort_list([(r, len(df[df[r] == 'S'])) for r in relations])
# trigger_dist = sort_list([(r, len(df[df[r] == 'T'])) for r in relations])
#
#
#
# plt.figure()
# width = 0.5
# fig, ax = plt.subplots()
# rec1 = ax.bar(getX(trigger_dist),getY(trigger_dist), width, color='r')
# rec2 = ax.bar(getX(suppress_dist)+width,getY(suppress_dist), width, color='b')
# ax.set_ylabel('Number of Targets')
# ax.set_xticks(getX(trigger_dist)+width)
# ax.set_xticklabels(getX(trigger_dist))
# plt.show()


def get_rels(l, r):
  return [i for i in l if i == r]

def count(l):
  I = get_rels(l,'I')
  S = get_rels(l,'S')
  T = get_rels(l,'T')
  return {'I':len(I),
          'S':len(S),
          'T':len(T)}

def agg_lines(df):
  lines = []
  for line in df:
    lines.append(line)
  return lines


x = []
y = []
df['lineno']= df.index.copy()
groups = df.groupby(relations)
gr = groups['cov'].agg({'average':np.mean, 'count': np.size})
# k = groups['lineno'].agg({'lines':agg_lines})
# print k
gr['TEMP']=gr.index.copy()
gr['I']= gr['TEMP'].apply(lambda row: count(row)['I'])
gr['T']= gr['TEMP'].apply(lambda row: count(row)['T'])
gr['S']= gr['TEMP'].apply(lambda row: count(row)['S'])
gr = gr[(gr['T'] + gr['S'] > 0) & (gr['average'] < 200) & (gr['I']>250)]

df2 = df.join(gr, how='right', on=gr.index.names)
df2.to_csv('/scratch/projects/guided-random-testing/src/joined.csv')
targets = df2[df2['T']==1][relations]
targets.to_csv('/scratch/projects/guided-random-testing/src/targets.csv')

# for g in gr.index:
#   print count(g)['I'], gr.loc[g]['count'], gr.loc[g]['average']
#   print gr.loc[g]['I']


plt.figure()
gr.plot(kind='scatter', x='average', y='count', c='I', s=267.)
plt.show()

#   x.append(str(g))

#   y.append(len(g))
#
# gr.to_csv('df.csv')
# plt.figure()
# fig, ax = plt.subplots()
# plt.bar(range(len(y)-1), y[1:], width=3)
# ax.set_xticklabels(x[1:])
# plt.show()