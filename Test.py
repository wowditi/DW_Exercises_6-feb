__author__ = 'Mark'

from graphIO import *
from Ex1_makegraphs import disjointunion
from basicgraphs import graph


def refine(g):
	#initialize
	colordict = { }
	for v in g.V():
		v.colorNum = v.deg()
		if v.colorNum not in colordict:
			colordict[v.colorNum] = [v]
		else:
			colordict[v.colorNum].append(v)
	print(colordict)

	oldgraph = graph(0, g.E(), g.V())
	changed = True
	newcolor = max(colordict.keys()) + 1

	while changed:
		tempcolordict = colordict.copy()
		for key in tempcolordict.keys():
			buren = tuple()
			for value in tempcolordict.get(key):
				nc = sorted(tuple(getNeighbourColors(value)))
				if len(buren) == 0:
					buren = nc
				elif nc != buren:
					print('###', nc, '    ', buren)
					colordict[key].remove(value)
					# value.colorNum = newcolor
					# buren[nc] = newcolor
					if newcolor in colordict:
						colordict[newcolor].append(value)
					else:
						colordict[newcolor] = [value]
				else:
					print('---', nc, '    ', buren)
				# 	colordict[value.colorNum].remove(value)
				# 	# value.colorNum = buren[nc]
				# 	colordict[buren[nc]].append(value)
			print(colordict, '\n')
			newcolor = max(colordict.keys()) + 1
		for key in colordict:
			for value in colordict[key]:
				value.colorNum = key
		if tempcolordict == colordict:
			changed = False
			print(colordict)
	finalcolors = []
	for node in g.V():
		finalcolors.append(node.colorNum)

	return finalcolors


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.colorNum)
	return colors


def compare(x):
	graphs = x[0][0]
	for y in range(1, len(x[0])):
		graphs = disjointunion(graphs, x[0][y])
	writeDOT(graphs,'jemoeder.dot')
	writeDOT(x[0][0],'j3mo3d3r.dot')
	print(sorted(refine(graphs)))


def removeDuplicates(original):
	new = []
	for element in original:
		if not new.__contains__(element):
			new.append(element)
	return new


print(compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_9.grl", readlist=True)))