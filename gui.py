import PySimpleGUI as sg
import os.path

sg.SetOptions(background_color='#000',
    text_element_background_color='#9FB8AD',
    element_background_color='#9FB8AD',
    scrollbar_color=None,
    input_elements_background_color='#FFF',
    button_color=('black','#FFF'))

encryptColumn = [
    [sg.In(size=(70,1), key="_FILES_"), sg.FilesBrowse("Add Files", target="_FILES_")], #values returns the path to files
    [sg.Submit("Add")],
    [sg.Listbox(values=[], enable_events=True, size=(70, 10), key="_FILE-ENCRYPT-LIST_")],
    [sg.Submit("Encrypt")]
]

decryptColumn = [
    [sg.Listbox(values=[], enable_events=True, size=(70, 10), key="_FILE-DECRYPT-LIST_")],
    [sg.Submit("Decrypt")]
]

#window format
layout = [
        [sg.Column(encryptColumn), sg.VSeperator(), sg.Column(decryptColumn)]
    ]


window = sg.Window(title="File Encryptor", layout=layout, margins=(10, 50), location=(0,0), size=(1150, 600)) #window properties


filesAdded = []
filesEncrypted = []
while True:
    event, values = window.read()

    if event == "Add":
        filesAdded += values['_FILES_'].split(';') #adding new file paths
        filesAdded = list(dict.fromkeys(filesAdded)) #remove duplicates
        window["_FILE-ENCRYPT-LIST_"].update(values=filesAdded) #adding file paths to the visual list

    if event == sg.WIN_CLOSED:
        break

    if event == "Encrypt":
        filesEncrypted += filesAdded
        filesEncrypted = list(dict.fromkeys(filesEncrypted)) #remove duplicates
        filesAdded = []
        window["_FILE-DECRYPT-LIST_"].update(values=filesEncrypted)
        window["_FILE-ENCRYPT-LIST_"].update(values=[])

window.close()