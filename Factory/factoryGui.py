# Oberfläche zum eingeben der Factory Daten - Maschinen und Aufträge

import PySimpleGUI as sg

layout = [[sg.Text("Hier erstellen Sie die Factory")], [sg.Button("OK")]]

# Create the window
window = sg.Window("Factory Erstellen", layout, margins=(500, 200))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()