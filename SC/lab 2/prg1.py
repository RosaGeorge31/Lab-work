import csv
from random import shuffle
import math
import numpy as np
def feedforward(x,X):
		ans = [0 for i in range(5)]
		len(x)
		len(X)
		# for i in range(5):
		# 	s=0
		# 	for j in range(len(x)):
		# 		s+=x[j]*X[j][i]
		# 	ans[i] = s
		return ans

mat = []
Reader = csv.reader(open('IRIS.csv', newline=''), delimiter=',')
print('Reading the dataset...\n\n')
for row in Reader:
	mat.append(row)
mat = mat[1:]
max_iter = 1000
c=1
shuffle(mat)
y = []
new = [[1 for i in range(len(mat[0])-1)] for i in range(len(mat)) ]
for i in range(len(mat)):
	for j in range(len(mat[i])):
		if j==4:
			if mat[i][j]=='Iris-versicolor':
				y.append(1)
			if mat[i][j]=='Iris-setosa':
				y.append(0)
		else:
			new[i][j] = float(mat[i][j])
n = len(new)
alr = 0.2
test = (9*n)//10
length = n-test
X_train = new[:test]
Y_train = y[:test]
max_iter=10
c=1
X_test = new[test:]
Y_test = y[test:]
threshold = 1
error = [1 for i in range(len(X_train))]
checker = [0 for i in range(len(X_train))]
num_ft = len(X_train[0])
Iwts = [[1/(5*num_ft) for u in range(num_ft)] for _ in range(5)]
Hwts = [1/5 for u in range(5)]

N = len(X_train)

while c!=max_iter:
	c+=1
	
	val = 0
	# for row in X_train:
	hidden = feedforward(X_train[0],Iwts)
	print(hidden)

	
# print(wts)
# correct = 0
# for i in range(len(X_test)):
# 	s = wts[0]
# 	for j in range(1,len(wts)):
# 		s += X_test[i][j]*wts[j]
# 	if s>=1:
# 		ynow = 1
# 	else:
# 		ynow = 0
# 	if Y_test[i] == ynow:
# 		correct+=1
	
# print('Accuracy = ' + str((correct*100)/length))
# print(c)
