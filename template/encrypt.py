import hashlib

def ecpt(message):
    hash_object = hashlib.sha256(message.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig
