from cryptography.fernet import Fernet
import codecs
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def passwort_to_key(password, salt):
    password = password.encode('UTF-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()
    f = Fernet(key)
    encrypted_text = f.encrypt(plaintext)
    print(encrypted_text)
    with open(file_path + '.encrypted', 'wb') as file:
        file.write(encrypted_text)


def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_text = file.read()

    f = Fernet(key)
    decrypted_text = f.decrypt(encrypted_text)

    with open(file_path[:-10]+".decrypted", 'wb') as file:
        file.write(decrypted_text)


# Example usage
file_path = 'original.txt'  # This is the lost file

# Reading salt from environment variable.
salt = os.environ["SALT"];
# verysecretpassword should be found out
key = passwort_to_key("verysecretpassword", salt)

# Encrypt the file
encrypt_file(file_path, key)

# Decrypt the file
# decrypt_file(file_path + '.encrypted', key)
