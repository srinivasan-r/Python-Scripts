import os
import pyperclip
import xlsxwriter

inputFile = pyperclip.paste()
print 'Converting ' + inputFile
if not os.path.exists(inputFile):
	exit()
inputDir = os.path.split(inputFile)[0]

tableList = ['Patient', 'Study', 'Stepimport', 'Reqproc', 'Sps', 'Pps', 'Series', 'Image']
t_tableList = ['t_patient', 't_study', 't_stepimport', 't_reqproc', 't_sps', 't_pps', 't_series', 't_image']
otherPerfList = ['Read', 'Update', 'QueryFlags', 'QuerySRFlags', 'Delete']
tableWSDict = {'t_patient': 'Patient', 't_study': 'Study', 't_stepimport': 'Stepimport', 't_reqproc': 'Reqproc',
			   't_sps': 'Sps', 't_pps': 'Pps', 't_series': 'Series', 't_image': 'Image'}
tableRowDict = {'t_patient': 1, 't_study': 1, 't_stepimport': 1, 't_reqproc': 1, 't_sps': 1, 't_pps': 1, 't_series': 1,
				't_image': 1}
perfRowDict = {'Read': 1, 'Update': 1, 'QueryFlags': 1, 'QuerySRFlags': 1, 'Delete': 1}
createPerfWB = xlsxwriter.Workbook(inputDir + '\CreatePerf.xlsx')
otherPerfWB = xlsxwriter.Workbook(inputDir + '\PerfAnalysis.xlsx')

wsTableDict = {}
wsPerfDict = {}
bold = createPerfWB.add_format({'bold': True})
for table in tableList:
	wsTableDict[table] = createPerfWB.add_worksheet(table)
	wsTableDict[table].write(0, 0, 'Table', bold)
	wsTableDict[table].write(0, 1, 'Average', bold)
	wsTableDict[table].write(0, 2, 'Min', bold)
	wsTableDict[table].write(0, 3, 'Max', bold)
bold = otherPerfWB.add_format({'bold': True})
for otherPerf in otherPerfList:
	wsPerfDict[otherPerf] = otherPerfWB.add_worksheet(otherPerf)
	wsPerfDict[otherPerf].write(0, 0, 'Table', bold)
	wsPerfDict[otherPerf].write(0, 1, 'Average', bold)
	wsPerfDict[otherPerf].write(0, 2, 'Min', bold)
	wsPerfDict[otherPerf].write(0, 3, 'Max', bold)
f = open(inputFile)
PatientRow = 1
for line in f:
	tokens = line.split(',')
	if len(tokens) != 4:
		continue
	col12 = tokens[0].split(':')
	if len(col12) != 2:
		continue
	typeNtable = col12[0].split()
	table = typeNtable[1].split('(')[0]
	if typeNtable[0] == 'Create':
		wsTableDict[tableWSDict[table]].write(tableRowDict[table], 0, tableWSDict[table])
		wsTableDict[tableWSDict[table]].write_number(tableRowDict[table], 1, float(col12[1].split('=')[1].strip()))
		wsTableDict[tableWSDict[table]].write_number(tableRowDict[table], 2, float(tokens[1].split('=')[1].strip()))
		wsTableDict[tableWSDict[table]].write_number(tableRowDict[table], 3, float(tokens[2].split('=')[1].strip()))
		tableRowDict[table] += 1
	else:
		perfType = typeNtable[0]
		if table == 'for':
			table = typeNtable[2].split('(')[0]
			wsPerfDict[perfType].write(perfRowDict[perfType], 0, table)
		else:
			wsPerfDict[perfType].write(perfRowDict[perfType], 0, tableWSDict[table])
		wsPerfDict[perfType].write_number(perfRowDict[perfType], 1, float(col12[1].split('=')[1].strip()))
		wsPerfDict[perfType].write_number(perfRowDict[perfType], 2, float(tokens[1].split('=')[1].strip()))
		wsPerfDict[perfType].write_number(perfRowDict[perfType], 3, float(tokens[2].split('=')[1].strip()))
		perfRowDict[perfType] += 1
for table in t_tableList:
	wsTableDict[tableWSDict[table]].write(tableRowDict[table], 0, tableWSDict[table])
	wsTableDict[tableWSDict[table]].write(tableRowDict[table], 1, '=MAX(B2:B11)')
	wsTableDict[tableWSDict[table]].write(tableRowDict[table], 2, '=MAX(C2:C11)')
	wsTableDict[tableWSDict[table]].write(tableRowDict[table], 3, '=MAX(D2:D11)')
createPerfWB.close()
otherPerfWB.close()
