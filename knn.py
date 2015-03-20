import math
import operator
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import DistanceMetric

def customDistance(instance1, instance2):
	distance = 0
	length = len(instance1)
	for x in range(length):
		distance += abs(min( abs(instance1[x]-instance2[x]), 360-abs(instance1[x]-instance2[x]) ))
	return distance

def getNeighbors(trainingSet, testInstance, k):
	distances = []
	for x in range(len(trainingSet)):
		dist = customDistance(testInstance, trainingSet[x])
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

def getNeighborIndices(trainingSet, testInstance, k):
	distances = []
	for x in range(len(trainingSet)):
		dist = customDistance(testInstance, trainingSet[x])
		distances.append((x, dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

# def getKnnNeighbors(trainingSet, k):
# 	nbrs=NearestNeighbors(n_neighbors=k,metric='pyfunc',func=customDistance)
# 	nbrs.fit(trainingSet)
# 	val=nbrs.kneighbors(trainingSet[0])
# 	return nbrs
# 	# distances, indices = nbrs.kneighbors(trainingSet)
# 	# return distances, indices

if __name__ == "__main__":
	data1 = [2, 2, 2]
	data2 = [4, 4, 4]
	distance = customDistance(data1, data2)
	print 'Distance: ' + repr(distance)

	trainSet = [[2, 2, 2], [4, 4, 4]]
	testInstance = [5, 5, 5]
	k = 1
	neighbors = getKnnNeighbors(trainSet, 1)
	print(neighbors)
