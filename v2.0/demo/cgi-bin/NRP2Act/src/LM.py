from sklearn import datasets
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn import metrics
from sklearn.cross_validation import cross_val_score, KFold, train_test_split, StratifiedKFold
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.metrics import classification_report
from sklearn.externals import joblib
import pickle
import numpy as np


def launch_report(file, bound) : 

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
	scores = cross_val_score(LinearSVC(loss = 'l2'), X, Y, cv = 10 )
	print("Accuracy : %0.3f " % (scores.mean()))

	##### BAYES #####
	
	print 'Naive Bayes MultinomialNB : '

	print(metrics.classification_report(Y, stratified_cv(X,Y,MultinomialNB), target_names = l_key))
	scores = cross_val_score(MultinomialNB(), X, Y, cv = 10 )
        print("Accuracy : %0.3f " % (scores.mean()))

	
def training(data) :
	Y = np.array([x[0] for x in data])
        Y = Y[1:] # delete header
        X = data[1:] # delete header
        Y, d = numerize(Y)
	X = np.array([x[4:] for x in X])
	
	clf_smo = SVC(kernel='linear')
	clf_lib = LinearSVC(loss = 'l2')
	#clf_bayes = MultinomialNB()	

	clf_smo.fit(X,Y)
	clf_lib.fit(X,Y)
	#clf_bayes(X,Y)
	clf_bayes = None
	# store classifiers
	joblib.dump(clf_smo, '../data/pickle/clf_smo.pkl')
	joblib.dump(clf_lib, '../data/pickle/clf_lib.pkl')
	# store dictionnary
	file = open('../data/pickle/dico.txt','wb')
	pickle.dump(d,file)
	file.close()

	return

def predicting(x) :
	file = open('../data/pickle/dico.txt','rb')
	dic = pickle.load(file)
	file.close()
	clf_smo = joblib.load('../data/pickle/clf_smo.pkl')
	clf_lib = joblib.load('../data/pickle/clf_lib.pkl')
	num_smo = clf_smo.predict(x)
	num_lib = clf_lib.predict(x)
	act = {}
	act['smo'] = find_key(dic, num_smo[0])
	act['lib'] = find_key(dic, num_lib[0])
	return act

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

def find_key(dic, val) :
	for key in dic.keys():
		if dic[key] == val :
			return key

if __name__ == "__main__" :

	launch_report(argv[1:])
	
