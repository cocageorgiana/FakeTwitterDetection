from pyspark import SparkContext
import src.config as cfg
import src.processing as prp
import src.algorithms.SVM as svm
import src.algorithms.NB as nb
import src.algorithms.RandomForest as rf
import time
import warnings

warnings.filterwarnings("ignore")

testing_file_location = 'Test_feature_extracted.csv'
training_file_location = 'Training_feature_extracted.csv'

if __name__ == "__main__":
    import os

    print(os.getcwd())
    spark_context = SparkContext("local", "Twitter");
    testing_file_location = 'Test_feature_extracted.csv'
    training_file_location = 'Training_feature_extracted.csv'

    start_time = time.time()

    ###############################################################################
    training_data = prp.PreProcessing('../data/training_dataset.csv', 'Training')
    training_data.process()

    test_data = prp.PreProcessing('../data/test_dataset.csv', 'Test')
    test_data.process()
    ###############################################################################
    
    ##############################SVM##############################################
    svm_time = time.time()

    maxIter = 200
    regParam = 0.0
    tol = 1e-6
    threshold = 0.0
    aggregationDepth = 2

    settings = [('maxIter', maxIter), ('regParam', regParam), ('tol', tol), ('threshold', threshold),
                ('aggregationDepth', aggregationDepth)]

    svm_classifier = svm.SVMClassifier(training_file_location, spark_context, maxIter, regParam, tol,
                                       threshold, aggregationDepth)
    svm_predict_test_data_class = svm_classifier.classify_testdata(testing_file_location)
    svm_classifier.confusion_matrix(svm_predict_test_data_class)
    print("SVM EXECUTION TIME " + str(time.time() - svm_time) + "for settings " + str(settings))
    ###############################################################################

    ##############################SVM##############################################
    svm_time = time.time()

    maxIter = 100
    regParam = 0.0
    tol = 1e-7
    threshold = 0.1
    aggregationDepth = 3

    settings = [('maxIter', maxIter), ('regParam', regParam), ('tol', tol), ('threshold', threshold),
                ('aggregationDepth', aggregationDepth)]

    svm_classifier = svm.SVMClassifier(training_file_location, spark_context, maxIter, regParam, tol,
                                       threshold, aggregationDepth)
    svm_predict_test_data_class = svm_classifier.classify_testdata(testing_file_location)
    svm_classifier.confusion_matrix(svm_predict_test_data_class)
    print("SVM EXECUTION TIME " + str(time.time() - svm_time) + "for settings " + str(settings))
    ###############################################################################

    ##############################SVM##############################################
    svm_time = time.time()

    maxIter = 50
    regParam = 0.1
    tol = 1e-7
    threshold = 0.1
    aggregationDepth = 5

    settings = [('maxIter', maxIter), ('regParam', regParam), ('tol', tol), ('threshold', threshold),
                ('aggregationDepth', aggregationDepth)]

    svm_classifier = svm.SVMClassifier(training_file_location, spark_context, maxIter, regParam, tol,
                                       threshold, aggregationDepth)
    svm_predict_test_data_class = svm_classifier.classify_testdata(testing_file_location)
    svm_classifier.confusion_matrix(svm_predict_test_data_class)
    print("SVM EXECUTION TIME " + str(time.time() - svm_time) + "for settings " + str(settings))
    ###############################################################################

    ##############################RF###############################################
    rf_time = time.time()

    maxDepth = 5
    maxBins = 32
    minInstancesPerNode = 1
    minInfoGain = 0.0
    maxMemoryInMB = 256
    impurity = "gini"
    numTrees = 50

    settings = [('maxDepth', maxDepth), ('maxBins', maxBins), ('minInstancesPerNode', minInstancesPerNode),
                ('minInfoGain', minInfoGain),
                ('maxMemoryInMB', maxMemoryInMB), ('impurity', impurity), ('numTrees', numTrees)]

    rf_classifier = rf.RFClassifier(training_file_location, spark_context, maxDepth, maxBins, minInstancesPerNode,
                                    minInfoGain, maxMemoryInMB, impurity, numTrees)
    rf_predict_test_data_class = rf_classifier.classify_testdata(testing_file_location)
    rf_classifier.confusion_matrix(rf_predict_test_data_class)

    print("RF EXECUTION TIME " + str(time.time() - rf_time) + "for settings " + str(settings))
    ##############################################################################

    ##############################RF###############################################
    rf_time = time.time()

    maxDepth = 10
    maxBins = 32
    minInstancesPerNode = 1
    minInfoGain = 0.0
    maxMemoryInMB = 256
    impurity = "gini"
    numTrees = 100

    settings = [('maxDepth', maxDepth), ('maxBins', maxBins), ('minInstancesPerNode', minInstancesPerNode),
                ('minInfoGain', minInfoGain),
                ('maxMemoryInMB', maxMemoryInMB), ('impurity', impurity), ('numTrees', numTrees)]

    rf_classifier = rf.RFClassifier(training_file_location, spark_context, maxDepth, maxBins, minInstancesPerNode,
                                    minInfoGain, maxMemoryInMB, impurity, numTrees)
    rf_predict_test_data_class = rf_classifier.classify_testdata(testing_file_location)
    rf_classifier.confusion_matrix(rf_predict_test_data_class)

    print("RF EXECUTION TIME " + str(time.time() - rf_time) + "for settings " + str(settings))
    ##############################################################################

    ##############################RF###############################################
    rf_time = time.time()

    maxDepth = 10
    maxBins = 32
    minInstancesPerNode = 1
    minInfoGain = 0.0
    maxMemoryInMB = 1024
    impurity = "gini"
    numTrees = 200

    settings = [('maxDepth', maxDepth), ('maxBins', maxBins), ('minInstancesPerNode', minInstancesPerNode),
                ('minInfoGain', minInfoGain),
                ('maxMemoryInMB', maxMemoryInMB), ('impurity', impurity), ('numTrees', numTrees)]

    rf_classifier = rf.RFClassifier(training_file_location, spark_context, maxDepth, maxBins, minInstancesPerNode,
                                    minInfoGain, maxMemoryInMB, impurity, numTrees)
    rf_predict_test_data_class = rf_classifier.classify_testdata(testing_file_location)
    rf_classifier.confusion_matrix(rf_predict_test_data_class)

    print("RF EXECUTION TIME " + str(time.time() - rf_time) + "for settings " + str(settings))
    ##############################################################################

    ##############################NB###############################################
    nb_time = time.time()

    smoothing = 1.0
    modelType = "multinomial"

    settings = [('smoothing', smoothing), ('modelType', modelType)]

    nb_classifier = nb.NbClassifier(training_file_location, spark_context, smoothing, modelType)
    nb_predict_test_data_class = nb_classifier.classify_testdata(testing_file_location)
    accuracy_nb = nb_classifier.confusion_matrix(nb_predict_test_data_class)
    print("NB EXECUTION TIME " + str(time.time() - nb_time) + "for settings " + str(settings))
    ##############################################################################

    ##############################NB###############################################
    nb_time = time.time()

    smoothing = 3.0
    modelType = "multinomial"

    settings = [('smoothing', smoothing), ('modelType', modelType)]

    nb_classifier = nb.NbClassifier(training_file_location, spark_context, smoothing, modelType)
    nb_predict_test_data_class = nb_classifier.classify_testdata(testing_file_location)
    accuracy_nb = nb_classifier.confusion_matrix(nb_predict_test_data_class)
    print("NB EXECUTION TIME " + str(time.time() - nb_time) + "for settings " + str(settings))
    ##############################################################################

    ##############################NB###############################################
    nb_time = time.time()

    smoothing = 4.0
    modelType = "multinomial"

    settings = [('smoothing', smoothing), ('modelType', modelType)]

    nb_classifier = nb.NbClassifier(training_file_location, spark_context, smoothing, modelType)
    nb_predict_test_data_class = nb_classifier.classify_testdata(testing_file_location)
    accuracy_nb = nb_classifier.confusion_matrix(nb_predict_test_data_class)
    print("NB EXECUTION TIME " + str(time.time() - nb_time) + "for settings " + str(settings))
    ##############################################################################

    print("Total Execution time is " + str(time.time() - start_time))
