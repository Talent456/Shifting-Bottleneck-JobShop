class NodeSchedule:
    # jeder Schedule hat den node als string und den fertigstellungszeitpunkt

    def __init__(self, id, time):
        self.id = id
        self.time = time

    def getJobPred(unscheduledFactory, current):
        currentPred = str(unscheduledFactory.in_edges(current))
        start = currentPred.find("[('") + 3
        end = currentPred.find("', ", start)
        return currentPred[start:end]
    
    def getMachinePred(current, scheduledMachinesAndEdges):
        machineNumber = int(current.split(',')[1].split('(')[0])
        i = 1
        while i < len(scheduledMachinesAndEdges):
            if(scheduledMachinesAndEdges[i][1].id == machineNumber):
                j = 0
                while j < len(scheduledMachinesAndEdges[i][0]):
                    if(scheduledMachinesAndEdges[i][0][j][0] == current):
                        if(j == 0):
                            return None
                        return scheduledMachinesAndEdges[i][0][j-1][0]
                    j = j + 1
                return None
            i = i + 1
    
    def findNodeSchedule(current, schedule):
        i = 0
        while i < len(schedule):
            if(schedule[i].id == current):
                return schedule[i]
            i = i + 1
    
    def calculateTime(current, unscheduledFactory, scheduledMachinesAndEdgesCopy, schedule):
        #Job kann '0' sein, dann 
        currentJobPred = NodeSchedule.getJobPred(unscheduledFactory, current)

        if(currentJobPred == '0'):
            currentJobPredTime = 0
        else:
            currentJobPredTime = NodeSchedule.findNodeSchedule(currentJobPred, schedule).time
            if(currentJobPredTime == 0):
                return None

        currentMachinePred = NodeSchedule.getMachinePred(current, scheduledMachinesAndEdgesCopy)
        if(currentMachinePred == None):
            currentMachinePredTime = 0
        else:
            currentMachinePredTime = NodeSchedule.findNodeSchedule(currentMachinePred, schedule).time
            if(currentMachinePredTime == 0):
                return None


        return max(int(currentJobPredTime), int(currentMachinePredTime)) + int(unscheduledFactory.nodes[current]['weight'])