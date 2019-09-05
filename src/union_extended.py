from src.node import Node
import pdb

class UnionExtended(Node):
    def __init__(self):
        self.unions = list()
        self.nodes = list()

    def add_union(self, union):
        spouse1 = union.get_spouse1()
        spouse2 = union.get_spouse2()

        self.unions.append(union)
        # [spouse3, spouse2]

        spouse1_pos = self.nodes.index(spouse1) if spouse1 in self.nodes else None
        spouse2_pos = self.nodes.index(spouse2) if spouse2 in self.nodes else None

        if spouse1_pos is None and spouse2_pos is not None:
            if spouse2_pos == 0:
                self.nodes.insert(0,spouse1)
            else:
                self.nodes.insert(spouse2_pos+1,spouse1)
        elif spouse2_pos is None and spouse1_pos is not None:
            if spouse1_pos == 0:
                self.nodes.insert(0,spouse2)
            else:
                self.nodes.insert(spouse1_pos+1,spouse2)
        else:
            self.nodes.append(spouse1)
            self.nodes.append(spouse2)


    def get_unions(self):
        return self.unions

    def get_children(self):
        children = []
        for union in self.unions:
            children += union.get_children()
        return children

    def to_html(self):
        pass
