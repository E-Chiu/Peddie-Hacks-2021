from cryptography.fernet import Fernet

# TO USE: ADD TESTERFILES IF NEEDED
# THEN COMMENT OUT ENCRYPT/DECRYPT SECTION OR ELSE IT WILL CANCEL OUT OR ENCRYPT EVEN MORE

testerFiles = ['./encryptTestFolder/testApp.exe', './encryptTestFolder/testImage.jpg', './encryptTestFolder/testText.txt', './encryptTestFolder/testVideo.mp4']

# obtain key from file
with open('filekey.key', 'rb') as filekey:
    key = filekey.read()

# use key
fernet = Fernet(key)

####### Encrypt Section ######

# encrypt
for fileName in testerFiles:
    with open(fileName, 'rb') as file:
        toEncrypt = file.read()

    encrypted = fernet.encrypt(toEncrypt)

    # write back to file
    with open(fileName, 'wb') as file:
        file.write(encrypted)

###### Decrypt Section ######

""" # decrypt
for fileName in testerFiles:
    with open(fileName, 'rb') as file:
        toDecrypt = file.read()

    decrypted = fernet.decrypt(toDecrypt)

    # write back
    with open(fileName, 'wb') as file:
        file.write(decrypted) """