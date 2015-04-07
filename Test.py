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

# def preprocessing(g):
# 	false_twin_list, twin_list, empty_count = get_twins(g)
# 	count = math.factorial(empty_count)
# 	for elem in false_twin_list:
# 		count *= math.factorial(len(elem))
# 	# true_list = []
# 	# for elem in twin_list:
# 	# 	nbs = list(elem[0].nbs).copy()
# 	# 	for node in elem:
# 	# 		if node is not elem[0]:
# 	# 			nbs.remove(node)
# 	# 	true_list.append(nbs)
# 	seen = []
# 	for elem in twin_list:
# 		if elem not in seen:
# 			piet = twin_list.count(elem)
# 			if piet > 1:
# 				seen.append(elem)
# 				count *= math.factorial(twin_list.count(elem))
# 	false_twin_list.sort(key=lambda l: len(l))
# 	newcolor = max(g._colordict.keys()) + 1
# 	last_length = 0
# 	for twinlist in false_twin_list:
# 		if len(twinlist) == last_length:
# 			newcolor -= last_length
# 		for node in twinlist:
# 			g.update_colordict(node, newcolor)
# 			newcolor += 1
# 		last_length = len(twinlist)
# 	last_length = 0
# 	seen.sort(key=lambda l: len(l))
# 	for twinlist in seen:
# 		if len(twinlist) == last_length:
# 			newcolor -= last_length
# 		for node in twinlist:
# 			g.update_colordict(node, newcolor)
# 			newcolor += 1
# 		last_length = len(twinlist)
# 	return count

start_time = time.clock()
# compare_fast(loadgraph("GI_march4/bigtrees1.grl", readlist=True))
# compare_fast(loadgraph("GI_march4/bigtrees3.grl", readlist=True))
# compare_fast(loadgraph("NewBenchmarkInstances/hugecographs.grl", readlist=True))
# graph =loadgraph("NewBenchmarkInstances/hugecographs.grl", readlist=False)
# graph.init_colordict()
# blaat, yolo = fast_color_refine(graph)
# compare_fast(loadgraph("GI_march4/torus24.grl", readlist=True))
# compare(loadgraph("benchmark/threepaths10240.gr", reisadlt=True))
find_isomorphisms(loadgraph("GI_TestInstancesWeek1/crefBM_6_15.grl", readlist=True), False, True)
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

# largest_color = 0
					# if color not in queue and itterate_color < newcolor:
					# 	added = True
					# 	# queue.append(color)
					# 	largest_color = color
					# while itterate_color < newcolor:
					# 	if not added:
					# 		added = True
					# 		largest_color = color
					# 		# queue.append(itterate_color)
					# 	elif len(G.get_colordict()[largest_color]) > len(G.get_colordict()[itterate_color]):
					# 		# queue[len(queue)-1] = itterate_color
					# 		queue.append(itterate_color)
					# 		used_queue.append(itterate_color)
					# 	else:
					# 		queue.append(largest_color)
					# 		used_queue.append(largest_color)
					# 		largest_color = itterate_color
					# 	itterate_color += 1


					# while itterate_color < newcolor:
					# 	if not added:
					# 		queue.append(itterate_color)
					# 		added = True
					# 	elif len(G.get_colordict()[queue[-1]]) >= len(G.get_colordict()[itterate_color]):
					# 		queue[-1] = itterate_color
					# 	itterate_color += 1
		# print(removable_queue)
		# print(removable_queue)

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

# def subset(permsub, other):
# 	for cycle in other.cycles():
# 		list = []
# 		for p in permsub:
# 			if p in cycle:
# 				list.append(p)
# 		if list == permsub:
# 			return True
# 	return False





# Graph 6x7680
# Time elapsed: 724.3092 sec
# 0 and 1 are isomorph
# 2 and 3 are undecided
# 4 and 5 are isomorph

# compare(loadgraph("GI_march4/products72.grl", readlist=True))

