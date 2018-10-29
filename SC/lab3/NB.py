import csv
import random
import math

class NBClassifier:
	def __init__(self,FILE=None):
		self.file=FILE
		self.test=[]
		self.train=[]
		self.data=[]
		self.labels=[]
		self.n_items=0
		self.positives=0
		self.attribute_positives=[] #A=1 for y=1
		self.attribute_negatives=[] #A=1 for y=0
		self.a0y1=[]
		self.a0y0=[]
		self.a1y1=[]
		self.a1y0=[]
		with open(self.file,"r") as file_name :
			data=csv.reader(file_name)
			for line in data:
				self.data.append(list(line))
			attributes=self.data.pop(0)
			#print(len(self.data))
			random.shuffle(self.data)
			self.n_items=len(self.data[0])-1
			for item in self.data:
				self.labels.append(item[-1])
			self.labels=list(set(self.labels))
			

	def training(self):
		self.a0y1=[0 for i in range(0,len(self.train[0])-1)]
		self.a0y0=[0 for i in range(0,len(self.train[0])-1)]
		self.a1y1=[0 for i in range(0,len(self.train[0])-1)]
		self.a1y0=[0 for i in range(0,len(self.train[0])-1)]
		self.positives=0
		for item in self.train:
			if item[-1]==self.labels[1]:
				self.positives+=1
		for item in self.train:
			for i in range(0,len(item)-1):
				if item[-1]==self.labels[0]:
					if item[i]=='1': #count how many A=1 for y=0
						self.a1y0[i]+=1
					else:
						self.a0y0[i]+=1
				if item[-1]==self.labels[1]:
					if item[i]=='1': #count how many A=1 for y=1
						self.a1y1[i]+=1
					else:
						self.a0y1[i]+=1
		for i in range(0,len(self.a0y0)):
			self.a0y0[i]/=(len(self.train)-self.positives)
			self.a1y0[i]/=(len(self.train)-self.positives)
			self.a1y1[i]/=self.positives
			self.a0y1[i]/=self.positives

	def testing(self):
		correct_predictions=0
		tp,tn,fp,fn=0.01,0.01,0.01,0.01
		for item in self.test:
			pred1=self.positives/len(self.train)
			pred0=1-pred1
			for i in range(0,len(item)-1):
				if item[i]=='1':
					pred0*=self.a1y0[i]
					pred1*=self.a1y1[i]
				if item[i]=='0':
					pred0*=self.a0y0[i]
					pred1*=self.a0y1[i]
			if pred0>pred1:
				if self.labels[0]==item[-1]:
					correct_predictions+=1
					tn+=1
				else:
					fn+=1
			else:
				if self.labels[1]==item[-1]:
					correct_predictions+=1
					tp+=1
				else:
					fp+=1

		return correct_predictions/len(self.test)*100,tp/(tp+fp),tp/(tp+fn),tn/(tn+fn),tn/(tn+fp)

	def run(self):
		accuracy,pre_plus,rec_plus,pre_min,rec_min=0,0,0,0,0
		n_items=len(self.data)
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
	nbc=NBClassifier("SPECT.csv")
	nbc.run()

if __name__ == '__main__':
	main()
