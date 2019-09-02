from collections import deque

class UniqueQueue():
    def __init__(self, to_open=None):
        if to_open is None:
            to_open = list()
        self.opened = list()
        self.to_open = deque(to_open)

    def push_list(self, elements):
        for element in elements:
            self.push(element)

    def push(self, element):
        if element in self.opened:
            return
        elif element in self.to_open:
            return
        else:
            self.to_open.append(element)

    def pop(self):
        if self.to_open:
            element = self.to_open.popleft()
            self.opened.append(element)
            return element
        else:
            return None

    def is_empty(self):
        return len(self.to_open) == 0

    def get_all(self):
        return self.opened
