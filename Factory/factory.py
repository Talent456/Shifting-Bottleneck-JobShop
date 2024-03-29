from ast import List
import networkx as nx

from Factory.Job import Job
from Factory.Machine import Machine
import matplotlib.pyplot as plt
import re
import concurrent.futures
from timeit import default_timer as timer

class Factory(nx.DiGraph):

    def __init__(self):
        super().__init__()
        # Anfangsknoten
        self.add_node("0", weight="0")
        #Endknoten
        self.add_node("*", weight="0")
        #Maschinen
        self.machines:List[Machine] = [None]

    def addJobToFactory(self, job: Job):
        #job zur factory hinzufügen
        i = 0
        nameCurrent = ''
        namePrevious = ''
        while i < len(job.machines):
            namePrevious = nameCurrent
            nameCurrent = str(job.id) + ',' + str(job.machines[i]) + '(1)'
            #j ist nach der Schleife die Anzahl der Jobsteps die bereits auf der gleichen Machine
            #des aktuellen jobs gelaufen sind, inklusive des aktuellen jobs 
            if(self.nodes.__contains__ (nameCurrent)):
                j = 2
                while True:
                    nameCurrent = str(job.id) + ',' + str(job.machines[i]) + '(' + str(j) + ')'
                    if(not(self.nodes.__contains__(nameCurrent))):
                        break
                    else:
                        j = j + 1
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
            

    def createMachineGroupings(self):
        temp= []
        #erstmal alle Knoten ohne Start und Endknoten in eine Liste packen
        for nodes in self.nodes():
            if(nodes != '0' and nodes != '*'):
                temp.append(nodes)

        #Hier wird die Liste der Maschinen anhand des letzten jobs auf die richtige Länge gestellt
        maxMachine = 0
        j = 0
        while j < len(temp):
            currentMachine = int(temp[j].split(',')[1].split('(')[0])
            if(currentMachine > maxMachine):
                maxMachine = currentMachine
            j = j + 1

        k = 1
        while k <= maxMachine:
            self.machines.append(None)
            k = k + 1

        #Die einzelnen Jobsteps werden der richtigen Maschine zugeordnet
        for jobStep in temp:
            machine = int(jobStep.split(',')[1].split('(')[0])
            if self.machines[machine] == None:
                self.machines[machine] = (Machine(machine, []))
            self.machines[machine].nodes.append(jobStep)

    #Es werden alle simplen pfade gesucht, die gewichtung berechnet und der längste genommen
    def calculateJobParams(self, job: Job):
        r = 0
        for path in nx.all_simple_paths(self, '0', job):
            weight_r = 0
            for node in path:
                weight_r = weight_r + int(self.nodes[node]['weight'])
            r = max (r, weight_r)
        q = 0
        for path in nx.all_simple_paths(self, job, '*'):
            weight_q = 0
            for node in path:
                weight_q = weight_q + int(self.nodes[node]['weight'])
            q = max (q, weight_q)
        jobWeight = int(self.nodes[job]['weight'])
        return (job, r - jobWeight, q - jobWeight, jobWeight)
    
    #findet die Maschine mit den höchsten Delay und gibt diese zurück
    def findMachineWithHighestDelay(self):
        maxSchedules:List[([], int, Machine)] = []
        i = 1
        while i < len(self.machines):
            params = []
            j = 0
            while j < len(self.machines[i].nodes):
                job = self.machines[i].nodes[j]
                params.append(self.calculateJobParams(job))
                j = j + 1
            maxSchedules.append(self.createSchedule(params, self.machines[i]))
            i = i + 1
        maxSchedules.sort(key=lambda a: a[1])
        return maxSchedules[len(maxSchedules)-1]
    
    def createSchedule(self, params, machineId):
        params.sort(key=lambda a: a[1])
        schedule:List[("", int, int)] = []
        schedule.append((params[0][0], params[0][1], params[0][3]))
        i = 1 
        while i < len(params):
            start = max(params[i][1], schedule[i-1][2])
            schedule.append((params[i][0], start, start + params[i][3]))
            i = i + 1
        
        scheduleDuration = schedule[i-1][2]
        headtailmax = 0
        j = 0
        while j < len(schedule):
            headtailmax = max(headtailmax, params[j][2] - (scheduleDuration - schedule[j][2]))
            j = j + 1

        completionTime = scheduleDuration + headtailmax
        return (schedule, completionTime, machineId)
    
    def addSchedule(self, schedule):
        i = 0
        newEdges = []
        while i < len(schedule[0]):
            j = i + 1
            nameCurrent = schedule[0][i][0]
            while j < len(schedule[0]):

                nameNext = schedule[0][j][0]
                self.add_edge(nameCurrent, nameNext,weight=0)
                newEdges.append((nameCurrent, nameNext))
                j = j + 1
            i = i + 1
        return newEdges
    
    def addScheduleMyWay(self, schedule):
        i = 0
        newEdges = []
        while i < len(schedule[0])-1:
            j = i + 1
            nameCurrent = schedule[0][i][0]
            nameNext = nameNext = schedule[0][j][0]
            self.add_edge(nameCurrent, nameNext,weight=0)
            newEdges.append((nameCurrent, nameNext))
            i = i + 1
        return newEdges
    
    #Es werden erst die alten Kanten entfernt und dann eine neue, konfliktfreie reihenfolge gefunden
    def rescheduleMachine(self, scheduledMachineAndEdges, initialGraph):
        i = 0
        while i < len(scheduledMachineAndEdges[1]):
            begin = scheduledMachineAndEdges[1][i][0]
            end = scheduledMachineAndEdges[1][i][1]
            if(not(initialGraph.has_edge(begin, end))):
                self.remove_edge(begin, end)
            i = i + 1
        params = []
        j = 0
        while j < len(scheduledMachineAndEdges[0].nodes):
            job = scheduledMachineAndEdges[0].nodes[j]
            params.append(self.calculateJobParams(job))
            j = j + 1
        schedule = self.createSchedule(params, scheduledMachineAndEdges[0].id)
        newEdges = self.addSchedule(schedule)
        return [(scheduledMachineAndEdges[0], newEdges), schedule[0]]


############Alte/Falsche Lösungen###########

    #findet die Maschine mit den höchsten Delay und gibt diese zurück
    def findMachineWithHighestDelayold(self, cutout):
        maxTupleMachine = (self.machines[1], 0)
        i = 1
        while i < len(self.machines):
            maxDelayJob = 0
            j = 0
            while j < len(self.machines[i].nodes):
                maxDelayJob = max(maxDelayJob, self.calculateJobDelay(self.machines[i].nodes[j], cutout))
                if maxDelayJob > maxTupleMachine[1]:
                    maxTupleMachine = (self.machines[i], maxDelayJob)
                j = j + 1
            i = i + 1
        return maxTupleMachine[0]

    def createAndAddScheduleOld(self, currentMachine, cutout):
        jobs:List[(node, int)] = [] #tuple mit dem node und der längsten completion time
        newEdges = []
        i = 0
        r = 0
        while i < len(currentMachine.nodes):
            node = currentMachine.nodes[i]
            for path in nx.all_simple_paths(self, '0', node, cutout):
                weight_r = 0
                for nodes in path:
                    weight_r = weight_r + int(self.nodes[nodes]['weight'])
                r = max (r, weight_r)
            jobs.append((node, r))
            r = 0
            i = i + 1
        #Die Jobs werden anhand ihrer shortest pathes, also ihrer frühsten fertigstellung
        #aufsteigend sortiert und dann die kanten dazu erstellt
        jobs.sort(key=lambda x: x[1])
        j = 1 
        while j < len(jobs):
            nameCurrent = jobs[j][0]
            namePrevious = jobs[j-1][0]
            self.add_edge(namePrevious, nameCurrent,weight=0)
            newEdges.append((namePrevious, nameCurrent))

            j = j + 1
        return newEdges


    def threadMethod(self, machine, node, delays):
        delays.append([machine, self.calculateJobDelay(node)])
    
    def findMachineWithHighestDelayAttempt(self, machines):
        delays:List[(Machine, int)] = []
        i = 1
        while i < len(machines):
            if(__name__ == '__main__'):
                executor = concurrent.futures.ProcessPoolExecutor(len(machines[i].nodes))
                futures = [executor.submit(self.threadMethod ,self , machines[i], node, delays) for node in machines[i].nodes]
                concurrent.futures.wait(futures)
            i = i + 1
        return max(delays, key=lambda item: item[1])[0]
    
    #nicht nutzbar da keine negativen zyklen verarbeitbar sind
    def calculateJobDelayOld(self, job: Job):
        invWeightGraph = self.inverseWeight()
        r = nx.bellman_ford_path_length(invWeightGraph, '0', job, 'weight') * -1
        q = nx.bellman_ford_path_length(invWeightGraph, job, '*', 'weight') * -1
        return r + q
    
    def inverseWeight(self):
        invGraph = self.copy()
        for edge in invGraph.edges:
            invGraph.edges[edge]['weight'] = invGraph.edges[edge]['weight'] * -1
        return invGraph