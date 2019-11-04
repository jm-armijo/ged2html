class ParsePath():
    def __init__(self):
        self.path = dict()

    def get_object_at(self, level):
        return self._get_val_at(level, 1)

    def get_key_at(self, level):
        return self._get_val_at(level, 0)

    def _get_val_at(self, level, idx):
        if level in self.path:
            return self.path[level][idx]
        else:
            return None

    def set_current(self, level, key, object):
        level = int(level)
        self._clear_after_level(level)
        self.path[level] = (key, object)

    def print(self):
        for key, value in self.path.items():
            print("{} {}\n".format(key, type(value)))

# private:

    def _clear_after_level(self, level):
        while level+1 in self.path:
            del self.path[level+1]
            level += 1
