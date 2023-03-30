import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle
import matplotlib.pyplot as pyplot
from matplotlib import style

data = pd.read_csv(".\StudentGrades\student-mat.csv", sep = ";")
data = data [["G1", "G2", "G3", "studytime", "failures", "absences"]]

predict = "G3"

x = np.array(data.drop([predict],1))
y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)


best = 0
for _ in range (20):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

    linear = linear_model.LinearRegression()

    linear.fit(x_train,y_train)
    acc = linear.score(x_test,y_test)
    print("Accuracy:", acc)

    if acc > best:
        best = acc
        with open("studentmodel.pickle", 'wb') as f:
            pickle.dump(linear,f)
print(f"Best Accuraccy: {best}")


pickle_in = open(".\StudentGrades\studentmodel.pickle", 'rb')
linear = pickle.load(pickle_in)


print("Coefficient: \n",linear.coef_)
print("Intercept: \n",linear.intercept_)

currentAcc = linear.score(x_test,y_test)
print("Current Accuracy:", currentAcc)

sampledata = [85,1648080001,100]

predictions = linear.predict(x_test)
for x in range(len(predictions)):
    print(predictions[x],x_test[x],y_test[x])


p = "G2"
style.use("ggplot")
pyplot.scatter(data[p],data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()