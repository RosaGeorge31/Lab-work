import csv
from collections import defaultdict
import collections
from itertools import permutations 

def find_frequent_itemsets(transactions, minimum_support, include_support=False):
    
    items = defaultdict(lambda: 0)

    for transaction in transactions:
        for item in transaction:
            items[item] += 1
    items = dict((item, support) for item, support in items.iteritems() if support >= minimum_support)
    return items

def ordered_item_set(transactions , result):
	final=[]
	for transaction in transactions:
		ordered_set=[]
		for item in result:
			if item[0] in transaction:
				ordered_set.append(item[0])
		final.append(ordered_set)
	#print "final=",final
	return final 

class FPNode(object):
    def __init__(self,item, count=1): 
        self.item = item
        self.count = count
        self.parent = None
        self.children = []
        self.neighbor = []

   
class FPtree(object):

	def __init__(self):
	        self.root = FPNode(None)
	        self.point = self.root
			
	
	def FPtree_gen(self,ordered_set,min_sup,min_conf,dataset):
		path=defaultdict(list)
		
		for item in ordered_set[0]:
			next_point = FPNode(item,1)
			self.point.children.append(next_point)
			next_point.parent = self.point

			if next_point.item not in path.keys():
				path[next_point.item]=[next_point]
			else:
				path[next_point.item].append(next_point)

			self.point = next_point
		print "********************"
		for transaction in ordered_set[1:]:
			print "transaction : ",transaction
			self.point = self.root
			for item in transaction:
				flag=0
				print "item :",item
				print "parent of item" , self.point.item
				for child in self.point.children:
					if item == child.item:
						child.count+=1
						
						flag=1
						print "node item :" , self.point.item , self.point.count 
						print "children:"
						for child1 in self.point.children:
							print child1.item ,":", child1.count
						child.parent = self.point
						self.point = child
						print "next parent:", self.point.item
				if flag ==0 :		
					newnode = FPNode(item,1)
					self.point.children.append(newnode)
					if newnode.item not  in path:
						path[newnode.item]=[newnode]
					else:
						path[newnode.item].append(newnode)
					print "parent item :" , self.point.item , self.point.count 
					print "children:"
					for child1 in self.point.children:
						print child1.item ,":", child1.count
					newnode.parent = self.point
					self.point = newnode
					#print self.point.item
		print "##############################################################"
		self.path_node(path,min_sup,min_conf,dataset)

	def path_node(self,path,min_sup,min_conf,dataset):
		for key,value in path.items():
			print key
			for v in value:
				print v.item ,v.count
		print "################################################################"
		table=[]
		
		for key,list_path in path.items():
			final=[]
			conditional_pattern=defaultdict()
			final.append(key)
			for pointer in list_path:
				path_root=[]
				c = pointer.count
				point = pointer.parent
				while point.parent is not None:
					path_root.append(point.item)
					point = point.parent
				path_root.reverse()
				#print key,path_root
				for letters in path_root:
					if letters not in conditional_pattern.keys():
						conditional_pattern[letters] = c
					else:
						conditional_pattern[letters] += c
			conditional_pattern = dict((item, support) for item, support in conditional_pattern.iteritems() if support >= min_sup)
			final.append(conditional_pattern)
			table.append(final)
		print table
		self.association_rules(table,min_conf,dataset)

	def association_rules(self,table,min_conf,dataset):
			rules=[]
			for items in table:
				patterns=[]
				if items[1]!={}:
					patterns.append(items[0])
					for key in items[1].keys():
						patterns.append(key)
					rules.append(patterns)
			print rules
			print(self.strong_association_rules(rules,min_conf,dataset))

	def take_count(self,dataset,item):
		count=0
		for transaction in dataset:
				if all(elem in transaction  for elem in item) or item in transaction:
					count +=1
		return count

	def strong_association_rules(self,rules,min_conf,dataset):
		count=0
		list_rules=[]
		for rule in rules:
			perm=list(permutations(rule))
			print "perm:" , perm
			perms = []
			for i in list(perm):
				 if not all(elem in perms for elem in i):
					perms.append(i)

			if len(rule)==3:
				perm=list(permutations(rule,2))
				#print "perm:" , perm
				#perms = []
				for i in list(perm):
					 if not all(elem in perms for elem in i):
						perms.append(i)

			percentage=0
			
			print "_________________________________________"
			
			for i in perms:
				if perms.index(i)%2==0:
					percentage =  self.take_count(dataset,i)/float(self.take_count(dataset,i[0]))*100
					#print i[0] , "->" , i[1:len(i)] , percentage
					existing =[]
					if percentage >= min_conf:
						existing.append(i[0])
						for j in i[1:len(i)]:
							existing.append(j)
						if existing not in list_rules:
							print i[0] , "->" , i[1:len(i)] , percentage
							count+=1
							list_rules.append(existing)
					
					percentage=self.take_count(dataset,i)/float(self.take_count(dataset,i[0:len(i)-1]))*100
					#print i[0:len(i)-1] , "->" , i[len(i)-1] , percentage
					existing =[]
					if percentage >= min_conf:
						existing.append(i[0])
						for j in i[1:len(i)]:
							existing.append(j)
								
						if existing  not in list_rules:
							print i[0:len(i)-1] , "->" , i[len(i)-1] , percentage
							count+=1
							list_rules.append(existing)
				else:
					percentage=self.take_count(dataset,i)/float(self.take_count(dataset,i[0:len(i)-1]))*100
					#print i[0:len(i)-1] , "->" , i[len(i)-1] , percentage
					existing =[]
					if percentage >= min_conf:
						existing.append(i[0])
						for j in i[1:len(i)]:
							existing.append(j)
								
						if existing  not in list_rules:
							print i[0:len(i)-1] , "->" , i[len(i)-1] , percentage
							count+=1
							list_rules.append(existing)

				#print"list_rules" , list_rules
				#print "existing:", existing
		return count-1


def main():

	with open('test_dataset_1.csv', 'rb') as f:
	    reader = csv.reader(f)
	    transactions = list(reader)
	#print(dataset)

	
	print "dataset=",transactions
	min_sup=2
	min_conf = 60

	result = []
	items = defaultdict()
	items = find_frequent_itemsets(transactions, min_sup, True)
	for itemset, support in items.iteritems():
		result.append((itemset,support))
	print "result = ",result
	result = sorted(result)
	result.sort(key=lambda v: v[1], reverse=True)
	print "result after sorting = ",result

	ordered_set = ordered_item_set(transactions,result)
	print "\nordered_item_set=" , ordered_set

	master  = FPtree()
	master.FPtree_gen(ordered_set,min_sup,min_conf,transactions)

if __name__ == '__main__':
	main()
