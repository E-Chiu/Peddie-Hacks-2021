from cryptography.fernet import Fernet
import pickle

# TO USE: ADD TESTERFILES IF NEEDED
# THEN COMMENT OUT ENCRYPT/DECRYPT SECTION OR ELSE IT WILL CANCEL OUT OR ENCRYPT EVEN MORE

####### Encrypt Section ######

def encrypt(profile, fernet):
    for fileName in profile:
        with open(fileName, 'rb') as file:
            toEncrypt = file.read()

        encrypted = fernet.encrypt(toEncrypt)

        # write back to file
        with open(fileName, 'wb') as file:
            file.write(encrypted)

###### Decrypt Section ######

def decrypt(profile, fernet):
    for fileName in profile:
        with open(fileName, 'rb') as file:
            toDecrypt = file.read()

        decrypted = fernet.decrypt(toDecrypt)

        # write back
        with open(fileName, 'wb') as file:
            file.write(decrypted)
 
def main():
    # obtain key from file
    with open('filekey.key', 'r') as filekey:
        key = filekey.read()
    # use key
    fernet = Fernet(key)

    currentProfile = []

    ###### Get files to encrypt/decrypt ######

    decrypt(['profile0.txt'], fernet)
    with open('profile0.txt', 'r') as readProfile:
        for line in readProfile:
            currentProfile.append(line.strip())

    with open('profile0.txt', 'w') as saveProfile:
        for file in currentProfile:
            saveProfile.write(file + "\n")
    encrypt(['profile0.txt'], fernet)

    encrypt(currentProfile, fernet)
    decrypt(currentProfile, fernet)

main()
