class Object():
    def __init__(self, object_id):
        self.id = object_id
        self.file = ''
        self.format = ''
        self.title = ''

    def set_file(self, file):
        self.file = file

    def set_format(self, format):
        self.format = format
