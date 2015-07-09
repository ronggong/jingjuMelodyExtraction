# -*- coding: utf-8 -*-

import json
import numpy as np

def contourReader(filename):
    '''
    to read contour json file
    '''
    with open(filename) as data_file:    
        data = json.load(data_file)

        contours_bins = data['contours_bins']
        contours_contourSaliences = data['contours_contourSaliences']
        contours_start_times = data['contours_start_times']
        duration = data['duration']
        
    #print len(contours_bins), len(contours_contourSaliences), len(contours_start_times), duration
    return contours_bins, contours_contourSaliences, contours_start_times, duration

def contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize, hopsize):
    '''
    delete pitch contours which shorter than 0.25s
    '''
    # minimum len allowed
    minLen = int((44100 * 0.25 - framesize)/float(hopsize)) + 1
    #print minLen
    
    # find to remove contour index
    toRmIndex = []
    for ii in range(len(contours_bins)):
        if len(contours_bins[ii]) < minLen:
            toRmIndex.append(ii)

    for ii in toRmIndex[::-1]:
        contours_bins.pop(ii)
        contours_contourSaliences.pop(ii)
        contours_start_times.pop(ii)

    # print len(contours_bins), len(contours_contourSaliences), len(contours_start_times)
    return contours_bins, contours_contourSaliences, contours_start_times, toRmIndex

def hz2centsbin(pitchHz, binResolution):
    centsbin = 1200 * np.log2(pitchHz/55.0) / binResolution
    return centsbin

def centsbin2hz(centsbin, binResolution):
    hz = 55.0*(2.0**(binResolution*centsbin/1200.0))
    return hz

def registerFilter(contours_bins, contours_contourSaliences, contours_start_times, tonicHz = 350.0):
    '''
    delete pitch contour outside 2 octaves register
    '''
    binResolution = 7.5
    minCents = hz2centsbin(200.0, binResolution)
    maxCents = hz2centsbin(500.0, binResolution)

    minCents = minCents - 2400.0/binResolution
    maxCents = maxCents + 2400.0/binResolution
    
    print minCents, maxCents, centsbin2hz(minCents, binResolution), centsbin2hz(maxCents, binResolution)

    toRmIndex = []
    threshold = 5 # if threshold points exceed the minCents or maxCents, delete this contour
    for jj in range(len(contours_bins)):
        ii = 0
        for pitch in contours_bins[jj]:
            if pitch > maxCents or pitch < minCents:
                ii += 1
                if ii >= threshold: 
                    toRmIndex.append(jj)
                    break

    # print len(toRmIndex)
    if len(toRmIndex) > 0:
        for ii in toRmIndex[::-1]:
            contours_bins.pop(ii)
            contours_contourSaliences.pop(ii)
            contours_start_times.pop(ii)

    print len(contours_bins), len(contours_contourSaliences), len(contours_start_times)
    return contours_bins, contours_contourSaliences, contours_start_times, toRmIndex

if __name__ == '__main__':
    filename = '/home/rgong/MTG/jingjuMelody/voicePitchContours/1-08 伴奏：玉堂春跪在督察院.json'
    contours_bins, contours_contourSaliences, contours_start_times, duration = contourReader(filename)
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndex1 = contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize = 2048, hopsize = 128)
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndex2 = registerFilter(contours_bins, contours_contourSaliences, contours_start_times, tonicHz = 350.0)
