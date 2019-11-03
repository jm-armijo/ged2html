from src.date import Date

# pylint: disable=too-few-public-methods
class UnionLink():
    def __init__(self, union_id):
        self.id = union_id
        self.date = Date()
        self.place = ''

    def is_private(self):
        return True
