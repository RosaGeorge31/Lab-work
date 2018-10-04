import csv
import random
import math
from random import shuffle
class KNN:
	def __init__(self,dta):
		self.data = dta
	def calcDist(self,t1,t2):
		ans = sqrt(pow(t1[0]-t2[0],2)+pow(t1[1]-t2[1],2))
		return ans


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
	print(new)



if __name__ == '__main__':
	main()