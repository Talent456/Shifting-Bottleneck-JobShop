class Step:
    # Ein Step ist ein Auftragsschritt. Ein Step hat eine Maschine an die er ausgeführt wird und dazu die Dauer der Bearbeitung
    machine = 0
    duration = 0
    def __init__(self, machine, duration):
        self.machine = machine
        self.duration = duration


