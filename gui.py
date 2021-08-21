import PySimpleGUI as sg
import main_Backend as crypt

sg.SetOptions(background_color='#000',
    text_element_background_color='#9FB8AD',
    element_background_color='#9FB8AD',
    scrollbar_color=None,
    input_elements_background_color='#FFF',
    button_color=('black','#FFF'))

encryptColumn = [
    [sg.In(size=(32,1), key="_NEW-PROF-IN_", enable_events=True), sg.Button("Add New Profile", key="_NEW-PROF_", size=(15,1))],
    [sg.Combo([], size=(30,1), key="_PROFILES_"), sg.Button("Remove Current Profile", key="_REMOVE-PROF_", size=(20,1))],
    [sg.In(size=(70,1), key="_FILES_"), sg.FilesBrowse("Add Files", target="_FILES_")], #values returns the path to files
    [sg.Submit("Add")],
    [sg.Listbox(values=[], enable_events=True, size=(70, 10), key="_FILE-ENCRYPT-LIST_")],
    [sg.Submit("Encrypt"), sg.Submit("Decrypt")]
]

#window format
layout = [
        [sg.Column(encryptColumn, justification="center")]
    ]


window = sg.Window(title="File Encryptor", layout=layout, margins=(10, 50), location=(0,0), size=(1150, 600)) #window properties

filesAdded = []
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if len(values["_NEW-PROF-IN_"]) >= 30:
        window["_NEW-PROF-IN_"].update(values["_NEW-PROF-IN_"][:-1])

    if event == "_NEW-PROF-IN_":
        continue

    if event == "_NEW-PROF_":
        continue

    if event == "Add":
        filesAdded += values['_FILES_'].split(';') #adding new file paths
        filesAdded = list(dict.fromkeys(filesAdded)) #remove duplicates
        window["_FILE-ENCRYPT-LIST_"].update(values=filesAdded) #adding file paths to the visual list

    if event == "Encrypt":
        continue

    if event == "Decrypt":
        continue


window.close()