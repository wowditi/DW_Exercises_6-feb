__author__ = 'Mark'

from graphIO import *
from Ex1_makegraphs import disjointunion
import time


step_counter = 0


#360.3973 sec
# def refine_colors(_l):
# 	# Initialization
# 	colordict = {}  # dictionary with key=colornum and value=vertex array
# 	print('start refining')
# 	for v in _l.V():
# 		v.colornum = v.deg
# 		if v.colornum in colordict:
# 			colordict[v.colornum].append(v)
# 		else:
# 			colordict[v.colornum] = [v]
# 	print('initial')
#
# 	not_done = True
# 	newcolor = max(colordict.keys()) + 1
#
# 	while not_done:
# 		tempcolordict = dict()
# 		for key in colordict.keys():
# 			array = colordict[key]
# 			buren = tuple(get_nb_colors(array[0]))
# 			adjusted = False
# 			for value in array[1::]:
# 				nc = tuple(get_nb_colors(value))
# 				if nc != buren:
# 					tempcolordict[value] = tuple([value.colornum, newcolor])
# 					adjusted = True
# 			if adjusted:
# 				newcolor += 1
# 		if len(tempcolordict) == 0:
# 			not_done = False
# 		for value in tempcolordict:
# 			old = tempcolordict[value][0]
# 			new = tempcolordict[value][1]
# 			colordict[old].remove(value)
# 			value.colornum = new
# 			if new in colordict:
# 				colordict[new].append(value)
# 			else:
# 				colordict[new] = [value]
# 		print('step')
# 	finalcolors = []
# 	for node in _l.V():
# 		finalcolors.append(node.colornum)
#
# 	return finalcolors


def compare(x):
	_l = x[0]

	graphs = _l[0]
	nodes = list()
	nodes.append(tuple([0, len(_l[0].V())]))

	for g in _l[1::]:
		# nodes.append(tuple([len(graphs.V()), len(graphs.V())+len(g.V())]))
		# print('disjoint union of total and', _l.index(g))
		# graphs.addGraph(g.E(), g.V())
		nodes.append(tuple([len(graphs.V()), len(graphs.V())+len(g.V())]))
		print('disjoint union of total and', _l.index(g))
		graphs = disjointunion(graphs, g)

	start_time = time.clock()

	graphs.init_colordict()
	colordict = prepare_graph(graphs)
	efficient(graphs, colordict)

	elapsed_time = time.clock() - start_time
	print('Time elapsed: {0:.4f} sec'.format(elapsed_time))


	array = []
	for vertex in graphs.V():
		array.append(vertex.colornum)
	result = []
	for n in nodes:
		result.append(sorted(array[n[0]:n[1]:]))

	for i in range(len(result)):
		for j in range(i+1, len(result)):
			if result[i] == result[j]:
				sort = sorted(result[i])
				isomorph = True
				for k in range(1, len(sort)):
					if sort[k] == sort[k-1]:
						isomorph = False
						break
				if isomorph:
					print(i, 'and', j, 'are isomorph')
				else:
					print(i, 'and', j, 'are undecided')
	print('Steps: ', step_counter)


#306.2617 sec
def efficient(_l, colordict):
	not_done = True
	newcolor = max(colordict.keys()) + 1

	while not_done:
		tempcolordict = dict()
		temp = dict()
		for key in colordict.keys():
			array = colordict[key]
			buren = tuple(get_nb_colors(array[0]))
			tempcolordict[key] = [array[0]]
			adjusted = False
			for value in array[1::]:
				nc = tuple(get_nb_colors(value))
				if nc == buren:
					tempcolordict[value.colornum].append(value)
				else:
					if newcolor in tempcolordict:
						tempcolordict[newcolor].append(value)
					else:
						tempcolordict[newcolor] = [value]
						adjusted = True
					temp[value] = newcolor
			if adjusted:
				newcolor += 1
		if tempcolordict == colordict:
			not_done = False
		for v in temp.keys():
			_l.update_colordict(v.colornum, temp[v], _l.V().index(v))
			# v.colornum = temp[v]
		colordict = tempcolordict.copy()
		global step_counter
		step_counter += 1
		print(step_counter)
	# finalcolors = []
	# for node in _l.V():
	# 	finalcolors.append(node.colornum)
	return colordict


def get_nb_colors(v):
	return sorted(n.colornum for n in v.nbs)


def prepare_graph(G):
	colordict = {}

	for v in G.V():
		v.colornum = v.deg
		if v.colornum in colordict:
			colordict[v.colornum].append(v)
		else:
			colordict[v.colornum] = [v]
	return colordict







# Graph 6x7680
# Time elapsed: 724.3092 sec
# 0 and 1 are isomorph
# 2 and 3 are undecided
# 4 and 5 are isomorph

# compare(loadgraph("GI_march4/products72.grl", readlist=True))

