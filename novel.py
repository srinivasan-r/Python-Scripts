console.clear()
text = editor.getText()
console.write(text)
editor.addText("\n")
for i in range(41,75):
	editor.addText(text + str(i)+"\n")
console.write("DOne")