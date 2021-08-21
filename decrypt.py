from cryptography.fernet import Fernet

filePath = 'profile0.txt'

# obtain key from file
with open('filekey.key', 'r') as filekey:
    key = filekey.read()
with open('identifier.key', 'rb') as identifierkey:
    identifier = identifierkey.read()

# use key
fernet = Fernet(key)

with open(filePath, 'rb') as file:
    toDecrypt = file.read()
toDecrypt = toDecrypt.replace(identifier, b'') # remove identifier
decrypted = fernet.decrypt(toDecrypt)

# write back to file
with open(filePath, 'wb') as file:
    file.write(decrypted)