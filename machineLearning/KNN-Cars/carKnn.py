import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd 
import numpy as np
from sklearn import linear_model , preprocessing
import pickle

data = pd.read_csv("./KNN-cars/car.data")

le = preprocessing.LabelEncoder()

buying = le.fit_transform(list(data["buying"]))
maint = le.fit_transform(list(data["maint"]))
door = le.fit_transform(list(data["door"]))
persons = le.fit_transform(list(data["persons"]))
safety = le.fit_transform(list(data["safety"]))
lug_boot = le.fit_transform(list(data["lug_boot"]))
cls = le.fit_transform(list(data["class"]))

def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
            list1 = unique_list

mylist = list(zip(cls,data["class"]))
print(unique(mylist))

predict = "safety"

x = list(zip(buying,maint,door,persons,lug_boot,safety))
y = list(predict)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)



# best = 0
# bestx = 0
# for x in range(1,20):
#     model = KNeighborsClassifier(n_neighbors=x)
#     model.fit(x_train,y_train)
#     acc = model.score(x_test,y_test)
#     print(acc,"iteration:",x)
#     if acc > best:
#         best = acc
#         bestx = x
#         with open("bestmodel.pickle", 'wb') as f:
#             pickle.dump(model,f)
# print("Best: ",best, "iteration: ", bestx)

with open ("bestmodel.pickle" ,'rb') as f:
    model = pickle.load(f)

predicted = model.predict(x_test)
names = ["unacc", "acc", "good", "vgood"]

# for x in range(len(x_test)):
#     if predicted[x] != y_test[x]:
#         print("Predicted:", names[predicted[x]], "Data:",x_test[x], "Actual", names[y_test[x]])
