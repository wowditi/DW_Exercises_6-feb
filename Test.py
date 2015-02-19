__author__ = 'Mark'

from graphIO import *
from Ex1_makegraphs import disjointunion


def refine_colors(_l):
	# Initialization
	colordict = {}  # dictionary with key=colornum and value=vertex array
	print('start refining')
	o = 0
	for v in _l.V():
		v.colornum = v.deg
		if v.colornum not in colordict:
			colordict[v.colornum] = [v]
		else:
			colordict[v.colornum].append(v)
		o += 1
		print(o)
	print('initial')

	not_done = True
	newcolor = max(colordict.keys()) + 1

	while not_done:
		tempcolordict = dict()
		for key in colordict.keys():
			array = colordict[key]
			buren = tuple(get_nb_colors(array[0]))
			adjusted = False
			for value in array[1::]:
				nc = tuple(get_nb_colors(value))
				if nc != buren:
					tempcolordict[value] = tuple([value.colornum, newcolor])
					adjusted = True
			if adjusted:
				newcolor += 1
		if len(tempcolordict) == 0:
			not_done = False
		for value in tempcolordict:
			old = tempcolordict[value][0]
			new = tempcolordict[value][1]
			colordict[old].remove(value)
			value.colornum = new
			if new in colordict:
				colordict[new].append(value)
			else:
				colordict[new] = [value]
		print('step')
	finalcolors = []
	for node in _l.V():
		finalcolors.append(node.colornum)

	return finalcolors


def get_nb_colors(v):
	return sorted(n.colornum for n in v.nbs)


def compare(x):
	_l = x[0]
	graphs = _l[0]
	nodes = []
	nodes.append(tuple([0, len(_l[0].V())]))
	for g in _l[1::]:
		nodes.append(tuple([len(graphs.V()), len(graphs.V())+len(g.V())]))
		print('disjoint union of total and', _l.index(g))
		graphs = disjointunion(graphs, g)
	array = refine_colors(graphs)
	# print(array)
	result = []
	for n in nodes:
		result.append(sorted(array[n[0]:n[1]:]))
	for i in range(len(result)):
		for j in range(i+1, len(result)):
			if result[i] == result[j]:
				print(i, 'and', j, 'are isomorph')
	# print(result)


def efficient(_l):
	print('start refining')
	v_array = _l.V()
	n = len(v_array)
	array = [[] for i in range(n)]
	o = 0
	for v in range(n):
		vertex = v_array[v]
		# vertex.colornum = vertex.deg()
		array[v].append(vertex)
		o += 1
		print(o)
	print('initial')



compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_4098.grl", readlist=True))