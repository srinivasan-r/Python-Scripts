import os
import re

dirPath = 'C:\\Users\\305022193\\Downloads\\ReZero kara Hajimeru Isekai Seikatsu\\'
fileNamePattern = re.compile(r'[^\d]+(\d+)')
for file in os.listdir(dirPath):
    newFile = "ReZero kara Hajimeru Isekai Seikatsu Episode " + re.match(fileNamePattern, file).group(1) + ".mp4"
    print file + "==>" + newFile
    os.rename(dirPath + file, dirPath + newFile)
