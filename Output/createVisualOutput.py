# Nach dem durchlauf soll der Plan in dieser Datei zu einem vernüftigen Tabelle gestaltet werden
from Factory.factory import Factory
from Factory.Job import Job
from Factory.Machine import Machine
from Output.NodeSchedule import NodeSchedule
import networkx as nx
from ast import List
import copy

def printOutput(schedule, unscheduledFactory):
    i = 0
    id = schedule[i].id.split(',')[1].split('(')[0]
    row = ""
    while i < len(schedule):
        if (id != schedule[i].id.split(',')[1].split('(')[0]):
            output = "Maschine: " + schedule[i-1].id.split(',')[1].split('(')[0] + row
            print(output)
            id = schedule[i].id.split(',')[1].split('(')[0]
            row = ""

        start = schedule[i].time - int(unscheduledFactory.nodes[schedule[i].id]['weight'])
        row = row + " Jobstep: " +schedule[i].id+ " Von: " +str(start)+ " Bis: " +str(schedule[i].time)
        spaces = 36 - len(row)
        while spaces > 0:
            row = row + " "
            spaces = spaces - 1
        row = row + "||"
        i = i + 1
    
    output = "Maschine: " + schedule[i-1].id.split(',')[1].split('(')[0] + row
    print(output)


def createVisualOutput(unscheduledFactory, scheduledMachinesAndEdges):

    scheduledMachinesAndEdgesCopy = copy.deepcopy(scheduledMachinesAndEdges)
    schedule:List[NodeSchedule] = []
    i = 1
    while i < len(scheduledMachinesAndEdges):
        j = 0
        while j < len(scheduledMachinesAndEdges[i][0]):
            currentNode = scheduledMachinesAndEdges[i][0][j][0]
            schedule.append(NodeSchedule(currentNode, 0))
            j = j + 1
        i = i + 1 

    while len(scheduledMachinesAndEdges) > 1:
        l = 1
        while l < len(scheduledMachinesAndEdges):
            current = scheduledMachinesAndEdges[l][0][0][0]
            currentTime = NodeSchedule.calculateTime(current, unscheduledFactory, scheduledMachinesAndEdgesCopy, schedule)
            if(currentTime !=  None):
                NodeSchedule.findNodeSchedule(current, schedule).time = currentTime
                del scheduledMachinesAndEdges[l][0][0]
                if(len(scheduledMachinesAndEdges[l][0]) == 0):
                   scheduledMachinesAndEdges.remove(scheduledMachinesAndEdges[l])
            l = l + 1

    printOutput(schedule, unscheduledFactory)