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


def wrap_key(text_edit):
    original_key_press = text_edit.keyPressEvent

    def key_press(event):
        if event.key() == Qt.Key_Tab:
            text_edit.insertPlainText('  ')
        else:
            original_key_press(event)

    text_edit.keyPressEvent = key_press


def attach_highlighter(self):
    mw.my_widgets = []
    editors = {'html': [self.tform.front, self.tform.back],
               'css':  [self.tform.css]}
    languages = ('html', 'css')

    config = mw.addonManager.getConfig(__name__)

    profiles = {}
    for language in languages:
        try:
            profile_name = config['user'][language]
        except KeyError:
            profile_name = 'default'
        profiles[language] = config[language][profile_name]

    # TODO: test this on other platforms besides Linux
    monospace = QFont('Monospace')
    monospace.setStyleHint(QFont.TypeWriter)
    mw.my_widgets.append(monospace)

    for language, text_edits in editors.items():
        for text_edit in text_edits:
            text_edit.setFont(monospace)
            # wrap_key(text_edit)
            highlighter = highlighters[language]
            highlighter_widget = highlighter(text_edit.document(), profiles[language]['style'])
            mw.my_widgets.append(highlighter_widget)


CardLayout.readCard = wrap(CardLayout.readCard, attach_highlighter)
