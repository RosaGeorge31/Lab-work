import csv
from random import shuffle
import math
mat = []
Reader = csv.reader(open('SPECT.csv', newline=''), delimiter=',')
for row in Reader:
	mat.append(row)
mat = mat[1:]
max_iter = 1000
c=1
shuffle(mat)
y = []
new = [[1 for i in range(len(mat[0]))] for i in range(len(mat)) ]
for i in range(len(mat)):
	for j in range(len(mat[i])):
		if j==0:
			if mat[i][j]=='Yes':
				y.append(1)
			if mat[i][j]=='No':
				y.append(0)
		else:
			new[i][j] = float(mat[i][j])
n = len(new)
alr = 0.3
test = (9*n)//10
length = n-test
X_train = new[:test]
Y_train = y[:test]
X_test = new[test:]
Y_test = y[test:]
threshold = 0.35
error = [1 for i in range(len(X_train))]
checker = [0 for i in range(len(X_train))]
num_ft = len(X_train[0])
wts = [1/(num_ft) for u in range(num_ft)]
row = 0
N = len(X_train)


while error!=checker and c!=max_iter:
	ind = 0
	for row in X_train:
		
		s = wts[0]
		for j in range(1,len(wts)):
			s+=row[j]*wts[j]
		if s>=1:
			prediction = 1
		else:
			prediction = 0
		error[ind] = Y_train[ind]-prediction
		

		for j in range(1,len(wts)):
			wts[j] += error[ind] * alr * row[j]
		wts[0] += error[ind] * alr
		ind+=1
	c+=1

correct = 0
for i in range(len(X_test)):
	s = wts[0]
	for j in range(1,len(wts)):
		s += X_test[i][j]*wts[j]
	if s>=1:
		ynow = 1
	else:
		ynow = 0
	if Y_test[i] == ynow:
		correct+=1
	
	
print('Accuracy = ' + str((correct*100)/length))
print(wts)
