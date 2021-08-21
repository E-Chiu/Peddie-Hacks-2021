import PySimpleGUI as sg
import os.path

sg.theme('Black')

#window format
layout = [
    [sg.In(size=(50,1), key="_FILES_"), sg.FilesBrowse("Add Files", target="_FILES_")], #values returns the path to files
    [sg.Submit("Add")]
]


window = sg.Window(title="File Storage", layout=layout, margins=(250, 200)) #window properties


filesAdded = []
while True:
    event, values = window.read()

    if event == "Add":
        filesAdded += values['_FILES_'].split(';') #adding new file paths
        filesAdded = list(dict.fromkeys(filesAdded)) #remove duplicates
        print(filesAdded) #separate the paths

    if event == sg.WIN_CLOSED:
        break

window.close()