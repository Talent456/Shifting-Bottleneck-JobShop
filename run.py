# File zum deklarien des ablaufs:
# createFactory, entweder aus Excel auslesen oder per Gui mit factoryGui 
# dann auf die Factory das SB Verfahren benutzen mit applyShiftingBottleneck
# Mit den Ergebnissen wird dann der VisualOutput erstellt

from Factory.factory import Factory
from Factory.job import Job


def createScheduling():
    jobs = {}
    jobs[0] = Job(1, [2,3,4], [10, 8, 4])
    jobs[1] = Job(2, [2,1,4,3], [8,3,5,6])
    jobs[2] = Job(3, [1,2,4], [4,7,3])

    js = Factory()
    i = 0
    while i < len(jobs):
        js.addJobtoFactory(jobs[i])
        i += 1
    js.createMachineSequence(1)


createScheduling()


#Ablauf des Programms:
#   Jobs einlesen und Graph erstellen -> Done
#   Gesamtbearbeitungszeit aller Jobs herausfinden(job der am längsten braucht) Cakt
#   Loop über alle Maschinen:
#       Verspätung für alle Maschinen berechnen, pro job auf maschine rij= längster weg von anfang bis zu dem node; qij= längster weg von job bis *; pij= weight des jobs selber
#           Diese werte pro job zusammenrechnen und den maximalwert nehmen. Dann die Maschine nehmen wo dieser wert am höchsten ist.
#       auf dieser maschine dann die ideale Reihenfolge bestimmen: Die reihenfolge nehmen wo die verspätung so gering wie möglich ist ?
#       dann für die reihenfolge neue edges hinzufügen
#       die Maschine aus dem "Bearbeitungspool" entfernen und neue Gesamtbearbeitungszeit berechnen
#       Rescheduling: durch die Maschinen aus dem "Fertigpool" iterieren -> den schedule entfernen und neuen schedule mit den neuen edges
#       DONE!
