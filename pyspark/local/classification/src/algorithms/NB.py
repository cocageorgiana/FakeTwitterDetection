from sklearn.metrics import accuracy_score, confusion_matrix
from pyspark.ml.classification import NaiveBayes
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml import Pipeline
from pyspark.sql.functions import *

from src import config as cfg

cfg.dir

features = ["Retweets", "Favorites", "New_Feature"]  # Class is label


class NbClassifier:

    def __init__(self, file_name, spark_context, smoothing=1.0, modelType="multinomial"):
        self.sqlContext = SQLContext(spark_context)

        self.spark_context = spark_context

        self.data = self.sqlContext.read.options(header='true', inferschema='true', delimiter=',').csv(file_name)

        self.data.cache()

        self.settings = [('smoothing', smoothing), ('modelType', modelType)]

        self.lr_data = self.data.select(col("Class").alias("label"), *features)

        vectorAssembler = VectorAssembler(inputCols=features, outputCol="unscaled_features")

        standardScaler = StandardScaler(inputCol="unscaled_features", outputCol="features")

        self.nb = NaiveBayes(smoothing=smoothing, modelType=modelType)

        stages = [vectorAssembler, standardScaler, self.nb]

        pipeline = Pipeline(stages=stages)

        self.model = pipeline.fit(self.lr_data)

    def classify_testdata(self, filename):
        """
          Function that classifies the testing dataset
          :param filename: The filename that contains the testing dataset
          :return: The predicted labels for the testing dataset
        """
        self.test_file = self.sqlContext.read.format('csv').options(header='true', inferschema='true').load(filename)

        lr_data = self.test_file.select(col("Class").alias("label"), *features)

        prediction = self.model.transform(lr_data)

        return prediction

    def classify(self, x):
        """
        Function that classifies an entry
        :param x: Entry to be predicted
        :return: The predicted label
        """

        x["Retweets"] = int(x["Retweets"])
        x["Favorites"] = float(x["Favorites"])

        data_frame = self.sqlContext.createDataFrame([x])
        output = self.model.transform(data_frame)
        return output.select(col("prediction")).collect()[0].prediction

    def confusion_matrix(self, predict):
        """
        Function that computes confusion matrix to evaluate the accuracy of the classification
        :param predict: The predicted labels that is used to compute the confusion matrix
        :return: The confusion matrix
        """
        predict_list = [i.prediction for i in predict.select("prediction").collect()]
        test_class = [i.Class for i in self.test_file.select("Class").collect()]  # self.test_file['Class']
        accuracy = accuracy_score(test_class, predict_list)
        accuracy = accuracy * 100
        print("############################NB############################")
        print("Accuracy for NB " + str(accuracy) + ' with settings ' + str(self.settings))
        print("Confusion Matrix for NB")
        print(confusion_matrix(test_class, predict_list))
        print("##########################################################")
        return accuracy

    # def plot(self, predict):
    #
    #     columns_header = ['Retweets', 'Favorites', 'New_Feature', 'Class']
    #
    #     testing_file_location = 'Test_feature_extracted.csv'
    #     training_file_location = 'Training_feature_extracted.csv'
    #
    #     train_file = pd.read_csv(training_file_location, sep=",", usecols=columns_header, index_col=None)
    #     test_file = pd.read_csv(testing_file_location, sep=',', usecols=columns_header, index_col=None)
    #
    #
    #     train = [i.label for i in self.lr_data.select("label").collect()]
    #     test_class = [i.prediction for i in predict.select("prediction").collect()]
    #
    #     color = ['red' if label == 1 else 'green' for label in train]
    #     color_test = ['black' if label == 1 else 'blue' for label in test_class]
    #
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')
    #     ax.scatter(train_file['Retweets'], train_file['Favorites'], train_file['New_Feature'],
    #                zdir='z', s=20, depthshade=True, color=color, marker='^')
    #     ax.scatter(test_file['Retweets'], test_file['Favorites'], test_file['New_Feature'],
    #                zdir='z', s=20, depthshade=True, color=color_test, marker='^')
    #     plt.title("NB Classifier")
    #     ax.set_xlabel('Retweets axis')
    #     ax.set_ylabel('Favorites axis')
    #     ax.set_zlabel('Feature axis')
    #     ax.legend(loc=2)
    #     plt.show()


if __name__ == "__main__":
    print("You are in main")
