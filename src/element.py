class Element():
    def __init__(self):
        self.sources = list()
        self.objects = list()
        self.notes = list()

    def add_note(self, note_id):
        self.notes.append(note_id)

    def add_source(self, source_id):
        self.sources.append(source_id)
