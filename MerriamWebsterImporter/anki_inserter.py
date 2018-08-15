

class AnkiInserter:

    def __init__(self, col, deck, model, max_definitions):
        self.col = col
        self.deck = deck
        self.model = model
        self.tags = "MerriamWebsterImporter"
        self.max_definitions = max_definitions

    def insert(self, input, definitions):

        if len(definitions) > 0:

            note = self.col.newNote()
            note_model = note.model()
            note_model['did'] = self.deck['id']
            note_model['id'] = self.model['id']

            note.fields[0] = input
            note.fields[1] = self._make_back_field(definitions)

            note.tags = self.col.tags.canonify(self.col.tags.split(self.tags))
            note_model['tags'] = note.tags
            self.col.addNote(note)

    def _make_back_field(self, definitions):
        amount = min(len(definitions), self.max_definitions)

        field = ""
        for i in range(amount):
            definition = definitions[i]
            field += definition
            field += "</br></br>"

        return field
