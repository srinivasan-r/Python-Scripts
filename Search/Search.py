import mmap
import os
import time
from datetime import datetime
from multiprocessing import Process, Lock

cwd = os.getcwd()
# searchStr = 'dM0@n$I}s6B42iR'
searchStr = 'DBAccess'
searchDir = 'C:\Viewstore\Cerber_SSA_2.5.1'
ignoreFileSize = 20 * 1024 * 1024
ignoreExts = ['.pdb', '.exe', '.obj', '.dll', '.lib']


def getListOfFiles(dirname):
	thisDirFiles = []
	if os.path.isdir(dirname):
		listOfFiles = os.listdir(dirname)
		for file in listOfFiles:
			filePath = os.path.join(dirname, file)
			if os.path.isdir(os.path.join(dirname, file)):
				thisDirFiles = thisDirFiles + getListOfFiles(os.path.join(dirname, file))
			else:
				if filePath[-4:] not in ignoreExts:
					thisDirFiles.append(filePath)
	else:
		print "Invalid directory " + dirname
	return thisDirFiles


def searchFiles(lock, resultFileName, filesList):
	result = []
	for file in filesList:
		if os.path.getsize(file) > ignoreFileSize or os.path.getsize(file) == 0:
			continue
		f = open(file)
		mmapF = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
		if mmapF.find(searchStr) != -1:
			result.append(file + '\n')
			i = 0;
			for line in f:
				i = i + 1
				if searchStr in line:
					result.append('\tline ' + str(i) + ': ' + line)
			result.append('\n')
		mmapF.close()
		f.close()
	lock.acquire()
	resultFile = open(resultFileName, 'a')
	resultFile.write('\n')
	for line in result:
		resultFile.write(line)
	resultFile.close()
	lock.release()


if __name__ == '__main__':
	start_time = time.time()
	print "Searching " + searchDir
	resultFileName = os.path.join(cwd, datetime.now().strftime('SearchResult_%Y_%m_%d_%H_%M.txt'))
	completeFilePaths = getListOfFiles(searchDir)
	x4 = len(completeFilePaths) / 4
	x2 = len(completeFilePaths) / 2
	lock = Lock()
	processes = []
	processes.append(Process(target=searchFiles, args=(lock, resultFileName, completeFilePaths[:x4],)))
	processes.append(Process(target=searchFiles, args=(lock, resultFileName, completeFilePaths[x4:x2],)))
	processes.append(Process(target=searchFiles, args=(lock, resultFileName, completeFilePaths[x2:x2 + x4],)))
	processes.append(Process(target=searchFiles, args=(lock, resultFileName, completeFilePaths[x2 + x4:],)))
	for process in processes:
		process.start()
	print 'Waiting for processes to complete'
	for process in processes:
		process.join()
	resultFile = open(resultFileName, 'a')
	resultFile.write('\n\n' + "Total time " + str(time.time() - start_time))
	resultFile.close()
