class Node():
    def __init__(self):
        self.children = list()
        self.parents = list()

    def get_children(self):
        return self.children

    def get_parents(self):
        return self.parents
