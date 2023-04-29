class Job:
    # Jeder Job hat eine id, eine Reihenfolge(Liste) von Maschinen und die Bearbeitungsdauer pro Schritt(Liste)

    def __init__(self,id , machines, processingTime):
        self.id = id
        self.machines = machines
        self.processingTime = processingTime


