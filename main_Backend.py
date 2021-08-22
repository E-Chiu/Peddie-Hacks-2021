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

def get_Profile(profile):
    currentProfile = []
    with open(profile, 'r') as readProfile:
        for line in readProfile:
            currentProfile.append(line.strip()) # add filenames to list and return
    return currentProfile

def set_Profile(profile, currentProfile, fernet, identifier):
    with open(profile, 'w') as saveProfile:
        for file in currentProfile:
            saveProfile.write(file + "\n")
    encrypt(profile, fernet, identifier)

def mark_Add(fernet, identifier):
    profile = './profiles/' + input('choose profile name: ') + '.profile'
    try:
        decrypt(profile, fernet, identifier) # decrypt profile first, if dne will be caught        
        currentProfile = get_Profile(profile) # get filenames
        filename = ''
        while True:
            print('Current filepaths: ' + ', '.join(currentProfile))
            filename = input('enter a filepath or "stop": ')
            if os.path.exists(filename) and filename not in currentProfile:
                currentProfile.append(filename) # add to list if exists
                print("File has been marked")
            else:
                filename = filename.lower()
                if filename != 'stop': # check to see if it is exit statement
                    print('Error: File does not exist')
                else:
                    break
        set_Profile(profile, currentProfile, fernet, identifier)
    except:
        print("Profile does not exist")

def mark_Del(fernet, identifier):
    profile = './profiles/' + input('choose profile name: ') + '.profile'
    try:
        decrypt(profile, fernet, identifier) # decrypt profile first, if dne will be caught
        currentProfile = get_Profile(profile) # get filepaths
        filepath = ''
        while True:
            print('Current filepaths: ' + ', '.join(currentProfile))
            filepath = input('Enter a filepath or "stop": ')
            if filepath in currentProfile:
                # check first if marked file has been encoded
                with open(filepath, 'rb') as f:
                    if f.readline().startswith(identifier): # if the identifier is at the front of the file decode it
                        decrypt(filepath, fernet, identifier)
                        print("Encoded file has been decoded first")
                currentProfile.remove(filepath)
                print("File has been unmarked")
            else:
                filepath = filepath.lower()
                if filepath != 'stop': # check to see if it is exit statement
                    print('Error: File is not in current profile')
                else:
                    break
        set_Profile(profile, currentProfile, fernet, identifier)
    except:
        print('Profile does not exist')

def mark_Toggle(fernet, identifier):
    profile = './profiles/' + input('choose profile name: ') + '.profile'
    try: # try to encrypt/decrypt files
        decrypt(profile, fernet, identifier) # decrypt profile first, if dne will be caught
        currentProfile = get_Profile(profile) # decrypt profile first, if dne will be caught
        for file in currentProfile:
            with open(file, 'rb') as f:
                if f.readline().startswith(identifier): # if the identifier is at the front of the file decode it
                    decrypt(file, fernet, identifier)
                else: # otherwise encode it
                    encrypt(file, fernet, identifier)
        encrypt(profile, fernet, identifier) # encode profile again
        print("Files have been encrypted/decrypted")
    except:
        print('Error: Profile does not exist')

def add_Profile(fernet, identifier):
    profile = './profiles/' + input('Choose name for new profile: ') + '.profile'
    try:
        open(profile, 'x')
        encrypt(profile, fernet, identifier) # encrypt new profile
        print('New Profile has been made')
    except:
        print('Profile name already exists')

def del_Profile(fernet, identifier):
    profile = './profiles/' + input('Choose name to delete: ') + '.profile'
    if os.path.exists(profile):
        decrypt(profile, fernet, identifier)
        currentProfile = get_Profile(profile)
        for file in currentProfile:
            with open(file, 'rb') as f:
                if f.readline().startswith(identifier): # check if need to decode anything
                    decrypt(file, fernet, identifier)
        os.remove(profile)
        print("Profile has been deleted")
    else:
        print("Profile does not exist")

def cleanup(fernet, identifier):
    profiles = [f for f in os.listdir('./profiles') if os.path.isfile(os.path.join('./profiles', f))]
    for profile in profiles: # make sure profiles are encrypted
        profile = './profiles/' + profile # make correct filepath
        with open(profile, 'rb') as f:
                if not f.readline().startswith(identifier):
                    encrypt(profile, fernet, identifier)

def main():
    # obtain key from file
    with open('filekey.key', 'r') as filekey:
        key = filekey.read()
    with open('identifier.key', 'rb') as identifierkey:
        identifier = identifierkey.read()
    # use key
    fernet = Fernet(key)
    
    cleanup(fernet, identifier) # make sure profiles are encrypted on close

    action = ''
    while action != 'quit':
        action = input('Enter an action ((A)dd, (D)elete, (T)oggle, (S)tart profile, (R)emove profile, quit): ').lower()
        if action == 'a':
            mark_Add(fernet, identifier)
        elif action == 'd':
            mark_Del(fernet, identifier)
        elif action == 't':
            mark_Toggle(fernet, identifier)
        elif action == 's':
            add_Profile(fernet, identifier)
        elif action == 'r':
            del_Profile(fernet, identifier)
        elif action != 'quit':
            print('option not chosen')
    
    cleanup(fernet, identifier)

main()
