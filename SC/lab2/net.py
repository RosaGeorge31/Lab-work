import csv
from math import exp
from random import random


def sigmoid(activation):
	return 1.0 / (1.0 + exp(-activation))


def forward_propagate(network, row):
	inputs = row

	for layer in network:
		new_inputs = []
		for neuron in layer:
			activation = activate(neuron['wts'], inputs)
			neuron['output'] = sigmoid(activation)
			new_inputs.append(neuron['output'])
			
		inputs = new_inputs
	return new_inputs   

def defaultNetwork(numInputs, numOutputs, numHidden):
	network = list()
	hidden_layer = [{'wts':[random() for i in range(numInputs + 1)]} for i in range(numHidden)]
	network.append(hidden_layer)
	output_layer = [{'wts':[random() for i in range(numHidden + 1)]} for i in range(numOutputs)]
	network.append(output_layer)
	
	return network

def activate(wts, inputs):
	count=0
	activation = wts[-1]
	for i in range(len(wts)-1):
		activation += wts[i] * inputs[i]

	return activation

def sigmoid_derivative(output):
	return output * (1.0 - output)

def backward_propagate_error(network, expected):
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['wts'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(expected[j] - neuron['output'])
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * sigmoid_derivative(neuron['output'])

def update_wts(network, row, l_rate):
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['wts'][j] += l_rate * neuron['delta'] * inputs[j]
			neuron['wts'][-1] += l_rate * neuron['delta']

def predict(network, row):
	outputs = forward_propagate(network, row)
	return outputs.index(max(outputs))

def train_network(network,train_set,numOutputs,l_rate):
	sum_error=0
	for row in train_set:
			outputs = forward_propagate(network, row)
			expected = [0 for i in range(numOutputs)]
			expected[row[-1]] = 1
			sum_error += sum([(expected[i]-outputs[i])**2 for i in range(len(expected))])
			backward_propagate_error(network, expected)
			update_wts(network, row, l_rate)
	print(sum_error)

def toFloat(rows,pos):
	for row in rows:
		for index,item in enumerate(row):
			if index!=pos:
				row[index]=float(item)
	return rows

def expected(rows,pos):
	class_values=[]
	hash_map={}
	actual=[None for i in range(len(rows))]
	for row in rows:
		if row[pos] not in class_values:
			class_values.append(row[pos])
	count=0
	for items in class_values:
		hash_map[items]=count
		count+=1
	for i in range(len(rows)):
		rows[i][pos] = hash_map[rows[i][pos]]
	return rows

def loadData():
	filename = "IRIS.csv"
	rows = []
	with open(filename,"r") as csvfile:
		csvreader = csv.reader(csvfile)
		field= next(csvreader)
		pos=field.index("class" or "Class")
		for row in csvreader:
			rows.append(row)

	
	numInputs = len(rows[0])-1
	numOutputs = len(set([row[-1] for row in rows]))
	

	rows=expected(rows,numInputs)
	
	rows=toFloat(rows,numInputs)
	
	network = defaultNetwork(numInputs, numOutputs,5)

	
	fold  = 9*len(rows)//10
	train_set = rows[:fold]
	test_set = rows[fold:]
	tp=0
	tn=0
	fp=0
	fn=0
	l_rate=0.1
	train_network(network,train_set,numOutputs,l_rate)
	for layer in network:
		count =0
		accuracy=0
		Matrix = [[0 for x in range(3)] for y in range(3)] 
		for row in rows:
			prediction = predict(network, row)
			Matrix[int(prediction)][int(row[-1])]=Matrix[int(prediction)][int(row[-1])]+1
			print('Expected=%d, Got=%d' % (row[-1], prediction))
			count=count+1
			if(row[-1]==prediction):
				accuracy=accuracy+1
				if predicted==labels[1]:
						tp+=1
					else:
						tn+=1
				else:
					if predicted==labels[1]:
						fp+=1
					else:
						fn+=1
	print("Accuracy " + str(accuracy*100/count) + '%')
	print("Precision(+)=",tp/(tp+fp))
	print("Recall(+)=",tp/(tp+fn))
	print("Precision(-)=",tn/(tn+fn))
	print("Recall(-)=",tn/(tn+fp),"\n\n\n\n")

def main():
	loadData()

if __name__ == '__main__':
	main()