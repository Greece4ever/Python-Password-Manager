"""
    LOCAL MODULE FOR PASSWORD ENCRYPTION,
    USES PYTHON'S BUILTIN FUNCTIONS AS WELL AS THE SECRETS MODULE,
"""


import secrets 
from typing import Union
import getpass
from random import randint 

INTS = [2,3,4]

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

SWITCHCASE = {
    1:  bin(6943),
    2:  bin(9643),
    3:  bin(35431),
    4:  bin(32431),
    5:  bin(43143),
    6:  bin(2113),
    7:  bin(7612),
    8:  bin(20543),
    9:  bin(993),
}

def isNumber(__input__) -> bool:
    try:
        float(__input__)
        return True
    except:
        return False

def randomCase(string : str) -> str:
    STRING_ARRAY = []
    for letter in string:
        choices = [letter.upper(),letter.lower()]
        STRING_ARRAY.append(secrets.choice(choices))
    return "".join(STRING_ARRAY)

def encryptIterations(iterations : Union[str,int]) -> str:
    """
        Encrypts iterations given in the form of a string
    """
    iterations = str(iterations)
    STORAGE = []
    for item in iterations:
        STORAGE.append(SWITCHCASE.get(int(item)))

    return "".join(STORAGE)

def decryptIterations(iterations : Union[bytes,str]) -> str:
    """
        Decrypts encrypted iterations
    """
    iterations = str(iterations)
    BINARY_ITEMS = [SWITCHCASE[item] for item in SWITCHCASE]
    VALUES = [str(item) for item in SWITCHCASE]
    for __item__ in range(len(VALUES)):
        iterations = iterations.replace(BINARY_ITEMS[__item__],VALUES[__item__])

    return "".join(iterations)

def encrypt(msg : str) -> list:
    dec = []
    dec_length = []
    length = len(msg)
    hashes = []
    STORED = []
    ITERATIONS = []
    for j in range(length):
        int_choice = secrets.choice(INTS)
        # tmp = []
        # for i in range(randint(1,4)):
        #     sec = secrets.choice(alphabet)
        #     CHOICES = [sec.upper(),sec.lower()]
        #     c_1 = secrets.choice(CHOICES)
        #     tmp.append(c_1)
        # tmp = "".join(tmp)
        choice_token = randomCase(str(secrets.token_hex(int_choice)))
        hashes.append(f'{choice_token}')
        ITERATIONS.append(str(len(choice_token)))
        converted_char = str(ord(msg[j]))
        converted_char_len = len(converted_char)
        dec.append(converted_char)
        dec_length.append(str(converted_char_len) + '_')

    for i in range(length):
        STORED.append(f'{hashes[i]}{dec[i]}')


    iter_has = "".join(ITERATIONS)
    chars = "---".join(dec) 
    dashes = "---".join(hashes) 
    chars_length = "".join(dec_length)
    chars_length = chars_length[:len(chars_length)-1]
    
    tmp_cache = []
    for i in range(randint(1,15)):
        tak = secrets.choice(alphabet)
        tmp_cache.append(tak)
    tmp_cache = "".join(tmp_cache)

    return ["".join(STORED) + randomCase(tmp_cache),(iter_has,chars_length)]

def decrpyt(encrypted_msg : str,encrypted_iterations : str,charvar_length : str) -> str:
    iterations = decryptIterations(encrypted_iterations)
    LENGTH = len(iterations)
    charvar_length = charvar_length.replace('_','')
    NUMBERS = []

    for i in range(LENGTH):
        tmp_len = int(iterations[i])
        tmp_char_len = int(charvar_length[i])
        tmp1 = encrypted_msg[tmp_len:]  
        NUMBERS.append(tmp1[:tmp_char_len])
        encrypted_msg = tmp1[tmp_char_len:]

    decrypted = [chr(int(letter)) for letter in NUMBERS]

    return "".join(decrypted)


if __name__ == "__main__":
    x = encrypt("Terry Davis is the smartest programmer that has ever lived.")
    print(x)
    print("\n\n")
    print(encryptIterations(223456))
    print("\n\n")
    print(decrpyt(x[0],x[1][0],x[1][1]))