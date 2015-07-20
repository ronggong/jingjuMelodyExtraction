# -*- coding: utf-8 -*-

import numpy as np
import essentia.standard as ess
import matplotlib.pyplot as plt

def length(contour):
    return len(contour)

def meanPitch(contour):
    return np.mean(contour)

def sdPitch(contour):
    return np.std(contour)

def vibrato(contour, sr, hopsize):
    # subtract the mean
    contour = np.array(contour) - meanPitch(contour)
    contour = contour.tolist()
    
    
    # even the contour length
    if len(contour) % 2 == 1:
        contour = contour + [0]

    normalizedLength = len(contour)
    '''
    # fft size default is 1024
    halfLength = len(contour)/2+1
    
    freqStep = (sr/float(hopsize)/2.0) / halfLength

    # freq vector
    freq = (np.array(range(halfLength)) + 0.5) * freqStep
    '''
    '''
    # normalize the length of pitch length to 8192
    normalizedLength = 8192
    if len(contour) < normalizedLength:
         contour = contour + [0] * (normalizedLength-len(contour))
    '''

    # fft spectrum
    fftEssentia = ess.FFT()
    out = fftEssentia(contour)
    mag = abs(out)
    #mag = mag.tolist()

    # calculate the mfcc
    hfb = sr/float(hopsize)/2.0
    dsr = sr/float(hopsize)
    MFCC = ess.MFCC(highFrequencyBound = hfb, sampleRate = dsr, inputSize = normalizedLength/2+1)
    bands, mfcc = MFCC(mag)
    
    '''
    plt.figure()
    plt.subplot(211)
    plt.plot(mfcc[1:])
    plt.title(len(contour))
    plt.subplot(212)
    plt.plot(contour)
    plt.show()
    '''

    #freqMaxAmp = freq[mag.index(max(mag))]
    return mfcc # we only need 12 coefficient

def featureExtract(contours_bins, contours_contourSaliences):
    lengthContour = []
    meanPitchContour = []
    sdPitchContour = []
    mfccs = []
    
    for contour in contours_bins:
        lengthContour.append(length(contour))
        meanPitchContour.append(meanPitch(contour))
        sdPitchContour.append(sdPitch(contour))

        mfcc = vibrato(contour, 44100, 128)
        mfccs.append(mfcc[1:])
       

    totalSalience = []
    meanSalience = []
    sdSalience = []

    for contour in contours_contourSaliences:
        totalSalience.append(sum(contour))
        meanSalience.append(meanPitch(contour))
        sdSalience.append(sdPitch(contour))
    
    return  lengthContour, meanPitchContour, sdPitchContour, totalSalience, meanSalience, sdSalience, mfccs

def stdDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5

def scaleFeatures(vals):
    vals = np.array(vals)
    mean = sum(vals)/float(len(vals))
    sd = stdDev(vals)
    vals = vals - mean
    return vals/sd, mean, sd
    
