def registerFilter(minCents, maxCents, pitchContour):
    '''
    delete pitch contour outside register
    False: remove
    True: keep
    '''
    ii = 0
    for pitch in pitchContour:
        if pitch > maxCents or pitch < minCents:
            ii += 1
            if ii >= 5:
                return False
    return True

def hz2centsbin(pitchHz, binResolution):
    centsbin = 1200 * np.log2(pitchHz/55.0) / binResolution
    return centsbin


minCents = hz2centsbin(minPitch, binResolution)
maxCents = hz2centsbin(maxPitch, binResolution)

toRmIndex = []
for ii in range(len(pitchContours)):
    r = registerFilter(minCents, maxCents, pitchContours[ii])
    if r == False:
        toRmIndex.append(ii)
