# Hier wird mithilfe der GUI oder der Excel Datei die Factory als nutzbares Objekt gebaut
from factory import Factory
import pandas as pd
import pathlib

def createFactory():
    # Manuell Factory erstellen, gibt sie danach zurück
    order1 = [(0,3), (1,7), (2,13)]
    order2 = [(2,9), (0,2), (1,7)]
    order3 = [(1,4), (1,7), (2,3)]
    machines = 3
    factory = Factory(machines, [order1, order2, order3])
    print(factory.machines)
    print(factory.jobs)
    return factory



createFactory()