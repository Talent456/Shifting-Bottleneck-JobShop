# File zum deklarien des ablaufs:
# createFactory, entweder aus Excel auslesen oder per Gui mit factoryGui 
# dann auf die Factory das SB Verfahren benutzen mit applyShiftingBottleneck
# Mit den Ergebnissen wird dann der VisualOutput erstellt

from ast import List
import Output.createVisualOutput as output
from Factory.factory import Factory
from Factory.Job import Job
from Factory.Machine import Machine
import networkx as nx
from timeit import default_timer as timer
import copy


def createScheduling():
    jobs = {}
    jobs[0] = Job(1, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [12, 5, 7, 3, 3, 8, 10, 4, 3, 2, 9, 5, 1, 1, 5])	
    jobs[1] = Job(2, [11, 5, 4, 12, 3, 6, 7, 15, 12, 13, 14, 5, 2, 13, 9], [4, 11, 5, 1, 1, 5, 9, 2, 3, 4, 1, 8, 3, 3, 7])	

    




    start = 0
    end = 0
    start = timer()
    js = Factory()
    scheduledMachinesAndEdges:List[(Machine, [])] = []
    i = 0
    while i < len(jobs):
        js.addJobToFactory(jobs[i])
        i += 1
    initialGraph = js.copy()
    js.createMachineGroupings()
    j = 1
    currentMachine = None
    machineCount = len(js.machines)
    scheduleForOutput:List[(Machine, [])] = []
    i = 0
    while i < machineCount:
        scheduleForOutput.append(None)
        i = i + 1
    while j < machineCount:
        print(j)
        maxCompletionSchedule = js.findMachineWithHighestDelay()
        currentMachine = maxCompletionSchedule[2]
        scheduleForOutput[currentMachine.id] = (maxCompletionSchedule[0], currentMachine)
        newEdges = js.addSchedule(maxCompletionSchedule)
        k = 0
        while k < len(scheduledMachinesAndEdges):
            reschedule = js.rescheduleMachine(scheduledMachinesAndEdges[k], initialGraph)
            scheduledMachinesAndEdges[k] = reschedule[0]
            scheduleForOutput[scheduledMachinesAndEdges[k][0].id] = (reschedule[1], scheduledMachinesAndEdges[k][0])
            k = k + 1
        scheduledMachinesAndEdges.append((currentMachine, newEdges))

        j = j + 1
        js.machines.remove(currentMachine)
    end = timer()
    print(end - start)

    output.createVisualOutput(initialGraph, scheduleForOutput)


    


createScheduling()


#Ablauf des Programms:
#   Jobs einlesen und Graph erstellen -> Done

#   Gesamtbearbeitungszeit aller Jobs herausfinden(job der am längsten braucht) Cakt, but why ????? erstmal weglassen

#   Loop über alle Maschinen:
#       Verspätung für alle Maschinen berechnen, pro job auf maschine rij= längster weg von anfang bis zu dem node; qij= längster weg von job bis *; pij= weight des jobs selber
#           Diese werte pro job zusammenrechnen und den maximalwert nehmen. Dann die Maschine nehmen wo dieser wert am höchsten ist. -> Done

#       auf dieser maschine dann die ideale Reihenfolge bestimmen: Die reihenfolge nehmen wo die verspätung so gering wie möglich ist ? Erstmal FCFS
#       dann für die reihenfolge neue edges hinzufügen
#       die Maschine aus dem "Bearbeitungspool" entfernen (und neue Gesamtbearbeitungszeit berechnen)
#       Rescheduling: durch die Maschinen aus dem "Fertigpool" iterieren -> den schedule entfernen und neuen schedule mit den neuen edges
#       DONE!

#   Probleme: Wie gehen wir mit negativen zyklen um ? Ersetze bellman-ford durch algo der das kann(gibt es nicht) ODER negative zyklen vermeiden bei der anlage (kp wie das aussehen soll) 

