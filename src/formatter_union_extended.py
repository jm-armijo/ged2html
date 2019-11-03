from src.formatter_factory import FormatterFactory

class UnionExtendedFormatter():
    def __init__(self, union_extended):
        self.union_extended = union_extended

    def format(self):
        if self.union_extended.is_private():
            return ''

        html = ''
        for node in self.union_extended.nodes:
            formatter = FormatterFactory.make(node)
            html += formatter.format()

        return html

FormatterFactory.register('UnionExtended', UnionExtendedFormatter)
