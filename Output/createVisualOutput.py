# Nach dem durchlauf soll der Plan in dieser Datei zu einem vernüftigen Tabelle gestaltet werden
from Factory.factory import Factory
from Factory.Job import Job
from Factory.Machine import Machine
from Output.NodeSchedule import NodeSchedule
import networkx as nx
from ast import List
import re
import copy

def createVisualOutput(unscheduledFactory, scheduledMachinesAndEdges):

    scheduledMachinesAndEdgesCopy = copy.deepcopy(scheduledMachinesAndEdges)
    schedule:List[NodeSchedule] = []
    i = 0
    while i < len(scheduledMachinesAndEdges):
        j = 0
        while j < len(scheduledMachinesAndEdges[i][1]):
            currentNode = scheduledMachinesAndEdges[i][1][j][0]
            schedule.append(NodeSchedule(currentNode, 0))
            j = j + 1
        schedule.append(NodeSchedule(scheduledMachinesAndEdges[i][1][j-1][1], 0))
        i = i + 1 

    while len(scheduledMachinesAndEdges) > 0:
        l = 0
        while l < len(scheduledMachinesAndEdges):
            flag = False
            current = scheduledMachinesAndEdges[l][1][0][0]
            currentTime = NodeSchedule.findNodeSchedule(current, schedule).time
            if(len(scheduledMachinesAndEdges[l][1]) == 1 and currentTime != 0):
                    current = scheduledMachinesAndEdges[l][1][0][1]
                    flag = True
            currentTime = NodeSchedule.calculateTime(current, unscheduledFactory, scheduledMachinesAndEdgesCopy, schedule)
            if(currentTime != None):
                NodeSchedule.findNodeSchedule(current, schedule).time = currentTime
                if(len(scheduledMachinesAndEdges[l][1]) != 1):
                    scheduledMachinesAndEdges[l][1].remove(scheduledMachinesAndEdges[l][1][0])
                if(flag):
                    scheduledMachinesAndEdges.remove(scheduledMachinesAndEdges[l])
            l = l + 1

    n = 0
    while n < len(scheduledMachinesAndEdgesCopy):
        o = 0
        output = "Maschine: " + str(scheduledMachinesAndEdgesCopy[n][0].id)
        while o < len(scheduledMachinesAndEdgesCopy[n][0].nodes):
            current = NodeSchedule.findNodeSchedule(scheduledMachinesAndEdgesCopy[n][0].nodes[o], schedule)
            start = current.time - int(unscheduledFactory.nodes[current.id]['weight'])
            output = output + " Jobstep: " +current.id+ " Von: " +str(start)+ " Bis: " +str(current.time) + " || "
            o = o + 1
        print(output)
        n = n + 1