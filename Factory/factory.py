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


    #TODO: Wir haben also bisher den Graphen mit allen jobs drin sowie einer liste mit den jobs pro maschine.
    # Nun müssen wir für jede Maschine die max. Verspätung ausrechnen. 
    # Dies machen wir folgendermaßen:
    #   Für jeden Job x jeder maschine rechnen wir aus:
    #       longest path from start to x + longest path from x to end + weight x
    #       dann den höchsten wert pro maschine speichern und alle anderen durchgehen.
    #       die maschine mit dem höchsten single wert hat die höchste verspätung und wird angegangen.
    #   im detail:
    #   max map machine = 0,0    erste 0 steht für die maschine, zweite 0 steht für den delay  
    #       iterieren über die indizes des machines list
    #       max wert job = 0
    #           iterieren über die jobs/knoten in der maschine
    #               max wert job = max(calculateshit, maxwertjob)
    #       if maxwert job größer als max map maschine value
    #           then max map maschine = x,max wert job     x hier maschine
    #   return am ende die maschine id aus der map
        