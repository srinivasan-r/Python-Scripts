import os

import time

cwd = os.getcwd()


def getListOfFiles(dirname):
    thisDirFiles = []
    if os.path.isdir(dirname):
        listOfFiles = os.listdir(dirname)
        for file in listOfFiles:
            filePath = os.path.join(dirname, file)
            thisDirFiles.append(filePath)
            if os.path.isdir(os.path.join(dirname, file)):
                thisDirFiles = thisDirFiles + getListOfFiles(os.path.join(dirname, file))
    else:
        print "Invalid directory " + dirname
    return thisDirFiles


start_time = time.time()
dirList = os.listdir(cwd)
if 'dldb-tools' in dirList:
    processDir = cwd
else:
    dirList = filter(lambda file: os.path.isdir(os.path.join(cwd, file)), dirList)
    dirList.sort(key=lambda dirName: os.path.getmtime(os.path.join(cwd, dirName)), reverse=True)
    for i, dirName in enumerate(dirList):
        print str(i) + " " + dirName
    choice = raw_input('[' + dirList[0] + ']-->')
    if not choice:
        choice = 0
    else:
        choice = int(choice)
    processDir = os.path.join(cwd, dirList[choice])
print "Creating FileList.txt for " + processDir
f = open(os.path.join(processDir, 'FilesList.txt'), 'w')
completeFilePaths = getListOfFiles(processDir)
for file in completeFilePaths:
    f.write(file + '\n')
f.close()
print "Total time " + str(time.time() - start_time)
