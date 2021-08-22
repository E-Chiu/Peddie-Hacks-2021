import PySimpleGUI as sg
import backend as crypt
from cryptography.fernet import Fernet
from os import listdir, path
from os.path import isfile, join

# obtain key from file
with open('filekey.key', 'r') as filekey:
    key = filekey.read()
with open('identifier.key', 'rb') as identifierkey:
    identifier = identifierkey.read()
# use key
fernet = Fernet(key)

crypt.cleanup(fernet, identifier)

sg.SetOptions(background_color='#000',
    text_element_background_color='#9FB8AD',
    element_background_color='#9FB8AD',
    scrollbar_color=None,
    input_elements_background_color='#FFF',
    button_color=('black','#FFF'))


encryptColumn = [
    [sg.In(size=(32,1), key="_NEW-PROF-IN_", enable_events=True), sg.Button("Add New Profile", key="_NEW-PROF_", size=(15,1))], # create new profile
    [sg.Combo([path.splitext(i)[0] for i in listdir("./profiles/") if isfile(join("./profiles/", i))], size=(30,1), key="_PROFILES_", enable_events=True), sg.Button("Remove Current Profile", key="_REMOVE-PROF_", size=(20,1))], # choose profile
    [sg.In(size=(70,1), key="_FILES_", enable_events=True), sg.FilesBrowse("Browse Files", target="_FILES_")], # browse files to encrypt
    [sg.Submit("Add")], # adds or removeschosen files to profile
    [sg.Listbox(values=[], enable_events=True, size=(70, 10), key="_FILE-ENCRYPT-LIST_")], # files in the profile
    [sg.Submit("Encrypt"), sg.Submit("Decrypt"), sg.Submit("Remove Selected")] # encrypt or decrypt files in profile. remove selected
]

#window format
layout = [
        [sg.Column(encryptColumn, justification="center")]
    ]


window = sg.Window(title="File Encryptor", layout=layout, margins=(10, 50), location=(0,0), size=(1150, 600)) #window properties


while True:

    event, values = window.read()

    if not values["_PROFILES_"] == "":
        window["_FILE-ENCRYPT-LIST_"].update(values=crypt.get_Profile("./profiles/" + values["_PROFILES_"] + ".profile", fernet, identifier))

    if values["_PROFILES_"] == "":
        window["_FILE-ENCRYPT-LIST_"].update(values=[])


    if event == sg.WIN_CLOSED:
        break

    if len(values["_NEW-PROF-IN_"]) >= 30: # maximum character limit is 30 for files
        window["_NEW-PROF-IN_"].update(values["_NEW-PROF-IN_"][:-1])

    if event == "_NEW-PROF_":
        try:
            if len(values["_NEW-PROF-IN_"].strip()) > 0:
                crypt.add_Profile(fernet, identifier, values["_NEW-PROF-IN_"].strip()) # creates a profile
                window["_NEW-PROF-IN_"]("")
                window["_PROFILES_"].update(values=[path.splitext(i)[0] for i in listdir("./profiles/") if isfile(join("./profiles/", i))])
        except:
            window["_NEW-PROF-IN_"]("File already exists")

    if event == "_REMOVE-PROF_":
        crypt.del_Profile(fernet, identifier, values["_PROFILES_"])
        window["_PROFILES_"].update(values=[path.splitext(i)[0] for i in listdir("./profiles/") if isfile(join("./profiles/", i))])


    if event == "Add":
        crypt.mark_Add(fernet, identifier, values["_PROFILES_"], values['_FILES_'].split(';'))
        window["_FILE-ENCRYPT-LIST_"].update(values=crypt.get_Profile("./profiles/" + values["_PROFILES_"] + ".profile", fernet, identifier)) #adding file paths to the visual list

    if event == "Remove Selected":
        print(values["_FILE-ENCRYPT-LIST_"])

    if event == "Encrypt":
        crypt.encrypt_Set(fernet, identifier, values["_PROFILES_"])

    if event == "Decrypt":
        crypt.decrypt_Set(fernet, identifier, values["_PROFILES_"])


window.close()
crypt.cleanup(fernet, identifier)