import csv
from random import shuffle
import math

class Perceptron:
	def __init__(self,file=None,iterations=1000,learning_rate=0.2):
		self.train=[]
		self.test=[]
		self.labels=[]
		self.weights=[]
		self.iterations=iterations
		self.MAX_ITERATIONS=1000
		self.LEARNING_RATE=learning_rate
		self.file=file

	def read_datafile(self):
		mat = []
		Reader = csv.reader(open(self.file, newline=''), delimiter=',')
		print('Reading the dataset...\n\n')
		for row in Reader:
			mat.append(row)
		mat = mat[1:]
		c=1
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
		return [new,y]

	def main_func(self,X_train,Y_train,X_test,Y_test):
	  
		threshold = 1
		error = [1 for i in range(len(X_train))]
		checker = [0 for i in range(len(X_train))]
		num_ft = len(X_train[0])
		wts = [1/(num_ft) for u in range(num_ft)]
		row = 0
		n = len(X_train)
		
		test = (9*n)//10
		length = n-test
		print('Training the dataset with length of training set = ', len(X_train))
		c=0
		while error!=checker and c!=self.MAX_ITERATIONS:
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
					wts[j] += error[ind] * self.LEARNING_RATE * row[j]
				wts[0] += error[ind] * self.LEARNING_RATE
				ind+=1
			c+=1
		print('\nTraining complete! Number of iterations : ' + str(c))
		print('Weights are:')
		print(wts)
		print('\nTesting the dataset with size of test set = ', len(X_test))
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
			
		print('\n\nAccuracy = ' + str((correct*100)/len(X_test))+'%')

def main():
	iris_perceptron=Perceptron('IRIS.csv')
	val= iris_perceptron.read_datafile()
	data = val[0]
	y=val[1]
	
	n = len(data)
	for i in range(0,n//10):
			test=data[i*10:(i+1)*10]
			train=data[0:i*10]+data[(i+1)*10:n]
			y_test = y[i*10:(i+1)*10]
			Y_train = y[0:i*10]+y[(i+1)*10:n]
			iris_perceptron.main_func(train,Y_train,test,y_test)


	spect_perceptron=Perceptron('SPECT.csv')
	val= spect_perceptron.read_datafile()
	data = val[0]
	y=val[1]
	
	n = len(data)
	for i in range(0,n//50):
			test=data[i*50:(i+1)*50]
			train=data[0:i*50]+data[(i+1)*50:n]
			y_test = y[i*50:(i+1)*50]
			Y_train = y[0:i*50]+y[(i+1)*50:n]
			spect_perceptron.main_func(train,Y_train,test,y_test)

if __name__ == '__main__':
	main()
