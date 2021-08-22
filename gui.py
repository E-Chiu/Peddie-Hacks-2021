import PySimpleGUI as sg
import backend as crypt
from cryptography.fernet import Fernet
from os import listdir, path
from os.path import isfile, join

sg.SetOptions(background_color='#000',
    text_element_background_color='#9FB8AD',
    element_background_color='#9FB8AD',
    scrollbar_color=None,
    input_elements_background_color='#FFF',
    button_color=('black','#FFF'))


# mypath = "./profiles/"
#         onlyfiles = [i for i in listdir(mypath) if isfile(join(mypath, i))]
#         print(onlyfiles)


encryptColumn = [
    [sg.In(size=(32,1), key="_NEW-PROF-IN_", enable_events=True), sg.Button("Add New Profile", key="_NEW-PROF_", size=(15,1))], # create new profile
    [sg.Combo([path.splitext(i)[0] for i in listdir("./profiles/") if isfile(join("./profiles/", i))], size=(30,1), key="_PROFILES_", enable_events=True), sg.Button("Remove Current Profile", key="_REMOVE-PROF_", size=(20,1))], # choose profile
    [sg.In(size=(70,1), key="_FILES_", enable_events=True), sg.FilesBrowse("Add Files", target="_FILES_")], # browse files to encrypt
    [sg.Submit("Add")], # adds chosen files to profile
    [sg.Listbox(values=[], enable_events=True, size=(70, 10), key="_FILE-ENCRYPT-LIST_")], # files in the profile
    [sg.Submit("Encrypt"), sg.Submit("Decrypt")] # encrypt or decrypt files in profile
]

#window format
layout = [
        [sg.Column(encryptColumn, justification="center")]
    ]


window = sg.Window(title="File Encryptor", layout=layout, margins=(10, 50), location=(0,0), size=(1150, 600)) #window properties

filesAdded = []

# obtain key from file
with open('filekey.key', 'r') as filekey:
    key = filekey.read()
with open('identifier.key', 'rb') as identifierkey:
    identifier = identifierkey.read()
# use key
fernet = Fernet(key)

while True:
    event, values = window.read()

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
        try:
            crypt.del_Profile(fernet, identifier, values["_PROFILES_"])
            window["_PROFILES_"].update(values=[path.splitext(i)[0] for i in listdir("./profiles/") if isfile(join("./profiles/", i))])
        except:
            window["_PROFILES_"]("Profile not selected")


    if event == "Add":
        crypt.mark_Add(fernet, identifier, values["_PROFILES_"], values['_FILES_'].split(';'))
        print(crypt.get_Profile("./profiles/" + values["_PROFILES_"] + ".profile", fernet, identifier))
        #window["_FILE-ENCRYPT-LIST_"].update(values=filesAdded) #adding file paths to the visual list

        # filesAdded += values['_FILES_'].split(';') #adding new file paths
        # filesAdded = list(dict.fromkeys(filesAdded)) #remove duplicates
        # window["_FILE-ENCRYPT-LIST_"].update(values=filesAdded) #adding file paths to the visual list

    if event == "Encrypt":
        continue

    if event == "Decrypt":
        continue


window.close()