import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.core.converters import Loader

from weka.filters import Filter
from weka.classifiers import FilteredClassifier
from weka.classifiers import Evaluation
from weka.core.classes import Random

from weka.classifiers import PredictionOutput, KernelClassifier, Kernel

from liblinear import *
from liblinearutil import *

def runBayes(file) :
	jvm.start()

	loader = Loader(classname="weka.core.converters.CSVLoader")
	data = loader.load_file(file)
	data.class_is_first()

	remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "1-3"])
	cls = Classifier(classname="weka.classifiers.bayes.NaiveBayes")

	fc = FilteredClassifier()
	fc.filter = remove
	fc.classifier = cls

	evl = Evaluation(data)
	evl.crossvalidate_model(cls, data, 10, Random(1))

	print(evl.percent_correct)
	print(evl.summary())
	print(evl.class_details())

	jvm.stop()

	
def runSMO(file) :
	jvm.start()

	loader = Loader(classname="weka.core.converters.CSVLoader")
	data = loader.load_file(file)
	data.class_is_first()

	remove = Filter(classname="weka.filters.unsupervised.attribute.Remove", options=["-R", "1-3"])
	
	cls = KernelClassifier(classname="weka.classifiers.functions.SMO", options=["-C", "1.0","-L","0.001","-P","1.0E-12","-N","0"])
	kernel = Kernel(classname="weka.classifiers.functions.supportVector.PolyKernel", options=["-C", "250007","-E","1.0"])
	cls.kernel = kernel
	pout = PredictionOutput(classname="weka.classifiers.evaluation.output.prediction.PlainText")

	evl = Evaluation(data)
	evl.crossvalidate_model(cls, data, 10, Random(1),pout)

	print(pout.buffer_content())

	print(evl.percent_correct)
	print(evl.summary())
	print(evl.class_details())


	jvm.stop()

def runLibLinear(file) :

	y,x  = svm_read_problem(file)
	prob = problem(y,x)
	param = parameter('-c 4 -B 1')

	m = train(prob, param)
	save_model('model_', m)
	m = load_model('model_')
	p_label, p_acc, p_val = predict(y, x, m)
	ACC, MSE, SCC = evaluations(y, p_label)

	jvm.stop()

if  __name__ == "__main__" :
	print('run Bayes')
	#runBayes('file/peptides_monomers.csv')

	print('run SMO')
	#runSMO('file/peptides_monomers.csv')	

	print('run liblinear')
	runLibLinear('test.train')
	
