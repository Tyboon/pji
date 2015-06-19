import csv as csv
import numpy as np
from sklearn.svm import LinearSVC

train=csv.reader(open('testtrain.csv','rb')) #open file
headerx=train.next()

x=[]
for row in train:
	x.append(row)
x=np.array(x)
category=csv.reader(open('testtarget.csv','rb')) #open file
headery=category.next()

y=[]
for row in category:
	y.append(row)
y=np.array(y)

clf=LinearSVC()
clf = clf.fit(x,y)

test=csv.reader(open('test.csv','rb'))
headert=test.next()
new=[]
for row in test:
	new.append(row)
new=np.array(new).astype(np.float)

resultset=clf.predict(new).astype(np.float)
np.savetxt('results.csv',resultset,delimiter=",")
