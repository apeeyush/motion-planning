from read_data import *
import random
from math import sin, cos, radians, pi
from knn import *
import networkx as nx
import gui
import matplotlib.pyplot as plt

# http://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect

def gen_datapoint(dimension):
	datapoint = []
	for i in range(dimension):
		datapoint.append(random.uniform(0, 360))
	return datapoint

def generate_data(count, dimension, obstacles):
	dataset = []
	for i in range(count):
		datapoint = gen_datapoint(dimension)
		while collide(datapoint, obstacles):
			datapoint = gen_datapoint(dimension)
		dataset.append(tuple(datapoint))
	return dataset

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def get_line_segments_coordinates(configuration, lengths):
	x = 0
	y = 0
	coordinates = [(0,0)]
	theta=0
	numDOF = len(configuration)
	for i in range(numDOF):
		theta = theta + configuration[i]
		theta_rad = radians(theta)
		x = x + lengths[i]*cos(theta_rad)
		y = y + lengths[i]*sin(theta_rad)
		coordinates.append((x,y))
	return coordinates

def get_coordinates_from_configurations(configurations, lengths):
	coordinates = []
	for configuration in configurations:
		coordinates.append(get_line_segments_coordinates(configuration, lengths))
	return coordinates


def collide(configuration, obstacles):
	coordinates = get_line_segments_coordinates(configuration, lengths)
	for obstacle in obstacles:
		for i in range(len(configuration)):
			if intersect(obstacle[0], obstacle[1], coordinates[i], coordinates[i+1]):
				return True
	return False

def get_mid_pos(configuration1, configuration2):
	mid_conf = []
	for i in range(len(configuration1)):
		mid_conf.append((configuration1[i]+configuration2[i])/2)
	return tuple(mid_conf)

eps = 2

def showDatapoints(dataset):
	for datapoint in dataset:
		plt.scatter(datapoint[0], datapoint[1])
	plt.show()

def check_path(configuration1, configuration2, obstacles):
	if (euclideanDistance(configuration1, configuration2) < eps):
		return True
	else:
		mid_pos = get_mid_pos(configuration1, configuration2)
		if collide(mid_pos, obstacles):
			return False
		else:
			return check_path(configuration1, mid_pos, obstacles) and check_path(mid_pos, configuration2, obstacles)

if __name__ == '__main__':
	numDOF, lengths, numObst, obstacles = get_robot_data()
	goal_positions = get_goals_data()
	dataset = goal_positions
	random_data = generate_data(2000, numDOF, obstacles)
	dataset = dataset + random_data
	numEdges = 0
	print 'Generated dataset..'
	G=nx.Graph()
	for i in range(len(dataset)):
		G.add_node(i)
	for index, datapoint in enumerate(dataset):
		neighbors = getNeighborIndices(dataset, datapoint, 10)
		for neighbor in neighbors:
			if check_path(dataset[neighbor], datapoint, obstacles) and neighbor != index :
				numEdges += 1
				G.add_edge(neighbor, index, weight=euclideanDistance(dataset[neighbor], datapoint))
	print numEdges
	showDatapoints(dataset)
	# nx.draw(G)
	# plt.draw()
	# plt.show()
	vertices = nx.shortest_path(G, source=0, target=1)
	positions = []
	for vertex in vertices:
		positions.append(dataset[vertex])
	print 'Showing results..'

	gui.start_position = goal_positions[0]
	gui.end_position = goal_positions[1]
	gui.obstacles = obstacles
	gui.positions = get_coordinates_from_configurations(positions, lengths)
	gui.MotionPlanningApp().run()
