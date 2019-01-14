import csv
import random
import math
import numpy as np
class NBClassifier:
	def __init__(self,listAttr):
		self.file="SPECT.csv"
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
		self.considerAttribute = listAttr
		self.considerAttribute.append(1)
		print(len(self.considerAttribute))
		with open(self.file,"r") as file_name :
			data=csv.reader(file_name)
			tmp = []
			for line in data:
				tmp.append(list(line))
			print(len(tmp[0]))
			attributes=tmp.pop(0)
			for i in range(len(tmp)):
				ls = []
				for k in range(len(tmp[0])):
					if self.considerAttribute[k]==1:
						ls.append(tmp[i][k])
				self.data.append(ls)

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
					if item[i]=='1' and self.considerAttribute[i]==1: #count how many A=1 for y=0
						self.a1y0[i]+=1
					else:
						if self.considerAttribute[i]==1:
							self.a0y0[i]+=1
				if item[-1]==self.labels[1]:
					if item[i]=='1': #count how many A=1 for y=1
						if self.considerAttribute[i]==1:
							self.a1y1[i]+=1
					else:
						if self.considerAttribute[i]==1:
							self.a0y1[i]+=1
		for i in range(0,len(self.a0y0)):
			self.a0y0[i]/=(len(self.train)-self.positives+1)
			self.a1y0[i]/=(len(self.train)-self.positives+1)
			if self.positives==0:
				self.positives=1
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
	def getAccuracy(self):
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

		return (tp + tn)/(tp + tn + fp + fn)

	def run(self):
		accuracy,pre_plus,rec_plus,pre_min,rec_min=0,0,0,0,0
		n_items=len(self.data)
		fold = (9 * n_items)//10
		# for i in range(0,n_items//10):
		# 	self.test=self.data[i*10:(i+1)*10]
		# 	self.train=self.data[0:i*10]+self.data[(i+1)*10:n_items]
		self.test=self.data[:fold]
		self.train=self.data[fold:]
		self.training()
		
	def Main_run(self):
		accuracy,pre_plus,rec_plus,pre_min,rec_min=0,0,0,0,0
		n_items=len(self.data)
		fold = (9 * n_items)//10
		# for i in range(0,n_items//10):
		# 	self.test=self.data[i*10:(i+1)*10]
		# 	self.train=self.data[0:i*10]+self.data[(i+1)*10:n_items]
		self.test=self.data[:fold]
		self.train=self.data[fold:]
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

class GeneticAlgo:
	def __init__(self,n,pop):
		self.num = n
		self.p = pop
		self.chromosomes = [list(np.random.randint(2, size=n)) for  _ in range(pop)]
		self.fitnessVals = [0 for _ in range(self.p)]
		self.currIteration = 0
		self.maxIteration = 5

	def fitness_eval(self):
		for i in range(self.p):
			nb = NBClassifier(self.chromosomes[i])
			nb.run()
			self.fitnessVals[i] = nb.getAccuracy()
		
	def selection(self):
		total = sum(self.fitnessVals)
		prob = []
		cum_fitness = []
		rand = []
		new_order = []
		
		for i in range(len(self.chromosomes)):
			prob.append(self.fitnessVals[i]/total)
			cum_fitness.append(sum(prob))
			rand.append(random.uniform(0, 1))
		for i in range(len(rand)):
			for j in range(len(cum_fitness)):
				if rand[i]<cum_fitness[j]:
					new_order.append(j)
					break
		temp = [[] for _ in range(len(new_order))]
		for i in range(len(new_order)):
			temp[i] = self.chromosomes[new_order[i]]
		self.chromosomes = temp
		


	def crossover(self,CrossOverRate,mutationRate):
		num = CrossOverRate * self.p
		chromo = []

		for i in range(int(num)):
			chromo.append(int(random.uniform(0, self.p-1)))
		temp2 = []

		pt = int(random.uniform(0,self.num-1))
		for i in range(len(chromo)):
			temp2.append(self.chromosomes[chromo[i]][:pt] +self.chromosomes[chromo[i]+1][pt:] )


		temp2.append(self.chromosomes[chromo[len(chromo)-1]][:pt] + self.chromosomes[chromo[0]][pt:])
		
		self.mutation(temp2,mutationRate)

	def mutation(self, arr,rate):
		num = self.p * self.num * rate
		rand_pts = []
		rand_chromosomes = []
		for i in range(int(num)):
			rand_pts.append(int(random.uniform(0,self.num-1)))
		
			rand_chromosomes.append(int(random.uniform(0,self.p)))
		
		for i in range(int(num)):
			if self.chromosomes[rand_chromosomes[i]][rand_pts[i]] == 1:
				self.chromosomes[rand_chromosomes[i]][rand_pts[i]] = 0
			else:
				self.chromosomes[rand_chromosomes[i]][rand_pts[i]] = 1
		




def main():
	# nbc=NBClassifier("SPECT.csv")
	# nbc.run()
	ga = GeneticAlgo(22,30)
	ga.fitness_eval()
	ga.selection()
	ga.crossover(0.25,0.10)
	
	if self.currIteration == self.maxIteration:
			nb = NBClassifier(self.chromosomes[0])
			nb.getAccuracy()
			return
	else:
		nb = NBClassifier(self.chromosomes[0])
		nb.getAccuracy()
	
	nb.Main_run()

if __name__ == '__main__':
	main()
