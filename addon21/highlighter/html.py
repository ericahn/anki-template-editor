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


TOKENS = ('tag',
          'element',
          'attribute',
          'equals',
          'value',
          'moustache')

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


class HtmlHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language.
    """

    def __init__(self, document, style_config):
        QSyntaxHighlighter.__init__(self, document)

        styles = create_styles(style_config)
        rules = []
        rules += [(tag, 0, styles['tag'])
                  for tag in ['<', '</', '>', '/>']]
        rules += [(r'<\/?([A-Za-z0-9_]+)>?', 1, styles['element'])]
        rules += [(r'\b([A-Za-z0-9_]+)(=)("[^"]+")', 1, styles['attribute'])]
        rules += [(r'\b([A-Za-z0-9_]+)(=)("[^"]+")', 2, styles['equals'])]
        rules += [(r'\b([A-Za-z0-9_]+)(=)("[^"]+")', 3, styles['value'])]
        rules += [(r'\{\{[#^\/]?(\w+:)?\w+\}\}', 0, styles['moustache'])]

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
