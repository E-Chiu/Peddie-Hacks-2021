from cryptography.fernet import Fernet
import os

####### Encrypt Section ######

def encrypt(filePath, fernet, identifier):

    with open(filePath, 'rb') as file:
        toEncrypt = file.read()

    encrypted = fernet.encrypt(toEncrypt)
    # write back to file
    with open(filePath, 'wb') as file:
        file.write(identifier) # add identifier to front
        file.write(encrypted)

###### Decrypt Section ######

def decrypt(filePath, fernet, identifier):
    with open(filePath, 'rb') as file:
        toDecrypt = file.read()
    toDecrypt = toDecrypt.replace(identifier, b'') # remove identifier
    decrypted = fernet.decrypt(toDecrypt)

    # write back to file
    with open(filePath, 'wb') as file:
        file.write(decrypted)

def get_Profile(profile, fernet, identifier):
    currentProfile = []
    decrypt(profile, fernet, identifier)
    with open(profile, 'r') as readProfile:
        for line in readProfile:
            currentProfile.append(line.strip()) # add filenames to list and return
    encrypt(profile, fernet, identifier)
    return currentProfile

def set_Profile(profile, currentProfile, fernet, identifier):
    decrypt(profile, fernet, identifier)
    with open(profile, 'w') as saveProfile:
        for file in currentProfile:
            saveProfile.write(file + "\n")
    encrypt(profile, fernet, identifier)

def mark_Add(fernet, identifier, name, fileList):
    profile = './profiles/' + name + '.profile'
     
    currentProfile = get_Profile(profile, fernet, identifier) # get filenames
    for filename in fileList:
        if os.path.exists(filename) and filename not in currentProfile:
            currentProfile.append(filename) # add to list if exists
    set_Profile(profile, currentProfile, fernet, identifier)


def mark_Del(fernet, identifier, name, filepath):
    profile = './profiles/' + name + '.profile'
    try:
        currentProfile = get_Profile(profile, fernet, identifier) # get filepaths
        if filepath in currentProfile:
            # check first if marked file has been encoded
            with open(filepath, 'rb') as f:
                if f.readline().startswith(identifier): # if the identifier is at the front of the file decode it
                    decrypt(filepath, fernet, identifier)
            currentProfile.remove(filepath)
        set_Profile(profile, currentProfile, fernet, identifier)
    except:
        pass

def encrypt_Set(fernet, identifier, name):
    profile = './profiles/' + name + '.profile'
    try: # try to encrypt/decrypt files
        currentProfile = get_Profile(profile, fernet, identifier) # decrypt profile first, if dne will be caught
        for file in currentProfile:
            with open(file, 'rb') as f:
                if not f.readline().startswith(identifier):
                    encrypt(file, fernet, identifier)
    except:
        pass

def decrypt_Set(fernet, identifier, name):
    profile = './profiles/' + name + '.profile'
    try: # try to encrypt/decrypt files
        currentProfile = get_Profile(profile, fernet, identifier) 
        for file in currentProfile:
            with open(file, 'rb') as f:
                if f.readline().startswith(identifier):
                    decrypt(file, fernet, identifier)
    except:
        pass

def mark_Toggle(fernet, identifier, name):
    encrypt_Set(fernet, identifier, name)
    decrypt_Set(fernet, identifier, name)

def add_Profile(fernet, identifier, name):
    profile = './profiles/' + name + '.profile'
    open(profile, 'x')
    encrypt(profile, fernet, identifier) # encrypt new profile

def del_Profile(fernet, identifier, name):
    profile = './profiles/' + name + '.profile'
    if os.path.exists(profile):
        currentProfile = get_Profile(profile, fernet, identifier)
        for file in currentProfile:
            with open(file, 'rb') as f:
                if f.readline().startswith(identifier): # check if need to decode anything
                    decrypt(file, fernet, identifier)
        os.remove(profile)

def cleanup(fernet, identifier):
    profiles = [f for f in os.listdir('./profiles') if os.path.isfile(os.path.join('./profiles', f))]
    for profile in profiles: # make sure profiles are encrypted
        profile = './profiles/' + profile # make correct filepath
        with open(profile, 'rb') as f:
                if not f.readline().startswith(identifier):
                    encrypt(profile, fernet, identifier)