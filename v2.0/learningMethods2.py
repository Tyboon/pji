from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn import metrics
from sklearn.cross_validation import cross_val_score, KFold, train_test_split, StratifiedKFold
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.metrics import classification_report

import csv_io
import numpy as np


def launch_linearSVC(file, bound) : 

	X, Y, d = load(file, bound)
	print('Y : ')
	print Y
	print d

	print('X : ')
	print X
	reportBis(X, Y, d)


def load(file, bound) :
	'''
	Voir le chargement selon les bornes ou non 
	'''
	X = csv_io.read_csv(file, label = 0)
	Y = np.array([x[0] for x in X])
	Y, d = numerize(Y)
	X = np.array([x[1:] for x in X])
	return X, Y, d

def stratified_cv(X, y, clf_class, shuffle=True, n_folds=10, **kwargs):
    stratified_k_fold = StratifiedKFold(y, n_folds=n_folds) #shuffle = shuffle ?
    y_pred = y.copy()
    for ii, jj in stratified_k_fold:
        X_train, X_test = X[ii], X[jj]
        y_train = y[ii]
        clf = clf_class(**kwargs)
        clf.fit(X_train,y_train)
        y_pred[jj] = clf.predict(X_test)
    return y_pred

def report(clf, X_test, Y_test, d) :
	Y_pred = clf.predict(X_test)
	
	l_val = sorted(d.values())
	l_key = []
	for v in l_val : 
		l_key.append(d.keys()[d.values().index(v)])	

	print l_key 
	print l_val
	print classification_report(Y_test, Y_pred, target_names = l_key)

def reportBis(X, Y, d) :
	'''
		Give scores for SMO, Liblinear and Bayes on data X with target Y
	'''
	# Prepare class name
        l_val = sorted(d.values())
        l_key = []
        for v in l_val :
                l_key.append(d.keys()[d.values().index(v)])

	##### SMO #####
	print 'SMO : '
	print(metrics.classification_report(Y, stratified_cv(X,Y,SVC,kernel = 'linear'), target_names = l_key))	
	scores = cross_val_score(SVC(kernel='linear'), X, Y, cv = 10 )
	print("Accuracy : %0.3f " % (scores.mean()))
	#metrics.roc_auc_score(Y, Y, average=None)

	##### LIBLIN #####
	print 'LibLinear : '
	print(metrics.classification_report(Y, stratified_cv(X,Y,LinearSVC,loss ='l2'), target_names = l_key))
	#print(cross_val_score(LinearSVC(loss='l2'), X, Y, scoring='roc_auc', cv = StratifiedKFold(Y, n_folds=10)))
	scores = cross_val_score(LinearSVC(loss = 'l2'), X, Y, cv = 10 )
	print("Accuracy : %0.3f " % (scores.mean()))

	##### BAYES #####
	
	print 'Naive Bayes MultinomialNB : '

	print(metrics.classification_report(Y, stratified_cv(X,Y,MultinomialNB), target_names = l_key))
	scores = cross_val_score(MultinomialNB(), X, Y, cv = 10 )
        print("Accuracy : %0.3f " % (scores.mean()))

	
def numerize(Y) :
	'''
		Transform nominal target form to numeric form.
		Return : the new 
	'''
	cpt = 0
	Y_dic = dict()
	Y_num = []
	for e in Y :
		if e not in Y_dic :
			Y_dic[e] = cpt
			cpt += 1
		Y_num.append(Y_dic[e])
	Y_num = np.array(Y_num)
	return Y_num, Y_dic

if __name__ == "__main__" :

	launch_linearSVC()
	
