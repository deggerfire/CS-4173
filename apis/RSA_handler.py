from Crypto.Cipher import PKCS1_OAEP
import base64

# Splits a string into chunks of size 200 for encodeing, number picked at sudo random
def chunkstringE(string):
    return (string[0+i:200+i] for i in range(0, len(string), 200))

# Splits a string into chunks of size 344 for decoding !DON'T CHANGE THIS NUMBER!
def chunkstringD(string):
    return (string[0+i:344+i] for i in range(0, len(string), 344))

# Uses RSA to encode a message of any size
def encode(message, public_key):
    # Make the cipher
    cipher = PKCS1_OAEP.new(public_key)
    # Make a blank string to hold the message
    eMessage = ""
    # Split the sting into chuncks
    for chunk in chunkstringE(message):
        # Encode each chunk and append it to the message
        eMessage += base64.b64encode(cipher.encrypt(chunk)).decode("utf-8")
    return eMessage

# Uses RSA to decode a message of any size
def decode(message, private_key):
    # Make the cipher
    cipher = PKCS1_OAEP.new(private_key)
    # Make a blank string to hold the message
    dMessage = ""
    # Split the sting into chuncks
    for chunk in chunkstringD(message):
        # Decode each chunk and append it to the message
        dMessage += cipher.decrypt(base64.b64decode((chunk.encode("utf-8")))).decode("utf-8")
    return dMessage