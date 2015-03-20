import math
import operator
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import DistanceMetric

def robotDistance(instance1, instance2):
	distance = 0
	for x in range(len(instance1)):
		distance += min (abs(instance1[x] - instance2[x]),abs(360 - instance1[x] + instance2[x]))
	return distance

def FitNeighbors(trainingSet,k):
	nbrs=NearestNeighbors(n_neighbors=k,metric='pyfunc',func=robotDistance)
	nbrs.fit(trainingSet)
	return nbrs

def getNeighbors(nbrs,trainingSet,testInstance,k):
	val=nbrs.kneighbors(testInstance)
	neighbors = []
	retrievedDistance=[]
	# print val
	for x in range(k):
		retrievedDistance.append( val[0][0][x])
		neighbors.append(trainingSet[val[1][0][x]])
	# assert (False)	
	return (neighbors,retrievedDistance)

trainingSet = [[1,2],[3,4],[5,6]]
testInstance = [1,2]
nbrs = FitNeighbors(trainingSet,2)
getNeighbors(nbrs,trainingSet,testInstance,1)
