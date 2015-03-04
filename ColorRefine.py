from  graphIO import *
from basicgraphs import graph
import time
import copy
from Ex1_makegraphs import disjointunion


def compare(x):
	_l = x[0]

	graphs = copy.deepcopy(_l[0])
	nodes = list()
	nodes.append(tuple([0, len(_l[0].V())]))

	for g in _l[1::]:
		nodes.append(tuple([len(graphs.V()), len(graphs.V())+len(g.V())]))
		print('disjoint union of total and', _l.index(g))
		graphs = disjointunion(graphs, g)
		# graphs.addGraph(copy.deepcopy(g.E()), copy.deepcopy(g.V()))

	start_time = time.clock()

	graphs.init_colordict()
	colordict = prepare_graph(graphs)
	finaldict = color_refine(graphs, colordict)

	elapsed_time = time.clock() - start_time
	print('Time elapsed: {0:.4f} sec'.format(elapsed_time))

	array = []
	for i in range(len(graphs.V())):
		array.append(graphs.V()[i].colornum)
	result = []
	for n in nodes:
		result.append(sorted(array[n[0]:n[1]:]))
		# for i in range(len(graphs.V()[n[0]:n[1]:])):
		# 	_l[nodes.index(n)].V()[i] =

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
					disjointunition = copy.deepcopy(_l[i])
					disjointunition.addGraph(copy.deepcopy(_l[j].E()), copy.deepcopy(_l[j].V()))
					disjointunition.init_colordict()
					print('count = ', count_isomorphisms(disjointunition))


def count_isomorphisms(G):
	colordict = G.get_colordict()
	# print('skjdsl', colordict)
	finaldict = color_refine(G, colordict)
	isomorph = True
	colorclass = {}
	for color in finaldict.keys():
		if len(finaldict[color]) >= 4:
			colorclass = finaldict[color]
			isomorph = False
		if len(finaldict[color])%2 == 1:
			return 0
	if isomorph:
		return 1
	else:
		colorclass = sort_label_array(colorclass)
		x = colorclass[0]
		num = 0
		# print(x.colornum)
		for y in colorclass[int(len(colorclass)/2)::]:
			deepG = copy.deepcopy(G)
			# print(G.V())
			update_graph(deepG, G.V().index(x), G.V().index(y))
			num += count_isomorphisms(deepG)
		return num


def sort_label_array(array):
	label_array = []
	for n in array:
		label_array.append(n.get_label())
	label_array = sorted(label_array)
	final_array = [0 for x in range(len(label_array))]
	for i in array:
		final_array[label_array.index(i.get_label())] = i
	return final_array


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

#update_colordict(self, oldcolor, newcolor, i):
def update_graph(G, x, y):
	newcolor = max(G.get_colordict().keys()) + 1
	G.update_colordict(G.V()[x].colornum, newcolor, x)
	G.update_colordict(G.V()[y].colornum, newcolor, y)


def color_refine(G, colordict):
	not_done = True
	newcolor = max(colordict.keys()) + 1

	while not_done:
		newcolordict = dict()
		adjustdict = dict()
		for color in colordict.keys():
			vertices = colordict[color]
			neighbours = tuple(get_nb_colors(vertices[0]))
			newcolordict[color] = [vertices[0]]
			adjusted = False
			for vertex in vertices[1::]:
				nbcolors = tuple(get_nb_colors(vertex))
				if nbcolors == neighbours:
					newcolordict[vertex.colornum].append(vertex)
				else:
					if newcolor in newcolordict:
						newcolordict[newcolor].append(vertex)
					else:
						newcolordict[newcolor] = [vertex]
						adjusted = True
					adjustdict[vertex] = newcolor
			if adjusted:
				newcolor += 1
		if newcolordict == colordict:
			not_done = False
		for v in adjustdict.keys():
			G.update_colordict(v.colornum, adjustdict[v], G.V().index(v))
		colordict = newcolordict.copy()
	return colordict

compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=True))