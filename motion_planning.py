from read_data import *
import random
from math import sin, cos, radians, pi
from knn import *
import networkx as nx
import gui
import matplotlib.pyplot as plt

def gen_datapoint(dimension):
	datapoint = []
	for i in range(dimension):
		datapoint.append(random.uniform(0, 360))
	return datapoint

def generate_data(count, dimension, obstacles, lengths):
	dataset = []
	for i in range(count):
		datapoint = gen_datapoint(dimension)
		while collide(datapoint, obstacles, lengths):
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


def collide(configuration, obstacles, lengths):
	coordinates = get_line_segments_coordinates(configuration, lengths)
	for obstacle in obstacles:
		for i in range(len(configuration)):
			if intersect(obstacle[0], obstacle[1], coordinates[i], coordinates[i+1]):
				return True
	return False

def get_mid_pos(configuration1, configuration2):
	mid_conf = []
	for i in range(len(configuration1)):
		angle1 = configuration1[i]
		angle2 = configuration2[i]
		difference = max(angle1, angle2)-min(angle1, angle2)
		if difference < 180:
			mid_conf.append((angle1+angle2)/2)
		else:
			mid_conf.append( ((angle1+angle2)/2+180)%360 )
	return tuple(mid_conf)

eps = 3

def showDatapoints(dataset):
	for datapoint in dataset:
		plt.scatter(datapoint[0], datapoint[1])
	plt.savefig('cSpace.png')

def check_path(configuration1, configuration2, obstacles, lengths):
	if (customDistance(configuration1, configuration2) < eps):
		return True
	else:
		mid_pos = get_mid_pos(configuration1, configuration2)
		if collide(mid_pos, obstacles, lengths):
			return False
		else:
			return check_path(configuration1, mid_pos, obstacles, lengths) and check_path(mid_pos, configuration2, obstacles, lengths)

if __name__ == '__main__':
	numDOF, lengths, numObst, obstacles = get_robot_data()
	goal_positions = get_goals_data()
	noPathFlag=False
	print 'Generating dataset..'
	dataset = goal_positions
	random_data = generate_data(2000, numDOF, obstacles, lengths)
	dataset = dataset + random_data

	# showDatapoints(dataset)

	numEdges = 0
	print 'Finding nearest neighbors..'
	G=nx.Graph()
	for i in range(len(dataset)):
		G.add_node(i)
	for index, datapoint in enumerate(dataset):
		neighbors = getNeighborIndices(dataset, datapoint, 8)
		for neighbor in neighbors:
			if check_path(dataset[neighbor], datapoint, obstacles, lengths) and neighbor != index :
				numEdges += 1
				G.add_edge(neighbor, index, weight=customDistance(dataset[neighbor], datapoint))

	print 'Finding shortest path..'
	positions = []
	for i in range(len(goal_positions)-1):
		try:
			vertices = nx.shortest_path(G, source=i, target=i+1, weight="weight")
		except nx.exception.NetworkXNoPath:
			vertices = []
			print 'No path'
			noPathFlag=True
		for vertex in vertices:
			positions.append(dataset[vertex])

	print 'Showing results..'

	gui.start_position = goal_positions[0]
	gui.end_position = goal_positions[1]
	gui.obstacles = obstacles
	gui.positions = get_coordinates_from_configurations(positions, lengths)
	gui.goal_positions = get_coordinates_from_configurations(goal_positions, lengths)
	gui.noPathFlag = noPathFlag
	gui.MotionPlanningApp().run()
