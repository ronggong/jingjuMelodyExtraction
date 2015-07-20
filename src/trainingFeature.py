# -*- coding: utf-8 -*-

import contourReader as cr
import featuresCalc as fc
import directoryGetter as dg
import matplotlib.pyplot as plt
import json

voicePath = '/home/rgong/MTG/jingjuMelody/voicePitchContours'
nonvoicePath = '/home/rgong/MTG/jingjuMelody/nonvoicePitchContours'

filenamesvoicePath = dg.jsonFilenameGetter(voicePath)
filenamesnonvoicePath = dg.jsonFilenameGetter(nonvoicePath)

allfilenames = filenamesvoicePath + filenamesnonvoicePath

# it contains each feature as a list [lengthContours, meanPitchContour ... mfcc1, mfcc2 ...]
featureList = []
for ii in range(19):
    featureList.append([])

featureVec = []
target = []
featureMeanSd = []

def featureListCreate(featureList, lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs, voicing):
    '''
    reshape features into featureList variable
    '''
    for ii in range(len(lengthContour)):
        featureList[0].append(lengthContour[ii])
        featureList[1].append(meanPitchContour[ii])
        featureList[2].append(sdPitchContour[ii])
        featureList[3].append(totalSalience[ii])
        featureList[4].append(meanSalience[ii])
        featureList[5].append(sdSalience[ii])
        for kk in range(len(mfccs[ii])):
            featureList[6+kk].append(mfccs[ii][kk])
        featureList[18].append(voicing)
    return featureList

def featureNormalization(featureList):
    '''
    the structure of normalized feature list is [(feature0, mean0, sd0), (feature1, mean1, sd1), ...]
    '''
    normalizedFeatureList = []
    for ii in range(len(featureList)-1):
        normalizedFeature, mean, sd = fc.scaleFeatures(featureList[ii])
        normalizedFeatureList.append((normalizedFeature, mean, sd))
    normalizedFeatureList.append(featureList[-1])
    return normalizedFeatureList

jj = 1
for filename in filenamesvoicePath:
    print jj, len(allfilenames)
    contours_bins, contours_contourSaliences, contours_start_times, duration = cr.contourReader(filename)
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndexCF = cr.contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize = 2048, hopsize = 128)
    #contours_bins, contours_contourSaliences, contours_start_times, toRmIndexRF = registerFilter(contours_bins, contours_contourSaliences, contours_start_times, tonicHz = 350.0) # need to give tonic firstly

    lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs = fc.featureExtract(contours_bins, contours_contourSaliences)

    featureList = featureListCreate(featureList, lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs, 0)
    jj += 1

for filename in filenamesnonvoicePath:
    print jj, len(allfilenames)
    contours_bins, contours_contourSaliences, contours_start_times, duration = cr.contourReader(filename)
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndexCF = cr.contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize = 2048, hopsize = 128)
    #contours_bins, contours_contourSaliences, contours_start_times, toRmIndexRF = registerFilter(contours_bins, contours_contourSaliences, contours_start_times, tonicHz = 350.0) # need to give tonic firstly

    lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs = fc.featureExtract(contours_bins, contours_contourSaliences)

    featureList = featureListCreate(featureList, lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs, 1)
    jj += 1

normalizedFeatureList = featureNormalization(featureList)

# reshape the feature vector and target
for ii in range(len(normalizedFeatureList[-1])):
    vec = []
    for jj in range(len(normalizedFeatureList)-1):
        vec.append(float(normalizedFeatureList[jj][0][ii]))

    featureVec.append(vec)
    target.append(normalizedFeatureList[-1][ii])

# write the mean and sd for each feature
for ii in range(len(normalizedFeatureList)-1):
    featureMeanSd.append((normalizedFeatureList[ii][1], normalizedFeatureList[ii][2]))

with open('featureJson.json', 'w') as outfile:
        data = {'featureVec': featureVec, 'target': target, 'meansd': featureMeanSd}
        json.dump(data, outfile)

'''
plt.figure(0)
plt.hist(lengthContour)
plt.title("length contour")

plt.figure(1)
plt.hist(meanPitchContour)
plt.title("mean pitch contour")

plt.figure(2)
plt.hist(sdPitchContour)
plt.title("sd pitch")

plt.figure(3)
plt.hist(totalSalience)
plt.title("total salience")

plt.figure(4)
plt.hist(meanSalience)
plt.title("mean salience")

plt.figure(5)
plt.hist(sdSalience)
plt.title("sd salience")

print vibratoFreq
plt.figure(6)
plt.hist(vibratoFreq)
plt.show()
'''
