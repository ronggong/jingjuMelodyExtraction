# -*- coding: utf-8 -*-

import pitchContours as pc
import directoryGetter as dg
import json
import os

# get filename from voice audio folder
rootVoice = '/home/rgong/Music/bestQuality'
filenamesVoice = dg.filenameGetter(rootVoice)

# write json output filenames to jsonfilenames
outputFolderVoice = '/home/rgong/MTG/jingjuMelody/voicePitchContours'
filenameJsonVoice = dg.filenameJson(filenamesVoice, outputFolderVoice)

# get filename from non voice audio folder
rootNonvoice = '/home/rgong/Music/bgtracks'
filenamesNonvoice = dg.filenameGetter(rootNonvoice)

# write json output filenames to jsonfilenames
outputFolderNonvoice = '/home/rgong/MTG/jingjuMelody/nonvoicePitchContours'
filenameJsonNonvoice = dg.filenameJson(filenamesNonvoice, outputFolderNonvoice)

pitchMakam = pc.PitchExtractMakam()
pitchMakam.setup()

# write pitch contours
for ii in range(len(filenamesVoice)):
    print 'extract pitch contours of ', ii
    contours_bins, contours_contourSaliences, contours_start_times, duration = pitchMakam.run(filenamesVoice[ii])

    with open(filenameJsonVoice[ii], 'w') as outfile:
        data = {'contours_bins': contours_bins, 'contours_contourSaliences': contours_contourSaliences, 'contours_start_times': contours_start_times.tolist(), 'duration': duration}
        json.dump(data, outfile)

for ii in range(len(filenamesNonvoice)):
    print 'extract pitch contours of ', ii
    contours_bins, contours_contourSaliences, contours_start_times, duration = pitchMakam.run(filenamesNonvoice[ii])

    with open(filenameJsonNonvoice[ii], 'w') as outfile:
        data = {'contours_bins': contours_bins, 'contours_contourSaliences': contours_contourSaliences, 'contours_start_times': contours_start_times.tolist(), 'duration': duration}
        json.dump(data, outfile)
