from  graphIO import *
from basicgraphs import graph
import time
import bisect
from Ex1_makegraphs import disjointunion


step_counter = 0


def compare(x):
	start_time = time.clock()
	graph_list = x[0]

	disjoint_union = graph_list[0]
	graph_ranges = list()
	graph_ranges.append(tuple([0, len(graph_list[0].V())]))

	for g in graph_list[1::]:
		graph_ranges.append(tuple([len(disjoint_union.V()), len(disjoint_union.V())+len(g.V())]))
		print('disjoint union of total and', graph_list.index(g))
		disjoint_union = disjointunion(disjoint_union, g)

	disjoint_union.init_colordict()

	start_time2 = time.clock()
	fast_color_refine(disjoint_union)
	elapsed_time2 = time.clock() - start_time2
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
					isolist[h].append(h)
					isolist[k].append(k)
	print(isolist)
	elapsed_time = time.clock() - start_time
	print('Time elapsed without reading: {0:.4f} sec'.format(elapsed_time))


def insert(seq, keys, item, k):
	i = bisect.bisect_left(keys, k)  # determine where to insert item
	keys.insert(i, k)  # insert key of item in keys list
	seq.insert(i, item)  # insert the item itself in the corresponding spot


def fast_color_refine(G):
	colordict = G.get_colordict()
	shortest_color_length = len(G.V())
	shortest_color = 0
	for color in colordict.keys():
		if color > 0:
			if len(colordict[color]) <= shortest_color_length:
				shortest_color = color
				shortest_color_length = len(colordict[color])
	queue = [shortest_color]
	i = 0
	newcolor = max(colordict.keys()) + 1
	while i < len(queue):
		incoming_nodes_dict = dict()
		for node in colordict[queue[i]]:
			for nb in node.get_nbs():
				color = nb.colornum
				if color not in incoming_nodes_dict:
					incoming_nodes_dict[color] = [nb]
				elif nb not in incoming_nodes_dict[color]:
					incoming_nodes_dict[color].append(nb)
		for color in incoming_nodes_dict.keys():
			nodes = incoming_nodes_dict[color]
			nodes.sort(key=lambda vertex: vertex.get_label())
			if not nodes == colordict[color]:
				if len(nodes) > len(colordict[color]) and color not in queue:
					queue.append(color)
				else:
					queue.append(newcolor)
				for node in nodes:
					G.update_colordict_fast(node, newcolor)
				newcolor += 1
		i += 1
	return G.get_colordict()


# def color_refine(G):
# 	colordict = G.get_colordict()
# 	not_done = True
# 	newcolor = max(colordict.keys()) + 1
#
# 	while not_done:
# 		newcolordict = dict()
# 		adjustdict = dict()
# 		for color in colordict.keys():
# 			vertices = colordict[color]
# 			neighbours = tuple(get_nb_colors(vertices[0]))
# 			newcolordict[color] = [vertices[0]]
# 			adjusted = False
# 			for vertex in vertices[1::]:
# 				nbcolors = tuple(get_nb_colors(vertex))
# 				if nbcolors == neighbours:
# 					newcolordict[vertex.colornum].append(vertex)
# 				else:
# 					if newcolor in newcolordict:
# 						newcolordict[newcolor].append(vertex)
# 					else:
# 						newcolordict[newcolor] = [vertex]
# 						adjusted = True
# 					adjustdict[vertex] = newcolor
# 			if adjusted:
# 				newcolor += 1
# 		if newcolordict == colordict:
# 			not_done = False
# 		for v in adjustdict.keys():
# 			G.update_colordict(v, adjustdict[v])
# 		colordict = newcolordict.copy()
# 		global step_counter
# 		step_counter += 1
# 	return colordict


def get_nb_colors(v):
	return sorted(n.colornum for n in v.get_nbs())


def count_isomorphisms(G):
	finaldict = fast_color_refine(G)
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


def sort_label_array(array):
	label_array = []
	for n in array:
		label_array.append(n.get_label())
	label_array = sorted(label_array)
	final_array = [0 for x in range(len(label_array))]
	for i in array:
		final_array[label_array.index(i.get_label())] = i
	return final_array


def update_graph(G, x, y):
	newcolor = max(G.get_colordict().keys()) + 1
	G.update_colordict(G.V()[x], newcolor)
	G.update_colordict(G.V()[y], newcolor)

start_time = time.clock()
compare(loadgraph("GI_march4/products216.grl", readlist=True))
# compare(loadgraph("benchmark/threepaths10240.gr", readlist=True))
# compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=True))
elapsed_time = time.clock() - start_time
print('Time elapsed with reading: {0:.4f} sec'.format(elapsed_time))
