import PySimpleGUI as sg
import os.path

sg.theme('Black')

#window format
layout = [
    [sg.In(size=(70,1), key="_FILES_"), sg.FilesBrowse("Add Files", target="_FILES_")], #values returns the path to files
    [sg.Submit("Add")],
    [sg.Listbox(values=[], enable_events=True, size=(70, 10), key="_FILELIST_")],
    [sg.Submit("Encrypt")]
]


window = sg.Window(title="File Storage", layout=layout, margins=(250, 200), location=(0,0)) #window properties


filesAdded = []
while True:
    event, values = window.read()

    if event == "Add":
        filesAdded += values['_FILES_'].split(';') #adding new file paths
        filesAdded = list(dict.fromkeys(filesAdded)) #remove duplicates
        window["_FILELIST_"].update(values=filesAdded) #adding file paths to the visual list

    if event == sg.WIN_CLOSED:
        break

window.close()