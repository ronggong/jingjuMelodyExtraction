import os

def filenameGetter(root):
    '''
    get all filenames in root
    '''
    filenames = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.endswith('.wav') or name.endswith('.mp3'):
                filenames.append(os.path.join(path, name))
    return filenames

def filenameJson(filenames, outputFolder):
    '''
    read filename, change it to .json, add outputFolder
    '''
    jsonfilenames = []
    for fn in filenames:
        head,tail = os.path.split(fn)
        tail = tail[:-4] + '.json'
        jsonfn = os.path.join(outputFolder, tail)
        jsonfilenames.append(jsonfn)
    return jsonfilenames

def jsonFilenameGetter(root):
    '''
    get all filenames in root
    '''
    filenames = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.endswith('.json'):
                filenames.append(os.path.join(path, name))
    return filenames

