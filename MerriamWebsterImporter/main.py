from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from MerriamWebsterImporter.dict_parser import DictParser
from MerriamWebsterImporter.input_dialog import InputDialog
from MerriamWebsterImporter.anki_inserter import AnkiInserter
from definition_importer import deck_name


def run():

    # getting input
    #################################################

    data = InputDialog().run()
    if not data:
        return

    text, definitions_amount = data
    inputs = parse_input(text)

    # setup anki collection for insertions
    #################################################

    # select deck
    deck_id = mw.col.decks.id(deck_name, create=True)
    mw.col.decks.select(deck_id)
    deck = mw.col.decks.current()

    # select model
    model = mw.col.models.byName("Basic")
    model['did'] = deck_id

    deck['mid'] = model['id']
    mw.col.decks.save(deck)
    mw.col.models.save()

    # parsing and inserting
    #################################################

    inserter = AnkiInserter(mw.col, deck, model, definitions_amount)
    not_found = []
    count = 0
    for input in inputs:
        definitions = DictParser.parse(input)
        if len(definitions) < 1:
            not_found.append(input)
        else:
            count += 1
            inserter.insert(input, definitions)

    # end message
    #################################################

    text = ""
    if count == 1:
        text += "One card successfully created. "
    elif count == 0:
        text += "No definitions found. "
    else:
        text += "{} cards successfully created. ".format(count)

    if len(not_found) > 0:
        text += "\n\nErrors occurred with: \n"
        for input in not_found:
            text += "- {} \n".format(input)

    showInfo(text)


def parse_input(input):

    lines = set([])
    for line in input.split('\n'):
        lines.add(line.encode('utf-8'))

    lines.discard(u'')
    return list(lines)


importAction = QAction("Import Definitions", mw)
importAction.triggered.connect(run)
mw.form.menuTools.addAction(importAction)
