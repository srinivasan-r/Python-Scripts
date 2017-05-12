import fileinput
import pyperclip

fileName = pyperclip.paste()

for line in fileinput.input(fileName, inplace=1):
	if 'DMSUtility.cxx' in line:
		continue
	print line.strip()
