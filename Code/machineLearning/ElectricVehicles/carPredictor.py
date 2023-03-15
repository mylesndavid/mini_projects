import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle
import matplotlib.pyplot as pyplot
from matplotlib import style


data = pd.read_csv(".\ElectricVehicles\Electric_Vehicle_Population_Data.csv", sep=",")
data = data[["Model Year","Electric Range"]]

predict = "Model Year"

# def replaceNan(array):
#     return np.nan_to_num(array)

x = np.array(data.drop([predict],1)) #what is the one doing?
# x = replaceNan(x)
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

print(x_train)

best = 0
for _ in range(20):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)
    model = linear_model.LinearRegression()
    model.fit(x_train,y_train)
    acc = model.score(x_test,y_test)
    print(acc)
    if acc > best:
        best = acc
        with open(".\ElectricVehicles\carPredictorModel.pickle", "wb")as f:
            pickle.dump(model,f)
print("Best:",best)

print("Coefficient: \n",model.coef_)
print("Intercept: \n",model.intercept_)

predictions = model.predict(x_test[:18])
for x in range(len(predictions)):
    print(predictions[x],x_test[x],y_test[x])