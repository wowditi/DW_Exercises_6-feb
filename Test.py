__author__ = 'Mark'

from graphIO import *
from Ex1_makegraphs import disjointunion
import time

#1083.1556 sec
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


def get_nb_colors(v):
	return sorted(n.colornum for n in v.nbs)


def compare(x):
	_l = x[0]
	graphs = _l[0]
	nodes = []
	nodes.append(tuple([0, len(_l[0].V())]))
	for g in _l[1::]:
		nodes.append(tuple([len(graphs.V()), len(graphs.V())+len(g.V())]))
		print('disjoint union of total and', _l.index(g))
		graphs = disjointunion(graphs, g)
	start_time = time.clock()
	array = refine_colors(graphs)
	elapsed_time = time.clock() - start_time
	print('Time elapsed: {0:.4f} sec'.format(elapsed_time))
	result = []
	for n in nodes:
		result.append(sorted(array[n[0]:n[1]:]))
	for i in range(len(result)):
		for j in range(i+1, len(result)):
			if result[i] == result[j]:
				print(i, 'and', j, 'are isomorph')
	# print(result)

#849.5499 sec
def efficient(_l):
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
	print('NEWCOLOR', newcolor)
	print('KEYS', colordict.keys())

	while not_done:
		tempcolordict = dict()
		# print(colordict.keys())
		# print(colordict)
		temp = dict()
		for key in colordict.keys():
			array = colordict[key]
			buren = tuple(get_nb_colors(array[0]))
			# print(key)
			tempcolordict[key] = [array[0]]
			adjusted = False

			for value in array[1::]:
				nc = tuple(get_nb_colors(value))
				if nc == buren:
					# try:
					tempcolordict[value.colornum].append(value)
					# except KeyError:
					# 	print(key, value.colornum)
					# 	print(colordict.keys())
				else:
					if newcolor in tempcolordict:
						tempcolordict[newcolor].append(value)
					else:
						tempcolordict[newcolor] = [value]
						# print(tempcolordict[newcolor], newcolor)
						adjusted = True
					temp[value] = newcolor
			if adjusted:
				# print(key)
				newcolor += 1
		if tempcolordict == colordict:
			not_done = False
		# print(temp)
		for v in temp.keys():
			v.colornum = temp[v]
		colordict = tempcolordict.copy()
		# print(colordict)
		print('step')
	# print(colordict)
	finalcolors = []
	for node in _l.V():
		finalcolors.append(node.colornum)

	return finalcolors



compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_4098.grl", readlist=True))