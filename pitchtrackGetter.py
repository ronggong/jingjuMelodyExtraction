import sys
sys.path.append("./src")
sys.path.append("./model")

import pitchContours as pc
import featuresCalc as fc
import contourReader as cr
from sklearn.externals import joblib
import numpy as np
import json

def pitchtrackGetter(fname, outputPitchtrack):
    # pitchContours object
    print 'extracting pitch contours ... ...'
    pitchMakam = pc.PitchExtractMakam()
    pitchMakam.setup()
    
    contours_bins, contours_contourSaliences, contours_start_times, duration = pitchMakam.run(fname)

    contours_start_times = contours_start_times.tolist()

    # filter short pitch contours
    print 'filtering short pitch contours ... ...'
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndexCF = cr.contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize = 2048, hopsize = 128)

    # feature extraction
    print 'extracting features ... ...'
    lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs = fc.featureExtract(contours_bins, contours_contourSaliences)

    # load mean sd for feature normalization
    meansdpath = './model/meansdJson.json'
    with open(meansdpath) as data_file:
        data = json.load(data_file)
        meansd = data['meansd']

    # normalize the feature vector
    featureVec = []
    for ii in range(len(lengthContour)):
        f1 = [(lengthContour[ii]/meansd[0][0])/meansd[0][1], (meanPitchContour[ii]/meansd[1][0])/meansd[1][1], (sdPitchContour[ii]/meansd[2][0])/meansd[2][1], (totalSalience[ii]/meansd[3][0])/meansd[3][1], (meanSalience[ii]/meansd[4][0])/meansd[4][1], (sdSalience[ii]/meansd[5][0])/meansd[5][1]]
        for kk in range(len(mfccs[ii])):
            f2.append((mfccs[ii][kk]-meansd[6+kk][0])/meansd[6+kk][1])
        feature = f1 + f2
        featureVec.append(feature)

    # classifying pitch contours
    print 'classifying pitch contours ... ...'
    knn = joblib.load('./model/jingju_pitchContoursClassificationModel.pkl') 
    
    classification = knn.predict(featureVec) # 0: voice 1: nonvoice
    classification = classification.tolist()

    contours_bins_out = []
    contours_contourSaliences_out = []
    contours_start_times_out = []
    
    for ii in range(len(classification)):
        if classification[ii] == 0:
           contours_bins_out.append(contours_bins[ii])
           contours_contourSaliences_out.append(contours_contourSaliences[ii])
           contours_start_times_out.append(contours_start_times[ii])
    
    # dumping contours into pitch track
    out = pitchMakam.pitchtrackDumper(contours_bins_out, contours_contourSaliences_out, contours_start_times_out, duration)

    np.savetxt(outputPitchtrack, out)

    return
