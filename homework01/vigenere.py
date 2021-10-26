from caesar import decrypt_caesar, encrypt_caesar


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.



    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key = keyword
    while len(key) < len(plaintext):
        key += keyword

    for i in range(0, len(plaintext)):
        if key[i].isupper():
            shift = ord(key[i]) - 65
        else:
            shift = ord(key[i]) - 97

        ciphertext += encrypt_caesar(plaintext[i], shift)
        ciphertext_ = ciphertext
    return ciphertext_


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key = keyword
    while len(key) < len(ciphertext):
        key += keyword

    for i in range(0, len(ciphertext)):
        if key[i].isupper():
            shift = ord(key[i]) - 65
        else:
            shift = ord(key[i]) - 97
        plaintext += decrypt_caesar(ciphertext[i], shift)
    return plaintext
