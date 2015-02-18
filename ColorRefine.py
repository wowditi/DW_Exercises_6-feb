from  graphIO import *
from basicgraphs import graph


def sortlist(_l):
	array = []
	for i in range(len(_l)):
		array.append([len(_l[i].V()), len(_l[i].E())])
	print(array)
	returnarray = []
	i = 0
	temp = 1
	while i < len(array)-1: #for i in range(len(array)-1):
		temparray = []
		temparray.append(_l[i])
		for g in range(i+1,len(array)):
			if array[g][0] == array[i][0] and array[g][1] == array[i][1]:
				temparray.append(_l[g])
				temp += 1
		returnarray.append(temparray)
		i += temp
		temp = 0
	print(returnarray)

G = loadgraph('examplegraph.gr')
H = loadgraph('examplegraph.gr')
J = loadgraph('examplegraph.gr')
T = loadgraph('examplegraph2.gr')
Q = loadgraph('examplegraph2.gr')

blaat = [G, H, J, T, Q]
print(sortlist(blaat))


def colorrefine(_l):
	for elem in _l:
		for v in elem.V():
			v.colornum = v.deg()
	i = 0
	notfinished = True
	while notfinished:
		i += 1
