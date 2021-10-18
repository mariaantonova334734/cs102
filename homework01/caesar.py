
import typing as tp

def encrypt_caesar(plaintext: str, shift: int = 3) -> str:

    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if i.isalpha():
            if i.isupper():
                if ord(i) + shift % 26 > 90:                   
                    ciphertext += chr(ord(i)+shift%26-26)
                else:
                    ciphertext += chr(ord(i) + shift % 26)
            elif i.islower():
                if ord(i) + shift % 26 > 122:
                    ciphertext += chr(ord(i) + shift % 26 - 26)
                else:
                    ciphertext += chr(ord(i) + shift % 26)               
        else:
            ciphertext += i
                
    return ciphertext



def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
"""
Decrypts a ciphertext using a Caesar cipher.


    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if i.isalpha():
            if i.isupper():
                if ord(i) - shift % 26 < 65:                    
                    plaintext += chr(ord(i) - shift % 26 + 26)
                else:
                    plaintext += chr(ord(i) - shift % 26)
            elif i.islower():
                if ord(i) - shift % 26 < 97:
                    plaintext += chr(ord(i) - shift % 26 + 26)
                else:
                    plaintext += chr(ord(i) - shift % 26)                
        else:
            plaintext += i
    return plaintext



def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
"""
Brute force breaking a Caesar cipher.
"""
best_shift = 0
# PUT YOUR CODE HERE
return best_shift

