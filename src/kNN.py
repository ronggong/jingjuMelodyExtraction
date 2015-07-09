from sklearn import neighbors
import json
import directoryGetter as dg
from sklearn.externals import joblib

print 'loading training data ...'
filename = 'trainingFeatureJson.json'

with open(filename) as data_file:    
    data = json.load(data_file)

    X = data['featureVec']
    y = data['target']

knn = neighbors.KNeighborsClassifier(n_neighbors=5)

# training
print 'training kNN model ... ...'
knn.fit(X, y)

joblib.dump(knn, 'jingju_pitchContoursClassificationModel.pkl') 

# testing
print 'testing kNN model ... ...'
knn = joblib.load('jingju_pitchContoursClassificationModel.pkl') 

testingFeaturesFolder = './testingFeatures/'
testingFeaturesfilenames = dg.jsonFilenameGetter(testingFeaturesFolder)

for testingFilename in testingFeaturesfilenames:
    with open(testingFilename) as data_file:    
        data = json.load(data_file)

        X = data['featureVec']
        y = data['toRmIndex']

    classification = knn.predict(X) # 0: voice 1: nonvoice
    classification = classification.tolist()
    
    outputFilename = testingFilename[:-5] + '_classification.json'
    with open(outputFilename, 'w') as outfile:
        data = {'featureVec': X, 'toRmIndex': y, 'classification': classification}
        json.dump(data, outfile)
