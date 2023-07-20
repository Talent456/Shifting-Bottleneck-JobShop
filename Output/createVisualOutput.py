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
    
    k = 0
    while k < len(scheduledMachinesAndEdges):
        print(scheduledMachinesAndEdges[k][0].id,  scheduledMachinesAndEdges[k][1])
        k = k + 1
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
    
  #  while len(scheduledMachinesAndEdges) > 0:
  #      l = 0
  #      while l < len(scheduledMachinesAndEdges):
  #          flag = False
  #          current = scheduledMachinesAndEdges[l][1][0][0]
  #          currentTime = NodeSchedule.findNodeSchedule(current, schedule).time
  #          currentPred = NodeSchedule.getPred(unscheduledFactory, current)
  #          currentPredTime = 0
  #          if(len(scheduledMachinesAndEdges[l][1]) == 1 ):
  #             if(NodeSchedule.checkIfAlreadyScheduled(current, currentTime, currentPred, schedule, unscheduledFactory)):
  #                  current = scheduledMachinesAndEdges[l][1][0][1]
  #                  currentPred = NodeSchedule.getPred(unscheduledFactory, current)
  #                  flag = True
  #          if(currentPred == '0'):
  #              NodeSchedule.findNodeSchedule(current, schedule).time = int(unscheduledFactory.nodes[current]['weight'])
  #              if(len(scheduledMachinesAndEdges[l][1]) != 1):
  #                  scheduledMachinesAndEdges[l][1].remove(scheduledMachinesAndEdges[l][1][0])
  #          else:
  #              currentPredTime = NodeSchedule.calculatePredTime
  #              findNodeSchedule(currentPred, schedule).time
  #          if(currentPredTime != 0):
  #              NodeSchedule.findNodeSchedule(current, schedule).time = int(unscheduledFactory.nodes[current]['weight']) + currentPredTime
  #              if(len(scheduledMachinesAndEdges[l][1]) != 1):
  #                  scheduledMachinesAndEdges[l][1].remove(scheduledMachinesAndEdges[l][1][0])
  #          if(flag):
  #              scheduledMachinesAndEdges.remove(scheduledMachinesAndEdges[l])
  #          l = l + 1

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
    while n < len(schedule):
        start = schedule[n].time - int(unscheduledFactory.nodes[schedule[n].id]['weight'])
        print("Jobstep: " +schedule[n].id+ " Von: " +str(start)+ " Bis: " +str(schedule[n].time))
        n = n + 1

            
    return schedule




    















    