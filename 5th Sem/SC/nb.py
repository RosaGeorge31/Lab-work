import numpy as np
import pandas as pd


def accuracy(actual, predicted):
    return (actual == predicted).mean() * 100

def metrics(y_pred, y_true):
    tp, tn, fp, fn = 0, 0, 0, 0
    for true, pred in zip(y_true, y_pred):
        if true == 0:
            if pred == 0:
                tn += 1
            else:
                fp += 1
        else:
            if pred == 1:
                tp += 1
            else:
                fn += 1
    precision, recall = None, None
    try:
        precision=tp/(tp+fp)
        recall=tp/(tp+fn)
    except:
        print("Divide by zero")    
    return precision,recall

def fit_data(data):
    probabilities = {}
    probcl = {}
    for x in classes:
        datacl = data[data[target]==x][features]
        clsp = {}
        tot = len(datacl)
        for col in datacl.columns:
            colp = {}
            for val,cnt in datacl[col].value_counts().iteritems():
                pr = cnt/tot
                colp[val] = pr
            clsp[col] = colp
        probabilities[x] = clsp
        probcl[x] = len(datacl) / len(data)
    return probabilities, probcl


def split_data(dataset, n_folds):
    dataset = dataset.sample(frac=1).reset_index(drop=True)
    dataset_split = list()
    fold_size = int(len(dataset) / n_folds)
    for i in range(n_folds):
        dataset_split.append(dataset.iloc[i * fold_size: (i + 1) * fold_size])
    return dataset_split


def calculate_probability(x, probcl, probabilities):
    probab = {}
    for cl in classes:
        pr = probcl[cl]
        for col,val in x.iteritems():
            try:
                pr *= probabilities[cl][col][val]
            except KeyError:
                pr = 0
        probab[cl] = pr
    return probab

def evaluate_algorithm(dataset, n_folds,lr=0.1):
    folds = split_data(dataset, n_folds)
    f_acc, f_rec, f_pre = 0., 0., 0.
    for index in range(len(folds)):
        train = pd.concat([folds[i] for i in range(len(folds)) if i is not index])
        test = folds[index]
        probabilities, probcl = fit_data(train)
        predicted = list()
        for i in test.index:
            predicted.append(classify(test.loc[i, features], probcl, probabilities))
        predicted = np.array(predicted)
        actual = np.array(test.loc[:, target])
        acc = accuracy(actual, predicted)
        f_acc += acc
    return f_acc / len(folds)

def classify(x, probcl, probabilities):
    probab = calculate_probability(x, probcl, probabilities)
    mx = 0
    mxcl = ''
    for cl,pr in probab.items():
        if pr > mx:
            mx = pr
            mxcl = cl
    return mxcl


np.random.seed(10)

df_spect = pd.read_csv('SPECT.csv')
df_spect['Class'] = df_spect['Class'].map(lambda x: 1 if x == 'Yes' else 0)
df_spect.head()

print('Loaded Data Successfully')

target = 'Class'
features = df_spect.columns[df_spect.columns != target]
classes = df_spect[target].unique()