from  graphIO import *
from basicgraphs import graph
import time
import math
from permv2 import permutation
from Ex1_makegraphs import disjointunion
import basicpermutationgroup


step_counter = 0
autolist = []
timer = time.clock() - time.clock()


def generate_automorphism(G, trivial):
	finaldict, changes = fast_color_refine(G)
	automorphism = True
	colorclass = list()
	for color in finaldict.keys():
		length = len(finaldict[color])
		if length % 2 == 1:
			return changes
		if length >= 4:
			colorlen = len(colorclass)
			if colorlen == 0:
				colorclass = finaldict[color]
				automorphism = False
			elif length <= colorlen:
				colorclass = finaldict[color]
				automorphism = False
	if automorphism:
		size = int(len(G.V())/2)
		mapping = [0]*size
		for color in finaldict.keys():
			vertices = finaldict[color]
			mapping[vertices[0].get_label()-size] = vertices[1].get_label()-size
		perm = permutation(len(mapping), mapping=mapping)
		autolist.append(perm)
		return changes
	else:
		nodes = G.V()
		dictionary = dict()
		for node in nodes:
			dictionary[node] = node.colornum
		colorclass.sort(key=lambda vertex: vertex.get_label())
		x = colorclass[0]
		first = True
		for y in colorclass[int(len(colorclass)/2)::]:
			update_graph(G, G.V().index(x), G.V().index(y))
			if first:
				first = False
				new_changes = generate_automorphism(G, trivial)
			else:
				new_changes = generate_automorphism(G, False)
			new_changes.append(x)
			new_changes.append(y)
			for node in new_changes:
				G.update_colordict(node, dictionary[node])
			if not trivial:
				return changes
	return changes


def checkautomorphisms(x, i):
	input_graph = x[0][i]
	input_graph.init_colordict()
	count = preprocessing(input_graph)
	length = len(input_graph.V())
	graph_copy = disjointunion(input_graph, graph())
	colordict = input_graph.get_colordict()
	disjoint_union = disjointunion(input_graph, graph_copy)
	disjoint_union.init_colordict()
	for color in colordict.keys():
		for node in colordict[color]:
			disjoint_union.update_colordict(disjoint_union.V()[input_graph.V().index(node)], color)
			disjoint_union.update_colordict(disjoint_union.V()[input_graph.V().index(node)+length], color)
	generate_automorphism(disjoint_union, True)
	autolist.append(permutation(int(len(disjoint_union.V())/2)))
	autolist2 = basicpermutationgroup.Reduce(autolist, 0)
	return count * order_computation(autolist2)


def compare_fast(x):
	isomorphisms_dict = dict()
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
						preprocessing(union)
						count, unused = count_isomorphisms_fast(union, True)
						if count > 0:
							isolist[i].append(j)
							isolist[j].append(i)
							if i not in isomorphisms_dict.keys():
								isomorphisms_dict[i] = checkautomorphisms(x, j)
								global autolist
								autolist = []
							print('there are ', isomorphisms_dict[i], ' isomorphisms')
						else:
							print(i, 'and', j, 'are not isomorph')
		if len(isolist[i]) > 1:
			for h in range(len(isolist[i])):
				for k in range(h+1, len(isolist[i])):
					isolist[h].append(k)
					isolist[k].append(h)
	print("yolo")
	print(isolist)
	elapsed2_time = time.clock() - starter_time
	print('Time elapsed without reading: {0:.4f} sec'.format(elapsed2_time))


def fast_color_refine(G):
	changed_list = []
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
		incoming_nodes_dict2 = dict()
		for node in colordict[queue[i]]:
			for nb in node.get_nbs():
				color = nb.colornum
				if color not in incoming_nodes_dict:
					incoming_nodes_dict[color] = [nb]
					incoming_nodes_dict2[color] = [nb]
				elif nb not in incoming_nodes_dict[color]:
					incoming_nodes_dict[color].append(nb)
					incoming_nodes_dict2[color].append(nb)
				else:
					incoming_nodes_dict2[color].append(nb)
		for color in incoming_nodes_dict.keys():
			added = False
			nodes = incoming_nodes_dict[color]
			nodes.sort(key=lambda vertex: vertex.get_label())
			# if not nodes == colordict[color]:
			# 	added = True
			# 	if len(nodes) > len(colordict[color]) and color not in queue:
			# 		queue.append(color)
			# 	else:
			# 		queue.append(newcolor)
			# 	for node in nodes:
			# 		changed_list.append(node)
			# 		G.update_colordict(node, newcolor)
			# 	newcolor += 1
			nodes2 = incoming_nodes_dict2[color]
			nodes2.sort(key=lambda vertex: vertex.get_label())
			# if color in colordict.keys():
			# 	if not nodes2 == colordict[color] and not nodes2 == colordict[newcolor-1]:
			# 		test = dict()
			# 		for node in nodes:
			# 			temp = nodes2.count(node)
			# 			if temp > 1:
			# 				if temp in test.keys():
			# 					test[temp].append(node)
			# 				else:
			# 					test[temp] = [node]
			# 		itterate_color = newcolor
			# 		booltest = False
			# 		for key in test.keys():
			# 			if not test[key] == colordict[color] and not test[key] == colordict[newcolor-1]:
			# 				for node in test[key]:
			# 					changed_list.append(node)
			# 					G.update_colordict(node, newcolor)
			# 					booltest = True
			# 				newcolor += 1
			# 		while booltest and itterate_color < newcolor:
			# 			if not added:
			# 				queue.append(itterate_color)
			# 				added = True
			# 			elif queue[len(queue)-1] not in G._colordict.keys() or itterate_color in G._colordict.keys() and len(G._colordict[queue[len(queue)-1]]) > len(G._colordict[itterate_color]):
			# 				queue[len(queue)-1] = itterate_color
			# 			itterate_color += 1
			if color in colordict.keys():
				if not nodes2 == colordict[color]:
					dict_count_nodes = dict()
					for node in nodes:
						temp = nodes2.count(node)
						if temp in dict_count_nodes.keys():
							dict_count_nodes[temp].append(node)
						else:
							dict_count_nodes[temp] = [node]
					itterate_color = newcolor
					# booltest = False
					for key in dict_count_nodes.keys():
						if not dict_count_nodes[key] == colordict[color]:
							for node in dict_count_nodes[key]:
								changed_list.append(node)
								G.update_colordict(node, newcolor)
								# booltest = True
							newcolor += 1
					while itterate_color < newcolor:
						if not added:
							queue.append(itterate_color)
							added = True
						elif len(G.get_colordict()[queue[len(queue)-1]]) > len(G.get_colordict()[itterate_color]):
							queue[len(queue)-1] = itterate_color
						itterate_color += 1
		i += 1
	return G.get_colordict(), changed_list


def order_computation(generators):
	nontrivial_vextex = basicpermutationgroup.FindNonTrivialOrbit(generators)
	if nontrivial_vextex is None:
		return 1
	orbit = basicpermutationgroup.Orbit(generators, nontrivial_vextex)
	stabilizer = basicpermutationgroup.Stabilizer(generators, nontrivial_vextex)
	lengthorbit = len(orbit)
	return lengthorbit*order_computation(stabilizer)


def get_nb_colors(v):
	return sorted(n.colornum for n in v.get_nbs())


def count_isomorphisms_fast(G, trivial):
	finaldict, changed_nodes = fast_color_refine(G)
	isomorph = True
	colorclass = []
	for color in finaldict.keys():
		length = len(finaldict[color])
		if length % 2 == 1:
			return 0, changed_nodes
		if length >= 4:
			colorlen = len(colorclass)
			if colorlen == 0:
				colorclass = finaldict[color]
				isomorph = False
			elif length <= colorlen:
				colorclass = finaldict[color]
				isomorph = False
	if isomorph:
		return 1, changed_nodes
	else:
		nodes = G.V()
		dictionary = dict()
		first = True
		for node in nodes:
			dictionary[node] = node.colornum
		colorclass.sort(key=lambda vertex: vertex.get_label())
		x = colorclass[0]
		for y in colorclass[int(len(colorclass)/2)::]:
			update_graph(G, G.V().index(x), G.V().index(y))
			if first:
				temp, new_changes = count_isomorphisms_fast(G, trivial)
				first = False
			else:
				temp, new_changes = count_isomorphisms_fast(G, False)
			new_changes.append(x)
			new_changes.append(y)
			for node in new_changes:
				G.update_colordict(node, dictionary[node])
			if temp > 0:
					return 1, changed_nodes
			if not trivial:
				return 0, changed_nodes
		return 0, changed_nodes


def update_graph(G, x, y):
	newcolor = max(G.get_colordict().keys()) + 1
	G.update_colordict(G.V()[x], newcolor)
	G.update_colordict(G.V()[y], newcolor)


def preprocessing(g):
	false_twin_list, twin_list, empty_count = get_twins(g)
	count = math.factorial(empty_count)
	for elem in false_twin_list:
		count *= math.factorial(len(elem))
	# true_list = []
	# for elem in twin_list:
	# 	nbs = list(elem[0].nbs).copy()
	# 	for node in elem:
	# 		if node is not elem[0]:
	# 			nbs.remove(node)
	# 	true_list.append(nbs)
	seen = []
	for elem in twin_list:
		if elem not in seen:
			piet = twin_list.count(elem)
			if piet > 1:
				seen.append(elem)
				count *= math.factorial(twin_list.count(elem))
	false_twin_list.sort(key=lambda l: len(l))
	newcolor = max(g._colordict.keys()) + 1
	last_length = 0
	for twinlist in false_twin_list:
		if len(twinlist) == last_length:
			newcolor -= last_length
		for node in twinlist:
			g.update_colordict(node, newcolor)
			newcolor += 1
		last_length = len(twinlist)
	last_length = 0
	seen.sort(key=lambda l: len(l))
	for twinlist in seen:
		if len(twinlist) == last_length:
			newcolor -= last_length
		for node in twinlist:
			g.update_colordict(node, newcolor)
			newcolor += 1
		last_length = len(twinlist)
	return count



# def preprocessing(g):
# 	false_twin_list, twin_list, empty_count = get_twins(g)
# 	count = math.factorial(empty_count)
# 	for elem in false_twin_list:
# 		count *= math.factorial(len(elem))
# 	seen = []
# 	for elem in twin_list:
# 		if elem not in seen:
# 			piet = twin_list.count(elem)
# 			if piet > 1:
# 				seen.append(elem)
# 				count *= math.factorial(twin_list.count(elem))
# 	false_twin_list.sort(key=lambda l: len(l))
# 	print(false_twin_list)
# 	newcolor = max(g._colordict.keys()) + 1
# 	last_length = 0
# 	for twinlist in false_twin_list:
# 		if len(twinlist) == last_length:
# 			newcolor -= 1
# 		last_length = len(twinlist)
# 		if twinlist[0] in g.V():
# 			g.update_colordict(twinlist[0], newcolor)
# 			twinlist.remove(twinlist[0])
# 			newcolor += 1
# 			for node in twinlist:
# 				g.delvert(node)
# 	last_length = 0
# 	seen.sort(key=lambda l: len(l))
# 	for twinlist in seen:
# 		if len(twinlist) == last_length:
# 			newcolor -= 1
# 		last_length = len(twinlist)
# 		if twinlist[0] in g.V():
# 			g.update_colordict(twinlist[0], newcolor)
# 			twinlist.remove(twinlist[0])
# 			newcolor += 1
# 			for node in twinlist:
# 				g.delvert(node)
# 	return count, g

def get_twins(g):
	false_twins_dict = dict()
	twins_dict = dict()
	temp = []
	number = 0
	for node in g.V():
		if len(node.get_nbs()) == 0:
			temp.append(node)
			number += 1
		else:
			nbs = node.get_nbs().copy()
			if tuple(nbs) not in false_twins_dict.keys():
				false_twins_dict[tuple(nbs)] = [node]
			else:
				false_twins_dict[tuple(nbs)].append(node)
			nbs.append(node)
			# print(node, nbs, node.get_nbs())
			nbs.sort(key=lambda vertex: vertex.get_label())
			if tuple(nbs) not in twins_dict.keys():
				twins_dict[tuple(nbs)] = [node]
			else:
				twins_dict[tuple(nbs)].append(node)
	for node in temp:
		g.delvert(node)
	false_keys = list(false_twins_dict.keys()).copy()
	for key in false_keys:
		if len(false_twins_dict[key]) == 1:
			false_twins_dict.pop(key)
	keys = list(twins_dict.keys()).copy()
	for key in keys:
		if len(twins_dict[key]) == 1:
			twins_dict.pop(key)
	return list(false_twins_dict.values()), list(twins_dict.values()), number


start_time = time.clock()
compare_fast(loadgraph("GI_march4/bigtrees1.grl", readlist=True))
# compare_fast(loadgraph("GI_march4/bigtrees3.grl", readlist=True))
# compare_fast(loadgraph("NewBenchmarkInstances/hugecographs.grl", readlist=True))
# graph =loadgraph("NewBenchmarkInstances/test.gr", readlist=False)
# graph.init_colordict()
# blaat, yolo = fast_color_refine(graph)
# print(blaat)
# compare_fast(loadgraph("GI_march4/cographs1.grl", readlist=True))
# compare(loadgraph("benchmark/threepaths10240.gr", reisadlt=True))
# compare_fast(loadgraph("GI_TestInstancesWeek1/crefBM_4_9.grl", readlist=True))
# x = loadgraph("NewBenchmarkInstances/hugecographs.grl", readlist=True)
# x1 = x[0][4]
# x2 = x[0][5]
#
# union = disjointunion(x1,x2)
# writeDOT(union, "test.dot")
# union.init_colordict()
# y,z = fast_color_refine(union)
# print(y)


elapsed_time = time.clock() - start_time
print('Time elapsed with reading: {0:.4f} sec'.format(elapsed_time))

# print(checkautomorphisms(loadgraph("GI_march4/bigtrees3.grl", readlist=True), 0))
# perm = permutation(6, cycles=[[0,1,2],[4,5]])
# perm2 = permutation(6, cycles=[[2,3]])
# # perm3 = permutation(6, cycles=[[1,3,2],[4,5]])
# list = [perm,perm2]
# print(order_computation(list)).timer)

# print("perm time ", permutation.timer)

#print("timer ", timer)

# print("scheier timer ", basicpermutationgroup