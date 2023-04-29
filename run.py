# File zum deklarien des ablaufs:
# createFactory, entweder aus Excel auslesen oder per Gui mit factoryGui 
# dann auf die Factory das SB Verfahren benutzen mit applyShiftingBottleneck
# Mit den Ergebnissen wird dann der VisualOutput erstellt

from Factory.factory import Factory
from Factory.job import Job


def createScheduling():
    jobs = {}
    jobs[1] = Job(1, [1,2,3], [10, 8, 4])
    jobs[2] = Job(2, [2,1,4,3], [8,3,5,6])
    jobs[3] = Job(3, [1,2,4], [4,7,3])

    js = Factory()
    for i in jobs.__sizeof__-1:
        js.addJobtoFactory(jobs[i])
    js.createMachineSequence(1)


