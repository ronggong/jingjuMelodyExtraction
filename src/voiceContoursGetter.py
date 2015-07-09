import directoryGetter as dg
import contourReader as cr
import json

def classificationResultReader(classificationResult):
    with open(classificationResult) as data_file:    
        data = json.load(data_file)

        toRmIndex = data['toRmIndex']
        classification = data['classification']
        
    return toRmIndex, classification
    
def voiceContoursGetter(pitchContourJson, classificationResult):
    contours_bins, contours_contourSaliences, contours_start_times, duration = cr.contourReader(pitchContourJson)
    contours_bins, contours_contourSaliences, contours_start_times, toRmIndex_cal = cr.contourFilter(contours_bins, contours_contourSaliences, contours_start_times, framesize = 2048, hopsize = 128)

    toRmIndex_json, classification = classificationResultReader(classificationResult)
            
    if len(toRmIndex_cal) == len(toRmIndex_json):
        contours_bins_out = []
        contours_contourSaliences_out = []
        contours_start_times_out = []
    
        for ii in range(len(classification)):
            if classification[ii] == 0:
                contours_bins_out.append(contours_bins[ii])
                contours_contourSaliences_out.append(contours_contourSaliences[ii])
                contours_start_times_out.append(contours_start_times[ii])
        return contours_bins_out, contours_contourSaliences_out, contours_start_times_out, duration
    else:
        print 'problem with toRmIndex length, not equal.'
        return
