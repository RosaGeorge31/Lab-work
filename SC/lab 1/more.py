import csv
reader = csv.reader(open("IRIS.csv"),delimiter=",")
import random
from random import shuffle
from math import exp
from random import randrange


data=[]
c=0
for row in reader:
	if(c==0):
		c+=1
		continue
	data.append(row)
random.seed(123)
shuffle(data)

X=[]
y=[]
c=0
for row in data:
	X.append(row[:-1])
	y.append(row[-1])


unique=[]
for i in range(len(y)):
	if y[i] not in unique:
		unique.append(y[i])
for i in range(len(y)):
	y[i]=unique.index(y[i])
for i in range(len(X)):
	for j in range(len(X[0])):
		X[i][j]=float(X[i][j])
for i in range(len(X)):
	X[i]=[1]+X[i]

data=[]
for i in range(len(X)):
	data.append(X[i]+[y[i]])

thresh=0.6
n_epochs=10
alpha=0.01
# X_train=X[:90]
# X_test=X[90:]
# y_train=y[:90]
# y_test=y[90:]


def train(train):
	global n_epochs,thresh,alpha
	nf=len(X[0])
	W=[1/(nf+1) for _ in range(nf)]
	for _ in range(n_epochs):
		for te in range(len(train)):
			sum=0
			for w,x in zip(W,train[te][:-1]):
				sum+=w*x
			pred=1 if sum>=thresh else 0
			iter_error=(train[te][-1]-pred)
			for i in range(len(train[te][:-1])):
				update=alpha*iter_error*train[te][i]
				W[i]+=update
	return W


def set_threshold(W,data):
	global thresh
	avg_sum=[]
	for i in range(len(data)):
		sum=0
		for w,x in zip(W,data[i][:-1]):
			sum+=w*x
		avg_sum.append(sum)
	a_sum=0
	c=0
	for i in range(len(data)):
		if data[i][-1]==0:
			a_sum+=avg_sum[i]
			c+=1
	thresh=a_sum/c
	

def predict(W,data):
	global thresh
	y_pred=[]
	avg_sum=[]
	for i in range(len(data)):
		sum=0
		for w,x in zip(W,data[i][:-1]):
			sum+=w*x
		avg_sum.append(sum)
		pred=1 if sum>=thresh else 0
		y_pred.append(pred)
	return y_pred,avg_sum

def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0

def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for _ in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split

def evaluate_algorithm(dataset, n_folds):
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	f=1
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		actual=[]
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			actual.append(row[-1])
		W=train(train_set)
		# set_threshold(W,train_set)
		predicted ,_= predict(W,test_set)
		print(" Fold ",f)
		print("predicted :",predicted)
		print("actual :",actual)
		accuracy = accuracy_metric(actual, predicted)
		scores.append(accuracy)
		f+=1
	return scores
print(evaluate_algorithm(data,10))