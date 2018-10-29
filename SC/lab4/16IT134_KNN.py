import csv
import random
import math
from random import shuffle
class KNN:
	def __init__(self):
		self.X_train = []
		self.Y_train = []
		self.X_test = []
		self.Y_test = []
		self.classes = []
	def calcDist(self,t1,t2):
		val=0
		for i in range(len(t1)):
			val+=pow(t1[i]-t2[i],2)
		ans = math.sqrt(val)
		return ans

	def unique(list1): 

	unique_list = [] 
	for x in list1: 
		if x not in unique_list: 
			unique_list.append(x) 
	return unique_list

	def classifier(self,arr,k):
		toSort = []
		for i in range(len(self.X_train)):
			toSort.append([self.calcDist(arr,self.X_train[i]),self.Y_train[i]])
		toSort.sort(key=lambda x: x[0])
		ans = self.findClass(toSort[:k+1])
		#return self.classes[ans]
		return ans

	def findClass(self,x):
		num_ones = 0
		for i in range(len(x)):
			num_ones+= x[i][1]
		num_zeroes = len(x)-num_ones
		if num_zeroes>num_ones:
			return 0
		else:
			return 1

def main():
	
	print("DATASET: IRIS.csv")
	Reader = csv.reader(open('IRIS.csv', newline=''), delimiter=',')
	mat = []
	print('Reading the dataset...\n\n')
	for row in Reader:
		mat.append(row)
	mat = mat[1:]
	max_iter = 1000
	c=1
	shuffle(mat)
	y = []
	new = [[0 for i in range(len(mat[0])-1)] for i in range(len(mat)) ]
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			if j==4:
				if mat[i][j]=='Iris-versicolor':
					y.append(1)
				if mat[i][j]=='Iris-setosa':
					y.append(0)
			else:
				new[i][j] = float(mat[i][j])
	n=len(new)
	knn = KNN()
	fold  = 9*n//10
	knn.X_train = new[:fold]
	knn.X_test = new[fold:]
	knn.Y_train = y[:fold]
	knn.Y_test = y[fold:]
	knn.classes = unique
	classes = []
	k = int(input('Enter the value of k'))
	for i in knn.X_test:
		classes.append(knn.classifier(i,k))
	for i in range(len(knn.Y_test)):
		print(str(classes[i]) + '  ' + str(knn.Y_test[i]))

if __name__ == '__main__':
	main()