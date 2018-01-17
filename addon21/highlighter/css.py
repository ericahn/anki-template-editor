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
    'brace': format('#BB7977'),
    'selector': format('#800000', 'bold'),
    'property': format('#BB7977', 'bold'),
    'equals': format('gray'),
    'value': format('#074726')
}


class CssHighlighter (QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        rules += [(brace, 0, STYLES['brace'])
                  for brace in ['\{', '\}']]

        rules += [(r'((?:(?:(?:[\w\d-]+)?[#\.])?[\w\d-]+[\s,]+)+)\{', 1, STYLES['selector'])]
        rules += [(r'\b([\w-]+)\s*:\s*([^;]*);', 1, STYLES['property'])]
        rules += [(r'\b([\w-]+)\s*:\s*([^;]*);', 2, STYLES['value'])]

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