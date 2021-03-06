An Anki addon that adds fixed-width text and syntax highlighting to the card template editor

One drawback to the otherwise powerful Anki template editor is the absence of two common features of text editors:

1. fixed width (monospace) text
2. syntax highlighting

A common ad-hoc workaround was to copy & paste between the Anki template editor and a separate text editor.
This addon provides these missing features directly in the template editor.
Syntax highlighting works for both HTML and CSS, although currently the lexing is naive.
Also, by default the addon converts tabs to 2 spaces; this will be configurable in later versions.

Example:
![Screenshot of editor](https://raw.githubusercontent.com/ericahn/anki-template-editor/master/docs/screenshots/shot4.png)

Next steps:

* configurable highlighting (colors, tokens)
* better syntax highlighting
* line numbers
* search & replace
* automatic indentation

