import PySimpleGUI as sg
import os.path

sg.theme('Black')

layout = [
    [sg.Input(), sg.FileBrowse("Add Files"), sg.Button("OK")]
]

window = sg.Window(title="File Storage", layout=layout, margins=(300, 250))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

window.close()