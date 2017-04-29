import re
console.clear()
# First we'll start an undo action, then Ctrl-Z will undo the actions of the whole script
editor.beginUndoAction()

for i in range(1,20):
	editor.rereplace("  ", " ")
editor.replace("\r\n ", "\r\n")
editor.replace("\r\n\r\n", "\r\n")
console.write("space and newline process complete\r\n")
for i in range(1,4):
	editor.rereplace(r"<code.*?>([^<]+)</code>", "$1", re.DOTALL)
	editor.rereplace(r"<a.*?>([^<]+)</a>", "$1", re.DOTALL)
	editor.rereplace(r"<span.*?>([^<]+)</span>", "$1", re.DOTALL)
	editor.rereplace(r"<tt[^>]*>([^<]+?)(</tt>)", "$1", re.DOTALL)
	editor.rereplace(r"<acronym[^>]*>([^<]+?)(</acronym>)", "$1", re.DOTALL)
	editor.rereplace(r"<p>([^<]+)</p>", "$1", re.DOTALL)
console.write("sub tag replace complete\r\n")
for i in range(1,40):
	editor.rereplace(r"<li>(\r\n)?([^<\r\n]*)(\r\n)([^<]*)(\r\n)?</li>", "<li>$2 $4</li>", re.DOTALL)
console.write("para to line complete\r\n")
editor.rereplace(r"<li>([^<]+) ?</li>", "$1", re.DOTALL)
editor.replace(" <ul>\r\n", "")
editor.replace(" \r\n</ul>", "")
console.write("Complete\r\n")
# End the undo action, so Ctrl-Z will undo the above two actions
editor.endUndoAction()