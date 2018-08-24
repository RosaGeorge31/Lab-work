import csv
from random import shuffle
mat = []
Reader = csv.reader(open('IRIS.csv', newline=''), delimiter=',')
for row in Reader:
	mat.append(row)
mat = mat[1:]
shuffle(mat)
y = []
new = [[1 for i in range(len(mat[0]))] for i in range(len(mat)) ]
for i in range(len(mat)):
	for j in range(len(mat[i])):

		if j==4:
			if mat[i][j]=='Iris-versicolor':
				y.append(1)
			if mat[i][j]=='Iris-setosa':
				y.append(0)
		else:
			new[i][j+1] = float(mat[i][j])
n = len(new)
test = (9*n)//10
X_train = new[:test]
Y_train = y[:test]
X_test = new[test:]
Y_test = y[test:]
print(Y_train)
num_ft = len(X_train[0])
wts = [1/(num_ft) for u in range(num_ft)]
output = []
for i in range(len(X_train)):
	s = 0
	for j in range(len(wts)):
		s +=X_train[i][j]*wts[j]
	output.append(s)
	if s<=2.6:
		output.append(0)
	else:
		output.append(1)
print(output==Y_train)