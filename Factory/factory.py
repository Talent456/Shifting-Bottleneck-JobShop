from ast import List
import networkx as nx

from Factory.job import Job
from Factory.Machine import Machine

class Factory(nx.DiGraph):

    def __init__(self):
        super().__init__()
        # Anfangsknoten
        self.add_node("0", weight=0)
        #Endknoten
        self.add_node("*",weight=0)
        #critical path
        self.criticalPath = None

    def addJobtoFactory(self, job: Job):
        #job zur factory hinzufügen
        i = 0
        while i < len(job.machines):
            nameCurrent = str(job.machines[i]) +"," + str(job.id)
            namePrevious = str(job.machines[i-1]) +","+ str(job.id)
            self.add_node(nameCurrent, weight=job.processingTime[i])
            #Bei erstem Schritt eine Edge von startknoten bis zum ersten machen
            if(i == 0):
                self.add_edge("0", nameCurrent)
                i += 1
                continue
            # für die 'normalen' knoten eine Edge von Schritt zu Schritt machen
            self.add_edge(namePrevious, nameCurrent)
            i += 1
        #danach den letzten Schritt mit dem Endknoten verbinden
        self.add_edge(nameCurrent, "*")
            

    def createMachineGroupings(self, machine):
        temp= []
        for nodes in self.nodes():
            if(nodes != '0' and nodes != '*'):
                temp.append(nodes)
        temp.sort()

        for job in temp:
            machineIndex = int(job[0])
            if len(machine)-1 < machineIndex:
                machine.append(Machine(machineIndex, []))
            machine[machineIndex].addNodes(job)
        print("holy shit it actually works! xdd")