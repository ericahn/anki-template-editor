import os

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

from anki.hooks import wrap
from aqt.clayout import CardLayout


from . import css
from . import html


highlighters = {'html': html.HtmlHighlighter,
                'css': css.CssHighlighter}


def showMore(obj):
    showInfo('Type: {}\nstr(): {}'.format(type(obj), str(obj)))


def attach_highlighter(self):
    editors = {'html': [], 'css': []}
    # Detect if in Anki 2.1 or 2.0
    try:
        # Anki 2.1
        tforms = [self.tform]
    except AttributeError:
        # Fall back to Anki 2.0.47
        tforms = [form['tform'] for form in self.forms]

    for tform in tforms:
        editors['html'] += [tform.front, tform.back]
        editors['css'] += [tform.css]

    # TODO: test this on other platforms besides Linux
    monospace = QFont('')
    monospace.setStyleHint(QFont.TypeWriter)

    for language, tforms in editors.items():
        for tform in tforms:
            tform.setFont(monospace)
            highlighter = highlighters[language]
            highlighter(tform.document())


CardLayout.readCard = wrap(CardLayout.readCard, attach_highlighter)
