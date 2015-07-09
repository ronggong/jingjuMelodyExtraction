import sys
sys.path.append("./src")
sys.path.append("./model")

import pitchContours as pc
import featuresCalc as fc
import contourReader as cr
from sklearn.externals import joblib
import numpy as np

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

    featureVec = []
    for ii in range(len(lengthContour)):
        f1 = [lengthContour[ii], meanPitchContour[ii], sdPitchContour[ii], totalSalience[ii], meanSalience[ii], sdSalience[ii]]
        f2 = mfccs[ii].tolist()
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
