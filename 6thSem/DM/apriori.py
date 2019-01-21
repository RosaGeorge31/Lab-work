import csv


class Apriori_Algo:

	def __init__(self,ms):
		self.Ck = []
		self.transactions = []
		self.Lk = []
		self.minSupport = ms 

	def readFromFile(self,filename):
		temp = []
		with open(filename) as csv_file:
			csv_reader = csv.reader(csv_file,delimiter=',')
			for row in csv_reader:
				self.transactions.append(row)
				for i in row:
					if i not in temp:
						temp.append(i)	
		for i in temp:
			self.Ck.append([i])
		

	def get_count(self,items,candidateList):
		counter = 0
		for itemset in candidateList:
			flag=True
			for item in items:
				if item not in itemset:
					flag = False
					break
			if flag == True:
				counter+=1
		return counter

	def check_common(first,second,k):
		temp = second[:k]
		if first == temp:
			return True
		return False


	def find_most_frequent(self,k):
		self.Lk = []
		if k<=3:
			for i in range(len(self.Ck)):
				count = self.get_count(self.Ck[i],self.transactions)
				if count >= self.minSupport:
					self.Lk.append(self.Ck[i])
			print(self.Lk)
		else:
			print('to be added')
			return
				
				#to add
		
		self.join(self.Lk,k+1)

		# for i in self.Ck:
		# 	self.count_Ck[i] = self.get_count(i,self.transactions)
		# 	if self.count_Ck[i] >= minSupport:
		# 		self.Lk.append(i)
		# 		if i not in self.uniqueLk:
		# 			self.uniqueLk.append(i)
		# self.join(self.uniqueLk,2)

	def join(self,itemSet,k):
		if k==2:
			temp = []
			for i in range(len(itemSet)-1):
				for j in range(i+1,len(itemSet)):
					temp.append([itemSet[i][0],itemSet[j][0]])
			self.Ck = temp
			self.find_most_frequent(k+1)
		else:
			temp = []
			for i in range(len(itemSet)-1):
				firstCommon = itemset[i][:(k-2)]
				for j in range(i+1,len(itemSet)):
					if check_common(firstCommon, itemset[j],k-2) == True:
						for k2 in range(k-,len(itemset[0])):
							temp.append(firstCommon.append(itemset[i][k2]))


def main():
	a = Apriori_Algo(2)
	a.readFromFile('test_dataset_1.csv')
	a.find_most_frequent(1)
   
if __name__ == '__main__':
	main()

