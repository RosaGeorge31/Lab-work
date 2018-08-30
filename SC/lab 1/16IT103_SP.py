import csv
import random

# Authored by: Aditi Rao
# Submitted on 24th August 2018

#### VERY IMPORTANT NOTE #####

# I am assuming that all training tuples in the csv
# files are such that the class label is the last attribute 
# or last column of the csv file. 
# In this example SPECT.csv requires the first column
# to be moved to the last position before running this code
class Perceptron:
    def __init__(self,file=None,iterations=1000,learning_rate=0.2):
        self.train=[]
        self.test=[]
        self.labels=[]
        self.weights=[]
        self.iterations=iterations
        self.MAX_ITERATIONS=1000
        self.LEARNING_RATE=learning_rate
        self.file=file

    def read_datafile(self):
        print("\nReading data from file: ", self.file)
        with open(self.file,"r") as file_name :
            data=csv.reader(file_name)
            for line in data:
                self.train.append(list(line))
            attributes=self.train.pop(0)
            random.shuffle(self.train)
            for i in range(0,int(len(self.train)*0.1)):
                self.test.append(self.train.pop())
        print("Data reading complete\n")

        print("Test set: ",len(self.test)," values. Train set: ",len(self.train)," values")
        n_items=len(self.train[0])
        self.weights=[1/(n_items) for i in range(0,n_items)]
        for item in self.train:
            self.labels.append(item[-1])

        self.labels=list(set(self.labels))
        print("Classes: ",self.labels,"\n")

    def train_perceptron(self):
        trained=True
        self.read_datafile()
        print("Training on ",len(self.train), "examples.....")
        n_items=len(self.train[0])
        for i in range (0,min(self.MAX_ITERATIONS,self.iterations)):
            for line in self.train:
                predicted=(self.weights[0]*1)

                for i in range(0,n_items-1):
                    predicted+=self.weights[i+1]*float(line[i])
                if predicted>1:
                    error=self.labels.index(line[-1])-1
                else:
                    error=self.labels.index(line[-1])
                if error!=0 and trained:
                    trained=False
                if error==0 and not trained:
                    trained=True            
                for i in range(1,n_items):
                    self.weights[i]+=self.LEARNING_RATE*error*float(line[i-1])
            if trained:
                print("Trained in ", i," iterations")
                print(self.weights)
                break    


        print("Training complete.\n")

    def test_perceptron(self):
        print("Testing ",len(self.test), " examples....")
        count=0
        n_items=len(self.train[0])
        for line in self.test:
            expected=self.weights[0]
            for i in range(0,n_items-1):
                expected+=self.weights[i+1]*float(line[i])
            if expected>1:
                predicted=self.labels[1]
            else:
                predicted=self.labels[0]
            #print(line[-1],predicted)
            if predicted==line[-1]:
                count+=1
        print("Testing Complete\nAccuracy: ",(count/len(self.test))*100,"%\n\n")


def main():
    iris_perceptron=Perceptron('IRIS.csv')
    iris_perceptron.train_perceptron()
    iris_perceptron.test_perceptron()

    # spect_perceptron=Perceptron('SPECT.csv')
    # spect_perceptron.train_perceptron()
    # spect_perceptron.test_perceptron()

if __name__ == '__main__':
    main()
