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


TOKENS = ('brace',
          'selector',
          'property',
          'equals',
          'value')

PROPERTIES = ('color', 'style')

DEFAULT_PROPERTIES = {'color': 'black',
                      'style': ''}


def create_styles(style_config):
    styles = {}
    for token in TOKENS:
        style = {}
        for property in PROPERTIES:
            try:
                style[property] = style_config['{}_{}'.format(token, property)]
            except KeyError:
                style[property] = DEFAULT_PROPERTIES[property]
        styles[token] = format(**style)
    return styles


class CssHighlighter (QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """

    def __init__(self, document, style_config):
        QSyntaxHighlighter.__init__(self, document)

        styles = create_styles(style_config)
        rules = []

        rules += [(brace, 0, styles['brace'])
                  for brace in ['\{', '\}']]

        rules += [(r'((?:(?:(?:[\w\d-]+)?[#\.])?[\w\d-]+[\s,]+)+)\{', 1, styles['selector'])]
        rules += [(r'\b([\w-]+)\s*:\s*([^;]*);', 1, styles['property'])]
        rules += [(r'\b([\w-]+)\s*:\s*([^;]*);', 2, styles['value'])]

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