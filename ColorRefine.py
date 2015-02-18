from  graphIO import *
from basicgraphs import graph


def sortlist(_l):
	array = [len(_l)+1]
	for i in range(len(_l)-1):
		array[i] = [len(_l[i].V()), len(_l[i].E())]
	returnarray = [[] for x in range(len(_l))]
	print(array)
	for i in range(len(array)-1):
		for g in array:
			if g[0] == array[i][0] and g[1] == array[i][1]:
				returnarray[i].append(_l[i].V())
	print(returnarray)

G = loadgraph('examplegraph.gr')
H = loadgraph('examplegraph2.gr')
blaat = [G, H]


def colorrefine(_l):
	degarray = [[] for x in range(len(_l[0].V()))]
	for elem in _l:
		for v in elem.V():
			print(v.deg())
			v.colornum = v.deg()
			degarray[v.deg()].append(v)
	i = 0
	print(degarray)
	notfinished = True

colorrefine(blaat)