import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.core.converters import Loader
import time

from weka.filters import Filter
from weka.classifiers import FilteredClassifier
from weka.classifiers import Evaluation
from weka.core.classes import Random

from weka.classifiers import PredictionOutput, KernelClassifier, Kernel

from liblinear import *
from liblinearutil import *

def runBayes(file,bound) :
	loader = Loader(classname="weka.core.converters.CSVLoader")
	data = loader.load_file(file)
	data.class_is_first()

	remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", bound])
	cls = Classifier(classname="weka.classifiers.bayes.NaiveBayes")

	fc = FilteredClassifier()
	fc.filter = remove
	fc.classifier = cls

	evl = Evaluation(data)
	evl.crossvalidate_model(cls, data, 10, Random(1))

	print(evl.percent_correct)
	print(evl.summary())
	result = evl.class_details()
	print(result)
	return result
	
def runSMO(file,bound) :

	loader = Loader(classname="weka.core.converters.CSVLoader")
	data = loader.load_file(file)
	data.class_is_first()

	remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", bound])
	
	cls = KernelClassifier(classname="weka.classifiers.functions.SMO", options=["-C", "1.0","-L","0.001","-P","1.0E-12","-N","0"])
	kernel = Kernel(classname="weka.classifiers.functions.supportVector.PolyKernel", options=["-C", "250007","-E","1.0"])
	cls.kernel = kernel
	pout = PredictionOutput(classname="weka.classifiers.evaluation.output.prediction.PlainText")

	evl = Evaluation(data)
	evl.crossvalidate_model(cls, data, 10, Random(1),pout)

	print(pout.buffer_content())

	#print(evl.percent_correct)
	#print(evl.summary())
	print(evl.class_details())
	return evl.class_details()

def runLibLinear(file) :

	y,x  = svm_read_problem(file)
	prob = problem(y,x)
	param = parameter('-c 4 -B 1')

	m = train(prob, param)
	save_model('model_', m)
	m = load_model('model_')
	p_label, p_acc, p_val = predict(y, x, m)
	ACC, MSE, SCC = evaluations(y, p_label)

def changeFile(file,bound) :
	pass

def learning(fileG, bound = "%d-%d" % (1,3)) : #fileG = 'file/peptides_monomers.csv'  bound = "%d-%d" % (1,3)

	result = ""
	try :
		jvm.start()
		print('BAYES')
		resB = runBayes(fileG, bound)

		print('SMO')
		resS = runSMO(fileG, bound)	

		print('LIBLINEAR')
		resL = runLibLinear('test.train') #TODO

		result = "BAYES \n %s \n SMO \n %s \n LibLinear \n %s" % (resB, resS, resL)

	except Exception, e:
		print (traceback.format_exc())
	finally :
		jvm.stop()
		return result
