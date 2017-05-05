import ctypes
import fileinput

CF_TEXT = 1

kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

fileName = ''
user32.OpenClipboard(0)
if user32.IsClipboardFormatAvailable(CF_TEXT):
	data = user32.GetClipboardData(CF_TEXT)
	data_locked = kernel32.GlobalLock(data)
	text = ctypes.c_char_p(data_locked)
	fileName = text.value
	print(text.value)
	kernel32.GlobalUnlock(data_locked)
else:
	print('no text in clipboard')
user32.CloseClipboard()

for line in fileinput.input(fileName, inplace=1):
	if 'DMSUtility.cxx' in line:
		continue
	print line.strip()
