import uuid

with open('identifier.key', 'w') as f:
    key = str(uuid.uuid4())[:12]
    f.write(key)