from  graphIO import *
from basicgraphs import graph
import time
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
			vertices = sorted(finaldict[color], key=lambda vertex: vertex.get_label())
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
	global autolist
	autolist.append(permutation(int(len(disjoint_union.V())/2)))
	autolist2 = basicpermutationgroup.Reduce(autolist, 0)
	autolist = []
	return count * order_computation(autolist2)



def find_isomorphisms(graph_list2, GI_problem= True, Aut=True):
	isomorphisms_dict = dict()
	graph_list = graph_list2[0]

	disjoint_union = graph_list[0]
	graph_ranges = list()
	graph_ranges.append(tuple([0, len(graph_list[0].V())]))

	for g in graph_list[1::]:
		graph_ranges.append(tuple([len(disjoint_union.V()), len(disjoint_union.V())+len(g.V())]))
		disjoint_union = disjointunion(disjoint_union, g)

	disjoint_union.init_colordict()
	timer = time.clock()
	fast_color_refine(disjoint_union)
	print(time.clock()-timer)
	array = []
	for vertex in disjoint_union.V():
		array.append(vertex.colornum)
	result = []
	for n in graph_ranges:
		result.append(sorted(array[n[0]:n[1]:]))

	if GI_problem:
		isolist = dict()
		isomorphismes_list = []
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
							isolist[i].append(j)
							isolist[j].append(i)
							isomorphisms_dict[i] = 1
							if len(isomorphismes_list) == 0 or isomorphismes_list[-1][0] != i:
								isomorphismes_list.append([i,j])
							else:
								isomorphismes_list[-1].append(j)
						else:
							union = disjointunion(graph_list[i], graph_list[j])
							union.init_colordict()
							count, unused = count_isomorphisms_fast(union, True)
							if len(isomorphismes_list) == 0 or isomorphismes_list[-1][0] != i:
								isomorphismes_list.append([i,j])
							else:
								isomorphismes_list[-1].append(j)
							if count > 0 and Aut:
								isolist[i].append(j)
								isolist[j].append(i)
								if i not in isomorphisms_dict.keys():
									isomorphisms_dict[i] = checkautomorphisms(graph_list2, j)
									global autolist
									autolist = []
			if len(isolist[i]) > 1:
				for h in range(len(isolist[i])):
					for k in range(h+1, len(isolist[i])):
						isolist[h].append(k)
						isolist[k].append(h)
		if not Aut:
			for isomorphism in isomorphismes_list:
				print(isomorphism)
		else:
			for isomorphism in isomorphismes_list:
				print(isomorphism, "		", isomorphisms_dict[isomorphism[0]])
	elif Aut:
		for i in range(len(result)):
			print("graph ", i, ":    ", checkautomorphisms(graph_list2, i))


def fast_color_refine(G):
	timer3 = 0
	changed_list = []
	colordict = G.get_colordict()
	removable_queue = []
	largest_color_length = 0
	largest_color = 0
	for color in colordict.keys():
		if color > 0:
			if largest_color_length == 0:
				largest_color = color
				largest_color_length = len(colordict[color])
			elif len(colordict[color]) >= largest_color_length:
				removable_queue.append(largest_color)
				largest_color = color
				largest_color_length = len(colordict[color])
			else:
				removable_queue.append(color)
	i = 0
	newcolor = max(colordict.keys()) + 1
	while len(removable_queue) >= 1:
		incoming_nodes_dict = dict()
		incoming_nodes_dict2 = dict()
		queue_zero = removable_queue[0]
		removable_queue.pop(0)
		for node in colordict[queue_zero]:
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
		for color in sorted(incoming_nodes_dict.keys()):
			nodes = incoming_nodes_dict[color]
			nodes.sort(key=lambda vertex: vertex.get_label())
			nodes2 = incoming_nodes_dict2[color]
			nodes2.sort(key=lambda vertex: vertex.get_label())
			if color in colordict.keys():
				if not nodes2 == colordict[color]:
					dict_count_nodes = dict()
					for node in nodes:
						temp = nodes2.count(node)
						if temp in dict_count_nodes.keys():
							dict_count_nodes[temp].append(node)
						else:
							dict_count_nodes[temp] = [node]
					new_color_classes = [color]
					for key in dict_count_nodes.keys():
						if not sorted(dict_count_nodes[key], key=lambda vertex: vertex.get_label()) == G.get_colordict()[color]:
							for node in dict_count_nodes[key]:
								changed_list.append(node)
								G.update_colordict(node, newcolor)
							new_color_classes.append(newcolor)
							newcolor += 1
					if color not in removable_queue:
						new_color_classes.sort()
						new_color_classes.sort(key=lambda colour: len(G.get_colordict()[colour]))
						for colour in range(len(new_color_classes)-1):
							removable_queue.append(new_color_classes[colour])
					else:
						new_color_classes.remove(color)
						new_color_classes.sort()
						new_color_classes.sort(key=lambda colour: len(G.get_colordict()[colour]))
						for colour in range(len(new_color_classes)):
							removable_queue.append(new_color_classes[colour])

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
	count = factorial(empty_count)
	for elem in false_twin_list:
		count *= factorial(len(elem))
	seen = []
	for elem in twin_list:
		if elem not in seen:
			piet = twin_list.count(elem)
			if piet > 1:
				seen.append(elem)
				count *= factorial(twin_list.count(elem))
	false_twin_list.sort(key=lambda l: len(l))
	newcolor = max(g.get_colordict().keys()) + 1
	last_length = 0
	for twinlist in false_twin_list:
		if len(twinlist) == last_length:
			newcolor -= 1
		last_length = len(twinlist)
		if twinlist[0] in g.V():
			g.update_colordict(twinlist[0], newcolor)
			twinlist.remove(twinlist[0])
			newcolor += 1
			for node in twinlist:
				g.delvert(node)
	last_length = 0
	seen.sort(key=lambda l: len(l))
	for twinlist in seen:
		if len(twinlist) == last_length:
			newcolor -= 1
		last_length = len(twinlist)
		if twinlist[0] in g.V():
			g.update_colordict(twinlist[0], newcolor)
			twinlist.remove(twinlist[0])
			newcolor += 1
			for node in twinlist:
				g.delvert(node)
	return count

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

def factorial(n):
	count = 1
	while n > 1:
		count *= n
		n -= 1
	return count
GI = True
Aut = True
if input("GI Problem?(True/False): ").lower() == "false":
	GI = False
if input("#Aut?(True/False): ").lower() == "false":
	Aut = False
find_isomorphisms(loadgraph(input("Your Inputgraph: "), readlist=True), GI, Aut)