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
    profile = 'profile' + input('choose profile number: ') + '.txt'
    try:
        decrypt(profile, fernet, identifier) # decrypt profile first, if dne will be caught
    except:
        # if there is exception then new profile should be made
        open(profile, 'x')
        print('New Profile has been made')
    currentProfile = get_Profile(profile) # get filenames
    filename = ''
    while True:
        print('Current filepaths: ' + ', '.join(currentProfile))
        filename = input('enter a filepath or "stop": ')
        if os.path.exists(filename):
            currentProfile.append(filename) # add to list if exists
            print("File has been marked")
        else:
            filename = filename.lower()
            if filename != 'stop': # check to see if it is exit statement
                print('Error: File does not exist')
            else:
                break
    set_Profile(profile, currentProfile, fernet, identifier)

def mark_Del(fernet, identifier):
    option = input('delete (P)rofile or (F)ile?: ').lower()
    if option == 'p':
        profile = 'profile' + input('choose profile number: ') + '.txt'
        if os.path.exists(profile):
            os.remove(profile)
            print("Profile Deleted")
        else:
            print("Profile does not exist")
    elif option == 'f':
        profile = 'profile' + input('choose profile number: ') + '.txt'
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
    else:
        print("Option not chosen")

def mark_Toggle(fernet, identifier):
    profile = 'profile' + input('choose profile number: ') + '.txt'
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


def main():
    # obtain key from file
    with open('filekey.key', 'r') as filekey:
        key = filekey.read()
    with open('identifier.key', 'rb') as identifierkey:
        identifier = identifierkey.read()

    # use key
    fernet = Fernet(key)
    
    action = ''
    while action != 'quit':
        action = input('Enter an action ((A)dd, (D)elete, (T)oggle, quit): ').lower()
        if action == 'a':
            mark_Add(fernet, identifier)
        elif action == 'd':
            mark_Del(fernet, identifier)
        elif action == 't':
            mark_Toggle(fernet, identifier)
main()
