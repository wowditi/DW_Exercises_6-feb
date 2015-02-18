from  graphIO import *
from basicgraphs import graph


def sortlist(_l):
	array = []
	for i in range(len(_l)):
		array[i] = [len(_l[i].V()), len(_l[i].E())]
	returnarray = [[]]
	for i in range(array):
		for g in array:
			if g[0] == array[i][0] and g[1] == array[i][1]:
				returnarray[i] += _l[i]
	print(returnarray)

G = loadgraph('examplegraph.gr')
H = loadgraph('examplegraph2.gr')
blaat = [G, H]
print(sortlist(blaat))


def colorrefine(_l):
	for elem in _l:
		for v in elem.V():
			v.colornum = v.deg()
	i = 0
	notfinished = True
	while notfinished:
		i += 1
