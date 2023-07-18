from ast import List


class Machine:
    # Jede Machine hat eine ID und die Knoten/Jobschritte die darauf ausgeführt werden 

    def __init__(self, id, nodes:List):
        self.id = id
        self.nodes = nodes

    def getNodes(self):
        return self.nodes
    
    def getId(self):
        return self.id