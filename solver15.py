#!/usr/local/bin/python3

import sys
import os
import copy
import heapq
import math
import numpy as np

class State(object):

	def __init__ (self, puzzle, link, cost):
		self.puzzle = puzzle
		self.link = link
		self.cost = cost

	def __eq__ (self, other):
		return self.cost == other.cost

	def __lt__ (self, other):
		return self.cost < other.cost

	def __gt__ (self, other):
		return self.cost > other.cost

"""
Declaring all the variables needed throughout.
"""
n = 4
goal_state = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])

def get_puzzle():

	"""
	Get puzzle, returns the default state board,
	if no input is found then a default input is provided
	"""

	if (sys.argv[1] and os.path.isfile(sys.argv[1])):
		file = open(sys.argv[1])
	else:
		print("No file found, using default file!")
		file = open('input.txt','r',encoding='utf-8')

	reader = file.read()
	file.close()
	reader = get_list(reader)
	origin = State (np.array(reader), '', 0)
	return origin

def get_list(reader, n=4):
	"""
	Returns an integer list of the input
	"""
	lst = reader.split()

	#This step is done to avoid utf-8 encoding
	lst[-1] = lst[-1].replace('\ufeff','')

	matrix = [[0 for x in range(n)] for y in range(n)]
	counter = 0;
	for each_row in range(n):
		for each_column in range(n):
			matrix[each_row][each_column] = int(lst[counter])
			counter += 1;
	return matrix

def calc_hamming (puzzle):

	"""
	Returns hamming distance between goal state and current state.
	Hamming distance is when a tile is not in place the count is incremented by 1
	"""
	total = 0
	for each_row in range(len(goal_state)):
		for each_column in range(len(goal_state[each_row])):
			if (goal_state[each_row][each_column] != puzzle[each_row][each_column]):
				total += 1
	return total

def calc_manhattan (puzzle):

	"""
	Returns Manhattan distance between goal state and current state.
	Manhattan distance is the distance of each tile from its original position
	"""
	return calc_hamming(puzzle)

def get_successor (state):

	"""
	Returns a valid successor from the current state
	"""

	# Getting the location of empty tile
	row, column = find_empty_space(state.puzzle)
	successor_object = []
	
	# To Get Up Successor
	successor1, cost1 = move_up (state.puzzle, row, column)
	successor11 = State(successor1, state.link + 'U', cost1 + state.cost)
	successor_object.append(successor11)

	# To Get Down Successor
	successor2, cost2 = move_down (state.puzzle, row, column)
	successor21 = State(successor2, state.link + 'D', cost2 + state.cost)
	successor_object.append(successor21)
	
	# To Get Left Successor
	successor3, cost3 = move_left (state.puzzle, row, column)
	successor31 = State(successor3, state.link + 'L', cost3 + state.cost)
	successor_object.append(successor31)

	# To Get Right Successor
	successor4, cost4 = move_right (state.puzzle, row, column)
	successor41 = State(successor4, state.link + 'R', cost4 + state.cost)
	successor_object.append(successor41)

	return successor_object

def move_up(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (row == 0):
		newstate[row][column] = newstate[3][column]
		newstate[3][column] = temp

	else:
		newstate[row][column] = newstate[row-1][column]
		newstate[row-1][column] = temp
	return newstate, calc_manhattan(newstate)

def move_down(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (row == 3):
		newstate[row][column] = newstate[0][column]
		newstate[0][column] = temp

	else:
		newstate[row][column] = newstate[row+1][column]
		newstate[row+1][column] = temp
	return newstate, calc_manhattan(newstate)

def move_left(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (column == 0):
		newstate[row][column] = newstate[row][3]
		newstate[row][3] = temp

	else:
		newstate[row][column] = newstate[row][column-1]
		newstate[row][column-1] = temp
	return newstate, calc_manhattan(newstate)

def move_right(state, row, column):

	"""
	Returns the Left movement of the blank tile in the current state
	"""
	newstate = copy.deepcopy(state)
	temp = newstate[row][column]
	if (column == 3):
		newstate[row][column] = newstate[row][0]
		newstate[row][0] = temp

	else:
		newstate[row][column] = newstate[row][column+1]
		newstate[row][column+1] = temp
	return newstate, calc_manhattan(newstate)

def find_empty_space (state):

	"""
	Find the empty tile and return its location
	"""
	for each_row in range(len(state)):
		for each_column in range(len(state[each_row])):
			if (state[each_row][each_column] == 0): return each_row,each_column


def main():
	heap = []
	puzzle = get_puzzle()
	visited = set()
	heapq.heappush(heap, (1,puzzle))
	while (len(heap) > 0):
		current = heapq.heappop(heap)[1]
		print("Visited: " + str(len(visited)) + " Queue Size: " + str(len(heap)) + " Heuristic: " + str(current.cost) + " Type: " + str(type(current.puzzle)))
		visited.add(str(current))
		if (np.array_equal(current.puzzle,goal_state)): 
			print(current.puzzle)
			print(current.link)
			print(current.cost)
			print("END")
			break
		
		successor_list = get_successor(current)
		for each_successor in successor_list:
			if (str(each_successor.puzzle) not in str(visited)):
				heapq.heappush(heap, (each_successor.cost, each_successor))
		

if __name__ == "__main__":
	main()