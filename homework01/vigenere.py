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
            shift = ord(key[i]) - ord("A")
        else:
            shift = ord(key[i]) - ord("a")

        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                if ord(plaintext[i]) + shift % (ord("Z") - ord("A") + 1) > ord("Z"):
                    ciphertext += chr(
                        ord(plaintext[i])
                        + shift % (ord("Z") - ord("A") + 1)
                        - (ord("Z") - ord("A") + 1)
                    )
                else:
                    ciphertext += chr(ord(plaintext[i]) + shift % (ord("Z") - ord("A") + 1))
            elif plaintext[i].islower():
                if ord(plaintext[i]) + shift % (ord("z") - ord("a") + 1) > ord("z"):
                    ciphertext += chr(
                        ord(plaintext[i])
                        + shift % (ord("z") - ord("a") + 1)
                        - (ord("Z") - ord("A") + 1)
                    )

                else:
                    ciphertext += chr(ord(plaintext[i]) + shift % (ord("z") - ord("a") + 1))
        else:
            ciphertext += plaintext[i]

    return ciphertext


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
            shift = ord(key[i]) - ord("A")
        else:
            shift = ord(key[i]) - ord("a")

        if ciphertext[i].isalpha():
            if ciphertext[i].isupper():
                if ord(ciphertext[i]) - shift % (ord("Z") - ord("A") + 1) < ord("A"):
                    plaintext += chr(
                        ord(ciphertext[i])
                        - shift % (ord("Z") - ord("A") + 1)
                        + (ord("Z") - ord("A") + 1)
                    )

                else:
                    plaintext += chr(ord(ciphertext[i]) - shift % (ord("Z") - ord("A") + 1))
            elif ciphertext[i].islower():
                if ord(ciphertext[i]) - shift % (ord("z") - ord("a") + 1) < ord("a"):
                    plaintext += chr(
                        ord(ciphertext[i])
                        - shift % (ord("z") - ord("a") + 1)
                        + (ord("z") - ord("a") + 1)
                    )

                else:
                    plaintext += chr(ord(ciphertext[i]) - shift % (ord("z") - ord("a") + 1))
        else:
            plaintext += ciphertext[i]

    return plaintext
