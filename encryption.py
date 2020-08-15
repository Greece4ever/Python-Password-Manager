from cryptography.fernet import Fernet
import base64

def descript(message : str) -> str:
    return base64.b32decode(message)


print(descript("HELLO WORLD"))