# File zum deklarien des ablaufs:
# createFactory, entweder aus Excel auslesen oder per Gui mit factoryGui 
# dann auf die Factory das SB Verfahren benutzen mit applyShiftingBottleneck
# Mit den Ergebnissen wird dann der VisualOutput erstellt

from ast import List
import string
from Factory.factory import Factory
from Factory.job import Job
from Factory.Machine import Machine
import networkx as nx
from timeit import default_timer as timer


def createScheduling():
    jobs = {}
    jobs[0] = Job(1, [1, 3, 5, 2, 3], [1, 4, 7, 12, 3])
    jobs[1] = Job(2, [5, 1, 3, 2, 4], [20, 2, 4, 5, 9])
    jobs[2] = Job(3, [1, 3, 6, 5, 2], [14, 9, 8, 2, 5])
    jobs[3] = Job(4, [1, 5, 2, 3, 4], [2, 4, 6, 6, 2])
    jobs[4] = Job(5, [5, 2, 3, 4, 5], [10, 7, 5, 3, 1])

    start = 0
    end = 0
    start = timer()
    js = Factory()
    scheduledMachinesAndEdges:List[(Machine, [])] = []
    i = 0
    while i < len(jobs):
        js.addJobToFactory(jobs[i])
        i += 1
    js.createMachineGroupings()
    j = 1
    currentMachine = None
    machineCount = len(js.machines)
    while j < machineCount:
        print(j)
        currentMachine = js.findMachineWithHighestDelay()
        newEdges = js.createAndAddSchedule(currentMachine)
        k = 0
        while k < len(scheduledMachinesAndEdges):
            scheduledMachinesAndEdges[k] = js.rescheduleMachine(scheduledMachinesAndEdges[k]) 
            k = k + 1
        scheduledMachinesAndEdges.append((currentMachine, newEdges))
        j = j + 1
        js.machines.remove(currentMachine)
    end = timer()
    print(end - start)
    k = 0
    while k < len(scheduledMachinesAndEdges):
        print(scheduledMachinesAndEdges[k][0].id,  scheduledMachinesAndEdges[k][1])
        k = k + 1

    


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

