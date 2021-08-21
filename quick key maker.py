import uuid

with open('identifier.key', 'wb') as f:
    key = str(uuid.uuid4())[:12]
    key = str.encode(key)
    f.write(key)

""" from cryptography.fernet import Fernet

key = Fernet.generate_key()
  
# string the key in a file
with open('filekey.key', 'wb') as filekey:
   filekey.write(key) """