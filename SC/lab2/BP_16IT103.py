import csv
import random
import math


#### MULTI LAYER PERCEPTRON CODE ####

#### VERY IMPORTANT NOTE #####

# I am assuming that all training tuples in the csv
# files are such that the class label is the last attribute
# or last column of the csv file.
# In this example SPECT.csv requires the first column
# to be moved to the last position before running this code

#Authored by: Aditi Rao

learning_rate=0.2

class InputNode:

	def __init__(self,ID=0):
		self.id=ID
		self.input=0		#Remember to update before every iteration!
		self.weights=[]
		self.output=0
		self.layer=0
		self.error=0

	def fire(self):
		self.output=self.input

class HiddenNode:

	def __init__(self,ID=0,BIAS=1):
		global learning_rate
		self.learning_rate=learning_rate
		self.id=ID
		self.inputs=[]
		self.weights=[]
		self.bias=BIAS
		self.output=0
		self.error=0
		self.forward_error=0
		self.forward_weight=0

	def fire(self):
		net_input=self.bias
		for i in range(0,len(self.inputs)):
			net_input+=self.inputs[i]*self.weights[i]
		self.output=1/(1+math.exp(-net_input))

	def updates(self):
		self.error=self.output*(1-self.output)*self.forward_error*self.forward_weight
		for i in range(0,len(self.weights)):
			self.weights[i]+=self.learning_rate*self.error*self.inputs[i]
		self.bias+=self.learning_rate*self.error

class OutputNode:

	def __init__(self,LAYER=0,BIAS=1):
		global learning_rate
		self.learning_rate=learning_rate
		self.inputs=[]
		self.weights=[]
		self.layer=LAYER
		self.error=0
		self.output=0
		self.target=None		#Remember to update this before every iteration!
		self.bias=BIAS

	def fire(self):
		net_input=self.bias
		for i in range(0,len(self.inputs)):
			net_input+=self.inputs[i]*self.weights[i]
		self.output=1/(1+math.exp(-net_input))
		self.error=self.output*(1-self.output)*(self.target-self.output)

	def updates(self):
		for i in range(0,len(self.weights)):
			self.weights[i]+=self.learning_rate*self.error*self.inputs[i]
		self.bias+=self.learning_rate*self.error



class MultiLayerPerceptron:
	def __init__(self,FILE=None,NHIDDEN=0):
		self.max_iterations=500
		self.nhidden=NHIDDEN
		self.file=FILE
		self.test=[]
		self.train=[]
		self.labels=[]
		self.inputs=[]
		self.hidden=[]
		self.outputs=[]
		self.data=[]

		#Reading in the data for the perceptron
		with open(self.file,"r") as file_name :
			data=csv.reader(file_name)
			for line in data:
				self.data.append(list(line))
			attributes=self.data.pop(0)
			random.shuffle(self.data)
			#for i in range(0,int(len(self.train)*0.1)):
			#	self.test.append(self.train.pop())
			#print("\nPerceptron Creation in Progress...")
			#print("\nTest set:",len(self.test),"values. Train set:",len(self.train),"values")
			n_items=len(self.data[0])-1
			for item in self.data:
				self.labels.append(item[-1])
			self.labels=list(set(self.labels))
		#print("Classes: ",self.labels,"\n")

		#Creating various nodes
		#print("\nCreating input layer nodes...")
		self.inputs=[InputNode(i) for i in range(0,len(self.data[0])-1)]
		#print(len(self.inputs),"input nodes created")
		#print("Creating Hidden layer nodes....")
		self.hidden=[HiddenNode(i) for i in range(0,self.nhidden)]
		#print(len(self.hidden),"hidden layer nodes created")
		#print("Creating output nodes...")
		self.outputs.append(OutputNode(self.nhidden+1))
		#print(len(self.outputs),"output nodes created")

		#Initializing weights and biases at each node
		for node in self.hidden:
			node.weights=[1/((len(self.data[0])-1)*5) for i in range(0,len(self.data[0])-1)]
			node.bias=1/(len(self.outputs)+len(self.hidden))
		for node in self.outputs:
			node.weights=[0.2 for i in range(0,len(self.hidden))]
			node.bias=1/(len(self.outputs)+len(self.hidden))
		#print("\nPerceptron Created Successfully!")

	def training(self):
		#print("Starting training process....")
		trained=True
		for i in range(0,self.max_iterations):
			for line in self.train:
				for i in range(0,len(self.train[0])-1):
					self.inputs[i].input=float(line[i])
				self.outputs[0].target=self.labels.index(line[-1])
				updated_inputs=[]
				for node in self.inputs:
					node.fire()
					updated_inputs.append(node.output)
				#print(updated_inputs)
				#print(self.outputs[0].target)
				updated_hidden_layer=[]
				for node in self.hidden:
					node.inputs=updated_inputs
					node.fire()
					updated_hidden_layer.append(node.output)
				for node in self.outputs:
					node.inputs=updated_hidden_layer
					node.fire()
				self.update_all()
		#print("Training Complete")

	def update_all(self):
		for node in self.outputs:
			node.updates()
		for i in range(0,len(self.hidden)):
			self.hidden[i].forward_error=self.outputs[0].error
			self.hidden[i].forward_weight=self.outputs[0].weights[i]
			self.hidden[i].updates()

	def classify(self,num):
		if num>=0.5:
			return self.labels[1]
		return self.labels[0]

	def testing(self):
		count=0
		tp=0.01
		tn=0.01
		fp=0.01
		fn=0.01
		results=[]
		for i in range(0,len(self.test)):
			line=self.test[i]
			predicted=None
			for i in range(0,len(self.train[0])-1):
				self.inputs[i].input=float(line[i])
			self.outputs[0].target=self.labels.index(line[-1])
			updated_inputs=[]
			for node in self.inputs:
				node.fire()
				updated_inputs.append(node.output)
			#print(updated_inputs)
			#print(self.outputs[0].target)
			updated_hidden_layer=[]
			for node in self.hidden:
				node.inputs=updated_inputs
				node.fire()
				updated_hidden_layer.append(node.output)
			for node in self.outputs:
				node.inputs=updated_hidden_layer
				node.fire()
				if node.output>0.5:
					predicted=self.labels[1]
				else:
					predicted=self.labels[0]
				if predicted==line[-1]:
					count+=1
					if predicted==self.labels[1]:
						tp+=1
					else:
						tn+=1
				else:
					if predicted==self.labels[1]:
						fp+=1
					else:
						fn+=1
		return count/len(self.test)*100,tp/(tp+fp),tp/(tp+fn),tn/(tn+fn),tn/(tn+fp) #Accuracy, Precision(+), Recall(+), Precision (-), Recall (-)
	def run(self):
		accuracy,pre_plus,rec_plus,pre_min,rec_min=0,0,0,0,0
		n_items=len(self.data)
		#print(n_items//10,n_items)
		for i in range(0,n_items//10):
			self.test=self.data[i*10:(i+1)*10]
			self.train=self.data[0:i*10]+self.data[(i+1)*10:n_items]
			self.training()
			acc,pp,rp,pm,rm=self.testing()
			accuracy+=acc
			pre_plus+=pp
			pre_min+=pm
			rec_plus+=rp
			rec_min+=rm
		accuracy=accuracy/(n_items//10)
		pre_min=pre_min/(n_items//10)
		pre_plus=pre_plus/(n_items//10)
		rec_min=rec_min/(n_items//10)
		rec_plus=rec_plus/(n_items//10)
		print("Accuracy:",accuracy,"\nPrecision\n(+):",pre_plus,"\n(-):",pre_min,"\nRecall\n(+):",rec_plus,"\n(-):",rec_min,"\n")
def main():

	print("DATASET: IRIS.csv")
	mlp=MultiLayerPerceptron("IRIS.csv",5)
	mlp.run()

	print("\n\n\nDATASET: SPECT.csv")
	mlp=MultiLayerPerceptron("SPECT.csv",5)
	mlp.run()



if __name__ == '__main__':
	main()
