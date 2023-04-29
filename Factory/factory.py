import networkx as nx

from Factory.job import Job

class Factory(nx.DiGraph):

    def __init__(self):
        super().__init__()
        # Anfangsknoten
        self.add_node("0")
        #Endknoten
        self.add_edge("*")
        #critical path
        self.criticalPath = None

    def addJobtoFactory(self, job: Job):
        #job zur factory hinzufügen
        for i in job.machines.__sizeof__-1:
            #Bei erstem Schritt eine Edge von startknoten bis zum ersten machen
            if(i == 0):
                self.add_edge("0", job.machines[i] +","+ job.id, weight=job.processingTime[i])
                continue
            # für die 'normalen' knoten eine Edge von Schritt zu Schritt machen
            self.add_edge(job.machines[i-1] +","+ job.id, job.machines[i] +","+ job.id, weight=job.processingTime[i])
        #danach den letzten Schritt mit dem Endknoten verbinden
        self.add_edge(job.machines[job.machines.__sizeof__-1] +","+ job.id, "*", weight=0)
            

    def createMachineSequence(self, maschineId):
        nodesForMachine = []
        for i in self.nodes:
           print("test")
        #Todo maschine und id in node reinschreiben dann alle nodes mit startwith maschine reinschreiben