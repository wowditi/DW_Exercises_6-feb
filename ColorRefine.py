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
	fast_color_refine(disjoint_union)

	elapsed_time = time.clock() - start_time
	print('Time elapsed: {0:.4f} sec'.format(elapsed_time))
	print('Steps: ', step_counter)

	array = []
	for vertex in disjoint_union.V():
		array.append(vertex.colornum)
	result = []
	for n in graph_ranges:
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
					union = disjointunion(graph_list[i], graph_list[j])
					union.init_colordict()
					print('count = ', count_isomorphisms(union))
	elapsed_time = time.clock() - start_time
	print('Time elapsed: {0:.4f} sec'.format(elapsed_time))
	print('Steps: ', step_counter)


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
		incoming_nodes = [[] for x in range (0,newcolor,1)]
		incoming_nodes_labels = [[] for x in range (0,newcolor,1)]
		for node in colordict[queue[i]]:
			for nb in node.get_nbs():
				if nb not in incoming_nodes[nb.colornum]:
					insert(incoming_nodes[nb.colornum], incoming_nodes_labels[nb.colornum], nb,nb.get_label())

		for nodes in incoming_nodes:
			index = incoming_nodes.index(nodes)
			if index in colordict.keys():
				# print(sorted(nodes,key=lambda vertex : vertex._label))
				# sorted(nodes, key=lambda vertex : vertex._label)
				# start_time = time.clock()
				# print(nodes)
				# nodes.sort(key=lambda vertex: vertex.get_label())
				# colordict[index].sort(key=lambda vertex: vertex.get_label())
				# elapsed_time = time.clock() - start_time
				# print('Time elapsed for-loop: {0:.4f} sec'.format(elapsed_time))
				if not nodes == colordict[index]:
					if len(nodes) > len(colordict[index]) and index not in queue:
						queue.append(index)
					else:
						queue.append(newcolor)
					for node in nodes:
						G.update_colordict(node, newcolor)
					newcolor += 1

		i += 1
		global step_counter
		step_counter += 1
	# elapsed_time = time.clock() - start_time
	# print('Time elapsed while-loop: {0:.4f} sec'.format(elapsed_time))
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
		# print(x.colornum)
		for y in colorclass[int(len(colorclass)/2)::]:
			for node in nodes:
				G.update_colordict(node, dictionary[node])
			# print(G.V())
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


#update_colordict(self, oldcolor, newcolor, i):
def update_graph(G, x, y):
	newcolor = max(G.get_colordict().keys()) + 1
	G.update_colordict(G.V()[x], newcolor)
	G.update_colordict(G.V()[y], newcolor)


compare(loadgraph("GI_march4/products72.grl", readlist=True))
# compare(loadgraph("benchmark/threepaths2560.gr", readlist=True))