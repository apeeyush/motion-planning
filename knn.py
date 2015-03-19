import math
import operator

def euclideanDistance(instance1, instance2):
	distance = 0
	length = len(instance1)
	for x in range(length):
		distance += min( abs(instance1[x]-instance2[x]), 360-abs(instance1[x]-instance2[x]) )
	return distance
	# length = len(instance1)
	# for x in range(length):
	# 	distance += pow((instance1[x] - instance2[x]), 2)
	# return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
	distances = []
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x])
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getNeighborIndices(trainingSet, testInstance, k):
	distances = []
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x])
		distances.append((x, dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

if __name__ == "__main__":
	data1 = [2, 2, 2]
	data2 = [4, 4, 4]
	distance = euclideanDistance(data1, data2)
	print 'Distance: ' + repr(distance)

	trainSet = [[2, 2, 2], [4, 4, 4]]
	testInstance = [5, 5, 5]
	k = 1
	neighbors = getNeighbors(trainSet, testInstance, 1)
	print(neighbors)
