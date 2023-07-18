class Machine:
    # Jede Machine hat eine ID und die Knoten/Jobschritte die darauf ausgeführt werden 

    def __init__(self, id, nodes):
        self.id = id
        self.nodes = nodes