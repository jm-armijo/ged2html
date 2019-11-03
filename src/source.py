class Source():
    def __init__(self, id):
        self.id = id
        self.title = ''
        self.text = ''
        self.objects = list()

    def add_object(self, object):
        self.objects.append(object)
