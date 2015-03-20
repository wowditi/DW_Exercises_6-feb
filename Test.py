__author__ = 'Mark'

from graphIO import *
from Ex1_makegraphs import disjointunion
import time


step_counter = 0


def compare(x):
	starter_time = time.clock()
	graph_list = x[0]

	disjoint_union = graph_list[0]
	graph_ranges = list()
	graph_ranges.append(tuple([0, len(graph_list[0].V())]))

	for g in graph_list[1::]:
		graph_ranges.append(tuple([len(disjoint_union.V()), len(disjoint_union.V())+len(g.V())]))
		print('disjoint union of total and', graph_list.index(g))
		disjoint_union = disjointunion(disjoint_union, g)

	disjoint_union.init_colordict()

	starter_time2 = time.clock()
	fast_color_refine(disjoint_union)
	elapsed_time2 = time.clock() - starter_time2
	print('Time elapsed fast refine: {0:.4f} sec'.format(elapsed_time2))

	array = []
	for vertex in disjoint_union.V():
		array.append(vertex.colornum)
	result = []
	for n in graph_ranges:
		result.append(sorted(array[n[0]:n[1]:]))

	isolist = dict()
	for i in range(len(result)):
		isolist[i] = []
	for i in range(len(result)):
		if len(isolist[i]) == 0:
			for j in range(i+1, len(result)):
				if len(isolist[j]) == 0 and result[i] == result[j]:
					sort = sorted(result[i])
					isomorph = True

					for k in range(1, len(sort)):
						if sort[k] == sort[k-1]:
							isomorph = False
							break
					if isomorph:
						print(i, 'and', j, 'are isomorph')
						isolist[i].append(j)
						isolist[j].append(i)
					else:
						print(i, 'and', j, 'are undecided')
						union = disjointunion(graph_list[i], graph_list[j])
						union.init_colordict()
						count = count_isomorphisms(union)
						if count > 0:
							isolist[i].append(j)
							isolist[j].append(i)
						print('count = ', count)
		if len(isolist[i]) > 1:
			for h in range(len(isolist[i])):
				for k in range(h+1, len(isolist[i])):
					isolist[h].append(k)
					isolist[k].append(h)
	print(isolist)
	elapsed2_time = time.clock() - starter_time
	print('Time elapsed without reading: {0:.4f} sec'.format(elapsed2_time))


def insert(seq, keys, item, k):
	i = bisect.bisect_left(keys, k)  # determine where to insert item
	keys.insert(i, k)  # insert key of item in keys list
	seq.insert(i, item)  # insert the item itself in the corresponding spot


def color_refine(_l, colordict):
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


def count_isomorphisms(G):
	finaldict = fast_color_refine(G)
	isomorph = True
	colorclass = []
	for color in finaldict.keys():
		length = len(finaldict[color])
		if length >= 4:
			colorlen = len(colorclass)
			if colorlen == 0:
				colorclass = finaldict[color]
				isomorph = False
			elif length <= colorlen:
				colorclass = finaldict[color]
				isomorph = False
		if length % 2 == 1:
			return 0
	if isomorph:
		return 1
	else:
		nodes = G.V()
		dictionary = dict()
		for node in nodes:
			dictionary[node] = node.colornum
		colorclass.sort(key=lambda vertex: vertex.get_label())
		x = colorclass[0]
		num = 0
		for y in colorclass[int(len(colorclass)/2)::]:
			for node in nodes:
				G.update_colordict(node, dictionary[node])
			update_graph(G, G.V().index(x), G.V().index(y))
			num += count_isomorphisms(G)
		return num


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

