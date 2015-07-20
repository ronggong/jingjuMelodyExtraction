from sklearn import neighbors
import json
import directoryGetter as dg
from sklearn.externals import joblib

print 'loading training data ...'
filename = 'featureJson.json'

with open(filename) as data_file:    
    data = json.load(data_file)

    X = data['featureVec']
    y = data['target']

knn = neighbors.KNeighborsClassifier(n_neighbors=5)

# training
print 'training kNN model ... ...'
knn.fit(X, y)

joblib.dump(knn, 'jingju_pitchContoursClassificationModel.pkl') 

