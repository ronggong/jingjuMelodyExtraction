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

featureVec = []
target = []

jj = 1
for filename in filenamesvoicePath:
    print jj, len(allfilenames)
    contours_bins, contours_contourSaliences, contours_start_times, duration = cr.contourReader(filename)
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndexCF = cr.contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize = 2048, hopsize = 128)
    #contours_bins, contours_contourSaliences, contours_start_times, toRmIndexRF = registerFilter(contours_bins, contours_contourSaliences, contours_start_times, tonicHz = 350.0) # need to give tonic firstly

    lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs = fc.featureExtract(contours_bins, contours_contourSaliences)

    for ii in range(len(lengthContour)):
        f1 = [lengthContour[ii], meanPitchContour[ii], sdPitchContour[ii], totalSalience[ii], meanSalience[ii], sdSalience[ii]]
        f2 = mfccs[ii].tolist()
        feature = f1 + f2
        featureVec.append(feature)
        target.append(0)
    jj += 1

for filename in filenamesnonvoicePath:
    print jj, len(allfilenames)
    contours_bins, contours_contourSaliences, contours_start_times, duration = cr.contourReader(filename)
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndexCF = cr.contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize = 2048, hopsize = 128)
    #contours_bins, contours_contourSaliences, contours_start_times, toRmIndexRF = registerFilter(contours_bins, contours_contourSaliences, contours_start_times, tonicHz = 350.0) # need to give tonic firstly

    lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs = fc.featureExtract(contours_bins, contours_contourSaliences)

    for ii in range(len(lengthContour)):
        f1 = [lengthContour[ii], meanPitchContour[ii], sdPitchContour[ii], totalSalience[ii], meanSalience[ii], sdSalience[ii]]
        f2 = mfccs[ii].tolist()
        feature = f1 + f2
        featureVec.append(feature)
        target.append(1)
    jj += 1

with open('featureJson.json', 'w') as outfile:
        data = {'featureVec': featureVec, 'target': target}
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
