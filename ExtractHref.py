import re
console.clear()
# First we'll start an undo action, then Ctrl-Z will undo the actions of the whole script
editor.beginUndoAction()
def extractHref(contents, lineNumber, totalLines):
	# As we've deleted the line, the "next" line to process
	# is actually the current line, so we return 0 to advance zero lines
	# and hence stay on the same line
	# return 0
	m = re.search(r'<a[^>]* href="([^"]*)".*', contents)
	if m:
		editor.replaceLine(lineNumber, m.group(1))

	# Here we return 2, as we've inserted a newline,
	# and we don't want to test the "SOMETHING" line again
	# return 2

	# if you wanted, you could optionally return 1 here, to move the next line
	# but that's the default, so you don't need to bother.


editor.forEachLine(extractHref)

console.write("Complete\r\n")
# End the undo action, so Ctrl-Z will undo the above two actions
editor.endUndoAction()