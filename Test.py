__author__ = 'Mark'

from graphIO import *
from Ex1_makegraphs import disjointunion
import time
import copy

#360.3973 sec
def refine_colors(_l):
	# Initialization
	colordict = {}  # dictionary with key=colornum and value=vertex array
	print('start refining')
	for v in _l.V():
		v.colornum = v.deg
		if v.colornum in colordict:
			colordict[v.colornum].append(v)
		else:
			colordict[v.colornum] = [v]
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

# def prepare_graph(_l):
# 	for v in _l.V():
# 		v.colornum = v.deg
#
# def test(G):
# 	not_done = True
# 	while not_done:
# 		H = copy.deepcopy(G)
# 		colordict2 = G.get_colordict()
# 		for color in colordict2.keys():
# 			vertices = colordict2[color]
# 			neighbours = tuple(get_nb_colors(vertices[0]))
# 			for vertex in vertices:
# 				nbcolors = tuple(get_nb_colors(vertex))
# 				if neighbours != nbcolors:
# 					newcolor = max(colordict2.keys()) + 1
# 					print(color, newcolor, G.V().index(vertex))
# 					H.update_colordict(color, newcolor, G.V().index(vertex))
# 		if colordict2 == H.get_colordict():
# 			not_done = False
# 		G = H
# 	print(G.get_colordict())
# 	finalcolors = []
# 	for node in G.V():
# 		finalcolors.append(node.colornum)
# 	return finalcolors

def get_nb_colors(v):
	return sorted(n.colornum for n in v.nbs)


def compare(x):
	_l = x[0]
	graphs = _l[0]
	nodes = []
	nodes.append(tuple([0, len(_l[0].V())]))
	#start_time = time.clock()
	for g in _l[1::]:
		nodes.append(tuple([len(graphs.V()), len(graphs.V())+len(g.V())]))
		print('disjoint union of total and', _l.index(g))
		graphs.addGraph(g.E(), g.V())
		# graphs = disjointunion(graphs, g)
	#elapsed_time = time.clock() - start_time
	#print('Time elapsed: {0:.4f} sec'.format(elapsed_time))
	start_time = time.clock()
	graphs.init_colordict()
	array = test(graphs)
	elapsed_time = time.clock() - start_time
	print('Time elapsed: {0:.4f} sec'.format(elapsed_time))
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
	# print(result)

#306.2617 sec
def efficient(_l):
	#dictionary with key=colornum and value=array with vertices
	colordict = {}

	#for all vertices v in the list of vertices
	for v in _l.V():
		#color of v = degree of v
		v.colornum = v.deg
		if v.colornum in colordict:
			#colordict[v.colornum] gives the value of colordict which is an array
			#with vertices. v is appended to this array
			colordict[v.colornum].append(v)
		else:
			#initilization of the color v.colornum and it's value (an array with
			#only v in it)
			colordict[v.colornum] = [v]

	not_done = True
	#integer with the next colornum
	newcolor = max(colordict.keys()) + 1

	while not_done:
		#empty dictionary in which we will reconstruct colordict
		tempcolordict = dict()
		#empty dictionary in which we put all changes we make in one cycle of the
		#while loop. key = vertex and value = vertex color
		temp = dict()
		#for all keys (colors) in the set of keys
		for key in colordict.keys():
			#array with all vertices of the color specified by key
			array = colordict[key]
			#neighbours of the first element in array
			buren = tuple(get_nb_colors(array[0]))
			#initilization of the color key and it's value (an array with
			#only the first element of array in it)
			tempcolordict[key] = [array[0]]
			#variable that indicates whether we made changes to the value (array
			#of vertices) of the key
			adjusted = False
			#for all vertices in array except the first element
			#array[start index : stop index : step size]
			for value in array[1::]:
				#neighbours' colors of vertex value
				nc = tuple(get_nb_colors(value))
				#if the vertex neighbours colors are the same as the
				#first element of array, append the vertex to the list
				#of vertices with that color
				if nc == buren:
					tempcolordict[value.colornum].append(value)
				else:
					#neighbour colors are not the same, so put the vertex
					#in a newly created color
					if newcolor in tempcolordict:
						tempcolordict[newcolor].append(value)
					else:
						tempcolordict[newcolor] = [value]
						adjusted = True
					#add the vertex to the dictionary temp with its new color
					#as value
					temp[value] = newcolor
			#if changes were made, newcolor was used, so we increment newcolor
			if adjusted:
				newcolor += 1
		#if the newly constructed dictionary is the same as the old one,
		#the color refinement is done
		if tempcolordict == colordict:
			not_done = False
		#for all vertices v in the dictionary with changes (temp),
		#set the new colornum which is the value of temp
		for v in temp.keys():
			v.colornum = temp[v]
		#update colordict with the newly constructed dictionary
		colordict = tempcolordict.copy()
	#return an array with the colornums of all vertices
	finalcolors = []
	for node in _l.V():
		finalcolors.append(node.colornum)
	return finalcolors

# Graph 6x7680
# Time elapsed: 724.3092 sec
# 0 and 1 are isomorph
# 2 and 3 are undecided
# 4 and 5 are isomorph

compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=True))