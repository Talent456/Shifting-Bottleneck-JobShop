class Factory:
    # Die Factory beinhaltet die Maschinen und die Aufträge für diesen Durchlauf
    machines = 0
    jobs = [[]]

    def __init__(self, machines, jobs):
        self.machines = machines
        self.jobs = jobs


