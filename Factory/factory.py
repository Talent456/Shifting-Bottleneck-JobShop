import networkx as nx

from Factory.job import Job

class Factory(nx.DiGraph):

    def __init__(self):
        super().__init__()
        # Anfangsknoten
        self.add_node("0")
        #Endknoten
        self.add_node("*")
        #critical path
        self.criticalPath = None

#GEWICHT MUSS AN DEN NODE NICHT AN DIE EDGE
    def addJobtoFactory(self, job: Job):
        #job zur factory hinzufügen
        i = 0
        while i < len(job.machines):
            #Bei erstem Schritt eine Edge von startknoten bis zum ersten machen
            if(i == 0):
                self.add_edge("0", str(job.machines[i]) +"," + str(job.id), weight=job.processingTime[i])
                i += 1
                continue
            # für die 'normalen' knoten eine Edge von Schritt zu Schritt machen
            self.add_edge(str(job.machines[i-1]) +","+ str(job.id), str(job.machines[i]) +","+ str(job.id), weight=job.processingTime[i])
            i += 1
        #danach den letzten Schritt mit dem Endknoten verbinden
        self.add_edge(str(job.machines[i-1]) +","+ str(job.id), "*", weight=0)
            

    def createMachineSequence(self, maschineId):
        nodesForMachine = []
        for i in self.nodes:
           print("test")
        #Todo maschine und id in node reinschreiben dann alle nodes mit startwith maschine reinschreiben