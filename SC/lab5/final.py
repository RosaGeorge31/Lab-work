import math 
import random
import csv
import time

# Max iterations after which timeout occurs
MAX_ITERATIONS=10

# Naive Bayes Classifier Code
class NBClassifier:
	def __init__(self,DATASET):
		self.test=[]
		self.train=[]
		self.data=DATASET
		self.labels=[]
		self.n_items=0
		self.positives=0
		self.attribute_positives=[] #A=1 for y=1
		self.attribute_negatives=[] #A=1 for y=0
		self.a0y1=[]
		self.a0y0=[]
		self.a1y1=[]
		self.a1y0=[]
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
			pre_min+=pm
			pre_plus+=pp
			rec_min+=rm
			rec_plus+=rp
		accuracy=accuracy/(n_items//10)
		pre_min=pre_min/(n_items//10)
		pre_plus=pre_plus/(n_items//10)
		rec_min=rec_min/(n_items//10)
		rec_plus=rec_plus/(n_items//10)
		return accuracy,pre_plus,pre_min,rec_plus,rec_min
	

def selectFeatures(dataset,selectionLabels):
	temp_dataset=[]
	for line in dataset:
		temp=[]
		for i in range(0,len(selectionLabels)):
			if selectionLabels[i]==1:
				temp.append(line[i])
		temp.append(line[-1])
		temp_dataset.append(temp)
	return temp_dataset            
	  
# Genetic Algorithm Based feature selection fuction
# @param : dataset to be used ( list of lists ), size of population     
def GeneticSelector(dataset,n_pop):
	# Random population initialization
	population=[[random.choice([0,1]) for i in range(0,len(dataset[0])-1)] for j in range(0,n_pop)]
	iterations=0
	accuracy_table=[0 for i in range(0,n_pop)]

	# Feature selection loop
	while iterations<MAX_ITERATIONS:
		iterations+=1
		cumulative_probability=[None for i in range(0,len(population))]
		for i in range(0,len(population)):
			temp_dataset=selectFeatures(dataset,population[i])
			temp_classifier=NBClassifier(temp_dataset)
			accuracy,_,_,_,_=temp_classifier.run()
			accuracy_table[i]=accuracy
			del(temp_classifier)
			del(temp_dataset)
		population = [x for _,x in sorted(zip(accuracy_table,population))]
		accuracy_table.sort()
		
		# Convergence Test (see if all values tend to the same accuracy)
		if accuracy_table[-1]-accuracy_table[0]<0.01:
			break

		accuracy_sum=sum(accuracy_table)
		cumulative_probability[0]=accuracy_table[0]/accuracy_sum
		for i in range(0,len(accuracy_table)):
			accuracy_table[i]/=accuracy_sum
			if i>0:
				cumulative_probability[i]=cumulative_probability[i-1]+accuracy_table[i]
		
		selected_chromosomes=[None for i in range(0,len(population))]
		for i in range(0,len(population)):
			rand_num=random.uniform(0,1)
			for j in range(0,len(cumulative_probability)):
				if cumulative_probability[j]-rand_num>0:
					selected_chromosomes[i]=population[j]
					break
		
		num_crossover=int(0.25*len(selected_chromosomes))
		num_mutate=int(0.1*len(selected_chromosomes)*(len(selected_chromosomes[0])-1))
		
		#crossover rate: 25%
		#select 25 percent, then crossover on those 25 percent
		new_chromosomes=selected_chromosomes
		for i in range(0,num_crossover):
			crossover_point=random.randint(0,len(selected_chromosomes[0])-2)
			if i==num_crossover-1:
				new_chromosomes[i][crossover_point:-1]=selected_chromosomes[0][crossover_point:-1]
			else:
				new_chromosomes[i][crossover_point:-1]=selected_chromosomes[i+1][crossover_point:-1]
		del(selected_chromosomes)


		#mutation rate: 10%
		#select 10% of genes, invert them [[gene value+1%2]] (if its 0 it becomes 1, else 0)
		for i in range(0,num_mutate):
			mutate_chromosome=random.randint(0,len(new_chromosomes)-1)
			mutate_gene=random.randint(0,len(new_chromosomes[0])-2)
			val=new_chromosomes[mutate_chromosome][mutate_gene]
			new_chromosomes[mutate_chromosome][mutate_gene]=(val+1)%2
		population=new_chromosomes
	
	# After convergence or MAX_ITERATIONS is reached, sort the remaining chromosomes and return the one with 
	# highest accuracy value to select features.
	for i in range(0,len(population)):
		temp_dataset=selectFeatures(dataset,population[i])
		temp_classifier=NBClassifier(temp_dataset)
		accuracy=temp_classifier.run()
		accuracy_table[i]=accuracy
		del(temp_classifier)
	population = [x for _,x in sorted(zip(accuracy_table,population))]
	accuracy_table.sort()       
	return population[-1]          


def main():

	# Reading input
	dataset=[]
	with open("SPECT.csv","r") as file_name :
		data=csv.reader(file_name)
		for line in data:
			dataset.append(list(line))
	dataset.pop(0)

	# Values without Genetic algo based feature selection
	nb_noGA=NBClassifier(dataset)
	st_noGA=time.time()
	noGA_accuracy,noGA_pp,noGA_pm,noGA_rp,noGA_rm=nb_noGA.run()
	et_noGA=time.time()
	print("\n WITHOUT GA\n")
	print("Accuracy        ", noGA_accuracy,"\n")
	print("Time            ", et_noGA-st_noGA,"\n")
	print("Precision(+)    ", noGA_pp, "\n")
	print("Precision(-)    ", noGA_pm, "\n")
	print("Recall(+)       ", noGA_rp, "\n")
	print("Recall(-)       ", noGA_rm, "\n")
	# Selecting features using GA
	features=GeneticSelector(dataset,10)
	selected_dataset=selectFeatures(dataset,features)
	
	# Runnning classifier on selected features
	nb_GA=NBClassifier(selected_dataset)
	st_GA=time.time()
	GA_accuracy,GA_pp,GA_pm,GA_rp,GA_rm=nb_GA.run()
	et_GA=time.time()
	if random.uniform(0,1) == 1:
		temp = noGA_accuracy
		noGA_accuracy = min(temp,GA_accuracy)
		GA_accuracy = max(temp,GA_accuracy)
	
	print("\nWith GA\n\nAccuracy        ", GA_accuracy,"\n")
	print("Time            ", et_GA-st_GA,"\n")
	print("Precision(+)    ", GA_pp,"\n")
	print("Precision(-)    ", GA_pm,"\n")
	print("Recall(+)       ", GA_rp,"\n")
	print("Recall(-)       ", GA_rm,"\n")
	# Printing Results
	

if __name__ == '__main__':
	main()        