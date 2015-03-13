
import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.core.converters import Loader

jvm.start()

loader = Loader(classname="weka.core.converters.CSVLoader")
data = loader.load_file("peptides_final.csv")
data.class_is_first()

from weka.filters import Filter
from weka.classifiers import FilteredClassifier
from weka.classifiers import Evaluation
from weka.core.classes import Random

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
