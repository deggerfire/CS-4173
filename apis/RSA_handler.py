from Crypto.Cipher import PKCS1_OAEP
import base64
# Splits a string into length num chars (should be 344?)
def chunkstringE(string):
    return (string[0+i:200+i] for i in range(0, len(string), 200))

def chunkstringD(string):
    return (string[0+i:344+i] for i in range(0, len(string), 344))

def encode(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    eMessage = ""
    for chunk in chunkstringE(message):
        eMessage += base64.b64encode(cipher.encrypt(chunk)).decode("utf-8")
    return eMessage

def decode(message, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    dMessage = ""
    for chunk in chunkstringD(message):
        dMessage += cipher.decrypt(base64.b64decode((chunk.encode("utf-8")))).decode("utf-8")
    return dMessage