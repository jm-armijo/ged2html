class Edge():
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def to_html(self):
        return (
            '        new LeaderLine(\n'
            '          document.getElementById("{}"),\n'
            '          document.getElementById("{}"),\n'
            '          {{startSocket: "top", endSocket: "bottom", path: "magnet"}}\n'
            '        );\n'
        ).format(self.start, self.end)
