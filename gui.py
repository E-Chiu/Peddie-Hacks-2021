import PySimpleGUI as sg
import os.path

sg.theme('Black')

#window format
layout = [
    [sg.Input(), sg.FilesBrowse("Add File", key="_FILES_")], #values returns the path to files
    [sg.Button("OK")]
]


window = sg.Window(title="File Storage", layout=layout, margins=(250, 200)) #window properties

while True:
    event, values = window.read()

    if event == "OK":
        print(values['_FILES_'].split(';')) #separate the paths

    if event == sg.WIN_CLOSED:
        break

window.close()