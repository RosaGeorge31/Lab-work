import csv

import sys

from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

class Apriori_Algo:

	def __init__(self):
		self.Ck = []
		self.count_Ck = {}
		self.transactions = []
		self.Lk = []
		self.uniqueLk = []

	def readFromFile(self,filename):

		with open(filename) as csv_file:
			csv_reader = csv.reader(csv_file,delimiter=',')
			for row in csv_reader:
				self.transactions.append(row)
				for i in row:
					if i not in self.Ck:
						self.Ck.append(i)


	def get_count2(self,items,candidateList):
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

	def find_most_frequent(self,minSupport):
		for i in self.Ck:
			self.count_Ck[i] = self.get_count1(i,self.transactions)
			if self.count_Ck[i] >= minSupport:
				self.Lk.append(i)
				if i not in self.uniqueLk:
					self.uniqueLk.append(i)
		self.join(self.uniqueLk,2)

	def join(self,itemSet,k):
		print(itemSet)
		temp = ([self.union(i,j) for i in itemSet for j in itemSet if len(self.union(i,j)) == k])
		print(temp)


	def union(self,i,j):
		# if len(i)!= 1 and len(j)!=1:
		#     for k in j:
		#         i.append(k)
		#     return i
		# if len(i)==1 and len(j)!=1:
		#     return j.append(i)
		# if len(j)==1 and len(i)!=1:
		#     return i.append(j)
		# return [i,j]
		L = []
		L.append(i)
		L.append(j)
		return L

def main():
	a = Apriori_Algo()
	a.readFromFile('test_dataset_1.csv')
   
	a.find_most_frequent(5)
   
if __name__ == '__main__':
	main()

