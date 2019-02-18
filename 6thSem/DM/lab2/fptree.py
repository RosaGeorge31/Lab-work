import csv

def permute(xs, low=0):
    if low + 1 >= len(xs):
        yield xs
    else:
        for p in permute(xs, low + 1):
            yield p        
        for i in range(low + 1, len(xs)):        
            xs[low], xs[i] = xs[i], xs[low]
            for p in permute(xs, low + 1):
                yield p        
            xs[low], xs[i] = xs[i], xs[low]

def second(elem):
	return elem[1]

class Node:

	def __init__(self,val):
		self.supportCount = 1
		self.value = val
		self.next = []
		self.parent = None
		
class FPTree:

	def __init__(self,ms):
		self.Ck = []
		self.transactions = []
		self.Lk = []
		self.minSupport = ms 
		self.set2 = []
		self.set1 = []
		self.root = Node('')
		self.nodeAddrs = {}
		self.conditionalFP = []

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

	def check_common(self,first,second,k):
		temp = second[:k]
		if first == temp:
			return True
		return False


	def find_most_frequent(self,k):
		Lk = []
		t = []
		for i in range(len(self.Ck)):
			count = self.get_count(self.Ck[i],self.transactions)
			if count >= self.minSupport:
				Lk.append(self.Ck[i])
				t.append((self.Ck[i],count))
		return Lk,t

		
	def checkPresent(self,item,itemset):
		if len(itemset)==0:
			return False
		for items in itemset:
			count = 0
			for elem in item:
				if elem in items:
					count+=1
			if count == len(item):
				return True
		return False

	def printTree(self,node):
		if node is None:
			return
		if node.value!='':
			print(str(node.value) + ' : ' + str(node.supportCount))
			if node.parent is not None:
				print('Parent: ' + node.parent.value)
		for nodes in node.next:
			self.printTree(nodes)
		

	def reorderTransactions(self,items):
		items.sort(reverse=True,key=second)
		tempTransactions = []
		temp = []
		maxlen = 0
		for item in items:
			temp.append(item[0])
		items = temp
		for transaction in self.transactions:
			maxlen = max(maxlen,len(transaction))
			temp = []
			for item in items:
				if item[0] in transaction:
					temp.append(item[0])
			tempTransactions.append(temp)
		self.transactions = tempTransactions

	def isRootNext(self,node):
		if node in self.root.next:
			return True
		return False

	def getPath(self,node):
		if self.isRootNext(node):
			return None
		ptr = node
		path = []
		
		path.append(ptr.supportCount)
		ptr = ptr.parent
		while ptr!=None:
			path.append(ptr.value)
			ptr = ptr.parent
		return path[::-1]

	def patterns(self):
		for item in self.conditionalFP:
			for i in range(1,len(item)):
				for j in range(len())

	def checkNext(self,val,itemset):
		if len(itemset)==0:
			return None
		for addr in itemset:
			if addr.value == val:
				return addr
		return None

	def treeGeneration(self):
		for transaction in self.transactions:
			c = 0
			if len(self.root.next)==0 :
				for item in transaction:
					if c==0:
						newNode = Node(item)
						self.root.next.append(newNode)
						print(1)
						print(item)
						self.nodeAddrs[item] = []
						self.nodeAddrs[item].append(newNode)
						head = newNode
						c=1
					else:
						newNode = Node(item)
						newNode.parent = head
						print(2)
						print(item)
						self.nodeAddrs[item] = []
						self.nodeAddrs[item].append(newNode)
						head.next.append(newNode)
						head = newNode
			else:
				flag=False
				for nodes in self.root.next:
					if nodes.value==transaction[0]:
						nodes.supportCount+=1
						flag=True
						if len(transaction)==1:
							break

						node = 	self.checkNext(transaction[1],nodes.next)

						if node != None:
							ptr=1
							while node!=None or ptr==len(transaction):
								node.supportCount+=1
								nodes = node
								ptr+=1
								if ptr==len(transaction):
									flag=True
									break
								node = self.checkNext(transaction[ptr],nodes.next)
				
							if ptr==len(transaction):
								flag=True
								break

							while ptr!=len(transaction):
								newNode = Node(transaction[ptr])
								self.nodeAddrs[transaction[ptr]].append(newNode)
								nodes.next.append(newNode)
								newNode.parent = nodes
								nodes = newNode
								ptr+=1
							flag=True
							break
						else:
							ptr =1
							head = self.root.next[0]
							while ptr!=len(transaction):
								newNode = Node(transaction[ptr])
								self.nodeAddrs[transaction[ptr]].append(newNode)
								head.next.append(newNode)
								newNode.parent = head
								head = newNode
								ptr+=1
							flag=True
							break
				
				if flag == False:
					newNode = Node(transaction[0])
					self.nodeAddrs[transaction[0]].append(newNode)
					self.root.next.append(newNode)
					head = newNode
					if len(transaction)==1:
						break
					ptr =1 
					while ptr!=len(transaction):
						newNode = Node(transaction[ptr])
						self.nodeAddrs[transaction[ptr]].append(newNode)
						head.next.append(newNode)
						newNode.parent = head
						head = newNode
						ptr+=1

	def run(self):
		k=1
		self.Lk, temp = self.find_most_frequent(k)
		self.reorderTransactions(temp)
		self.treeGeneration()
		self.printTree(self.root)
		print(self.nodeAddrs)
		for key,item in self.nodeAddrs.items():
			temp = []
			flag = False
			temp.append(key)
			for node in item:
				path = self.getPath(node)
				if path is not None:
					flag = True
					temp.append(path)
			if flag:
				self.conditionalFP.append(temp)
		print(self.conditionalFP)
		self.patterns()

def main():

	minSupport = int(input('Enter the value of the minimum support:\n'))
	a = FPTree(minSupport)
	a.readFromFile('test.csv')
	a.run()
   
if __name__ == '__main__':
	main()
