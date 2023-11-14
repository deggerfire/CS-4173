from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Does not work here would need to be move into user/host_room
def makeKey(password):
    # Use PBKDF2HMAC to make a key from the room password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), # Using SHA256 algorithm
        length=32, # Needs to be of length 32 to be a key
        salt=b"", # Super secure salt, just for early version
        iterations=480000, # Recomended number of iterations
    )
    print(kdf)

    # Make and return the key
    return base64.urlsafe_b64encode(kdf.derive(password))