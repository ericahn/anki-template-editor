# syntax.py

import sys

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *


def format(color, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages
STYLES = {
    'tag': format('brown'),
    'element': format('darkMagenta', 'bold'),
    'attribute': format('green'),
    'equals': format('gray'),
    'value': format('blue'),
    'moustache': format('red', 'bold')
}


class HtmlHighlighter (QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        rules += [(tag, 0, STYLES['tag'])
                  for tag in ['<', '</', '>', '/>']]

        rules += [(r'<\/?([A-Za-z0-9_]+)>?', 1, STYLES['element'])]
        rules += [(r'\b([A-Za-z0-9_]+)(=)("[^"]+")', 1, STYLES['attribute'])]
        rules += [(r'\b([A-Za-z0-9_]+)(=)("[^"]+")', 2, STYLES['equals'])]
        rules += [(r'\b([A-Za-z0-9_]+)(=)("[^"]+")', 3, STYLES['value'])]

        rules += [(r'\{\{[#^\/]?(\w+:)?\w+\}\}', 0, STYLES['moustache'])]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text.
        """
        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        pass