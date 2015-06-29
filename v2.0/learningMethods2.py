from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn import metrics
from sklearn.cross_validation import cross_val_score, KFold, train_test_split, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
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
	#X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.7, random_state = 0)
	#clf = GaussianNB()
	#clf = SVC(kernel = 'linear')
	#regC = 1.0  # SVM regularization parameter
	#clf = SVC(kernel='rbf', gamma=0.01, C=regC)
	#clf = LinearSVC(loss = 'l2')
	#clf = OneVsRestClassifier(LinearSVC(random_state = 0))
	#clf.fit(X_train, Y_train)



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
        l_val = sorted(d.values())
        l_key = []
        for v in l_val :
                l_key.append(d.keys()[d.values().index(v)])
	print 'SMO : '
	print(metrics.classification_report(Y, stratified_cv(X,Y,SVC,kernel = 'linear'), target_names = l_key))	
	print 'LibLinear : '
	print(metrics.classification_report(Y, stratified_cv(X,Y,LinearSVC,loss ='l2'), target_names = l_key))
	print 'Naive Bayes : '
	print(metrics.classification_report(Y, stratified_cv(X,Y,GaussianNB), target_names = l_key))
'''
	#expected = OneVsRestClassifier(LinearSVC(random_state = 0)).fit(X,Y).predict(X)

	#print(metrics.classification_report(expected,Y))
	#print(metrics.confusion_matrix(expected,Y))
	clf = LinearSVC(random_state = 0)
	k_fold = KFold(len(Y), 10, shuffle = True)
	#cross_val_score(clf, X, Y, cv = cv, score_func = metrics.f1_score)

	precisions =  cross_val_score(clf, X, Y, cv=k_fold, n_jobs = 1, scoring = 'precision')
	print( 'Precision : ', precisions)
	recalls = cross_val_score(clf, X, Y, cv=k_fold, n_jobs = 1, scoring = 'recall')
	print('Recall : ', recalls)
	f_measures = cross_val_score(clf, X, Y, cv=k_fold, n_jobs = 1, scoring = 'f1')  
	print('F_measure : ', f_measures)
	#aucs = cross_val_score(clf, X, Y, cv=k_fold, n_jobs = 1, scoring = 'roc_auc')
	#print('Auc : ', aucs)
	acc = cross_val_score(clf, X, Y, cv=k_fold, n_jobs = 1, scoring = 'accuracy') 
   	print('Acc : ',acc)
'''	

	
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
	
