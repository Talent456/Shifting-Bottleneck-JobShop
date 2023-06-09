from ast import List
import networkx as nx

from Factory.job import Job
from Factory.Machine import Machine
import matplotlib.pyplot as plt

class Factory(nx.DiGraph):

    def __init__(self):
        super().__init__()
        # Anfangsknoten
        self.add_node("0")
        #Endknoten
        self.add_node("*")
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
                self.add_edge("0", nameCurrent, weight=job.processingTime[i])
                i += 1
                continue
            # für die 'normalen' knoten eine Edge von Schritt zu Schritt machen
            self.add_edge(namePrevious, nameCurrent,weight=job.processingTime[i])
            i += 1
        #danach den letzten Schritt mit dem Endknoten verbinden
        self.add_edge(nameCurrent, "*", weight=0)
            

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
             
    def func(self, u, v):
        return self.nodes[u]['weight']
    
    def calculateJobDelay(self, job: Job):
        invWeightGraph = self.inverseWeight()
        r = nx.bellman_ford_path_length(invWeightGraph, '0', job, 'weight') * -1
        q = nx.bellman_ford_path_length(invWeightGraph, job, '*', 'weight') * -1
        return r + q
    
    def inverseWeight(self):
        invGraph = self.copy()
        for edge in invGraph.edges:
            invGraph.edges[edge]['weight'] = invGraph.edges[edge]['weight'] * -1
        return invGraph

    def findMachineWithHighestDelay(self, machines):
        maxTupleMachine = (machines[1], 0)
        i = 1
        while i < len(machines):
            maxDelayJob = 0
            j = 0
            while j < len(machines[i].nodes):
                maxDelayJob = max(maxDelayJob, self.calculateJobDelay(machines[i].nodes[j]))
                if maxDelayJob > maxTupleMachine[1]:
                    maxTupleMachine = (machines[i], maxDelayJob)
                j = j + 1
            i = i + 1
        return maxTupleMachine[0]
    
    def createAndAddSchedule(self, currentMachine):
        jobs:List[(node, int)] = [] #tuple mit dem node und dem kürzestem path
        newEdges = []
        i = 0
        while i < len(currentMachine.nodes):
            node = currentMachine.nodes[i]
            jobs.append((node, nx.shortest_path_length(self, '0', node, 'weight')))
            i = i + 1
        jobs.sort(key=lambda x: x[1])
        j = 1 
        while j < len(jobs):
            nameCurrent = jobs[j][0]
            namePrevious = jobs[j-1][0]
            self.add_edge(namePrevious, nameCurrent,weight=0)
            newEdges.append((namePrevious, nameCurrent))

            j = j + 1
        return newEdges
    
    def rescheduleMachine(self, scheduledMachineAndEdges):
        i = 0
        while i < len(scheduledMachineAndEdges[1]):
            self.remove_edge(scheduledMachineAndEdges[1][i][0], scheduledMachineAndEdges[1][i][1])
            i = i + 1
        scheduledMachineAndEdges = (scheduledMachineAndEdges[0], self.createAndAddSchedule(scheduledMachineAndEdges[0]))

    
    #TODO: Ein-Maschinen-Problem funktioniert soweit, einmal mit paar beispielen testen ???
    
    #   Rescheduling: Ich gehe meine "neue" Liste von bereits hinzugefügten Maschinen durch und muss diese anpassen.
    #   Ich iteriere durch diese Liste:
    #       Ich entferne die edges der maschine (aus dem graphen und der liste) und suche neu die kürzesten wege
    #       füge die dann hinzu und packe die wieder in die liste
