class Edge:
    def __init__(self, source: str, target: str, relation: str):
        self.source = source
        self.target = target
        self.relation = relation 

    def to_tuple(self):
        return (self.source, self.target, {"relation": self.relation})

        
        



        