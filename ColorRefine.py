from  graphIO import *
from basicgraphs import graph
import time
import bisect
import basicpermutationgroup
from permv2 import permutation
from Ex1_makegraphs import disjointunion
import basicpermutationgroup


step_counter = 0
autolist = []
timer = time.clock() - time.clock()


def generate_automorphism(G, trivial):
	global timer
	starter_time = time.clock()
	finaldict, changes = fast_color_refine(G)
	automorphism = True
	colorclass = list()
	for color in finaldict.keys():
		length = len(finaldict[color])
		if length % 2 == 1:
			return 0, changes
		if length >= 4:
			colorlen = len(colorclass)
			if colorlen == 0:
				colorclass = finaldict[color]
				automorphism = False
			elif length <= colorlen:
				colorclass = finaldict[color]
				automorphism = False
	timer = timer + time.clock()-starter_time
	if automorphism:
		size = int(len(G.V())/2)
		f = [0]*size  # (list(int(len(G.V())/2))
		for color in finaldict.keys():
			vertices = finaldict[color]
			# print(vertices)
			f[vertices[0].get_label()-size] = vertices[1].get_label()-size
		perm = permutation(len(f), mapping=f)
		# if membership_testing(autolist, perm):
		autolist.append(perm)
		return 1, changes
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
			# nielisgek = 0
			if first:
				# print(y, trivial)
				first = False
				nielisgek, new_changes = generate_automorphism(G, trivial)
			else:
				nielisgek, new_changes = generate_automorphism(G, False)
			new_changes.append(x)
			new_changes.append(y)
			for node in new_changes:
				G.update_colordict(node, dictionary[node])
			if nielisgek == 1 and not trivial:
				return 1, changes
	return 0, changes


def checkautomorphisms(x, i):
	graph_list= x[0]
	x2 = disjointunion(graph_list[i], graph())
	disjoint_union = disjointunion(graph_list[i], x2)
	disjoint_union.init_colordict()
	generate_automorphism(disjoint_union, True)
	autolist.append(permutation(int(len(disjoint_union.V())/2)))
	autolist2 = basicpermutationgroup.Reduce(autolist, 0)
	return order_computation(autolist2)


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
						count = count_isomorphisms_fast(union, True)
						if count > 0:
							isolist[i].append(j)
							isolist[j].append(i)
							if i not in isomorphisms_dict.keys():
								isomorphisms_dict[i] = checkautomorphisms(x, i)
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
					changed_list.append(node)
					G.update_colordict(node, newcolor)
				newcolor += 1
		i += 1
	return G.get_colordict(), changed_list


def order_computation(generators):
	starting_time = time.clock()
	nontrivial_vextex = basicpermutationgroup.FindNonTrivialOrbit(generators)
	if nontrivial_vextex is None:
		return 1
	orbit = basicpermutationgroup.Orbit(generators, nontrivial_vextex)
	global timer
	stabilizer = basicpermutationgroup.Stabilizer(generators, nontrivial_vextex)
	lengthorbit = len(orbit)
	timer = timer + time.clock()-starting_time
	return lengthorbit*order_computation(stabilizer)

# def order_computation(generators):
# 	result = 1
# 	global timer
# 	starting_time = time.clock()
# 	nontrivial_vextex = basicpermutationgroup.FindNonTrivialOrbit(generators)
# 	while nontrivial_vextex is not None:
# 		orbit = basicpermutationgroup.Orbit(generators, nontrivial_vextex)
# 		stabilizer = basicpermutationgroup.Stabilizer(generators, nontrivial_vextex)
# 		generators = stabilizer
# 		nontrivial_vextex = basicpermutationgroup.FindNonTrivialOrbit(generators)
# 		result *= len(orbit)
# 	timer = timer + time.clock()-starting_time
# 	return result


# def membership_testing(generators, perm):
# 	# start_time = time.clock()
# 	if not generators and not perm.istrivial():
# 		return True
# 	nontrivial_vextex = basicpermutationgroup.FindNonTrivialOrbit(generators)
# 	if nontrivial_vextex is None:
# 		return False
# 	orbit, transversals = basicpermutationgroup.Orbit(generators, nontrivial_vextex, True)
# 	temporary_perm = perm
# 	for transversal in transversals:
# 		if subset(perm.cycles()[0], transversal):
# 			temporary_perm = (-transversal) * perm
# 			templist = []
# 			for cycle in temporary_perm.cycles():
# 				for el in cycle:
# 					templist.append(el)
# 			if nontrivial_vextex not in templist:
# 				break
# 	if temporary_perm.istrivial():
# 		return True
# 	return membership_testing(basicpermutationgroup.Stabilizer(generators, nontrivial_vextex), temporary_perm)


def subset(permsub, other):
	for cycle in other.cycles():
		list = []
		for p in permsub:
			if p in cycle:
				list.append(p)
		if list == permsub:
			return True
	return False


def get_nb_colors(v):
	return sorted(n.colornum for n in v.get_nbs())


def count_isomorphisms_fast(G, trivial):
	finaldict, unused = fast_color_refine(G)
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
		first = True
		for y in colorclass[int(len(colorclass)/2)::]:
			for node in nodes:
				G.update_colordict(node, dictionary[node])
			update_graph(G, G.V().index(x), G.V().index(y))
			if first:
				# print(y, trivial)
				first = False
				if count_isomorphisms_fast(G, True) > 0:
					return 1
			else:
				if count_isomorphisms_fast(G, False) > 0:
					return 1
		return 0


def update_graph(G, x, y):
	newcolor = max(G.get_colordict().keys()) + 1
	G.update_colordict(G.V()[x], newcolor)
	G.update_colordict(G.V()[y], newcolor)


start_time = time.clock()
compare_fast(loadgraph("GI_march4/bigtrees3.grl", readlist=True))
# compare(loadgraph("GI_march4/products216.grl", readlist=True))
# compare(loadgraph("benchmark/threepaths10240.gr", readlist=True))
# compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=True))
elapsed_time = time.clock() - start_time
print('Time elapsed with reading: {0:.4f} sec'.format(elapsed_time))

# perm = permutation(6, cycles=[[0,1,2],[4,5]])
# perm2 = permutation(6, cycles=[[2,3]])
# # perm3 = permutation(6, cycles=[[1,3,2],[4,5]])
# list = [perm,perm2]
# print(order_computation(list))
# print("perm time ", permutation.timer)
print("timer ", timer)
# print("scheier timer ", basicpermutationgroup.timer)
