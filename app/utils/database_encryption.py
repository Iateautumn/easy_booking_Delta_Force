import json
import os
from cryptography.fernet import Fernet
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy import String
from cryptography.fernet import Fernet
from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine


# class Config:

#     KEY_FILE = "./encryption_key.txt"
#     if os.path.exists(KEY_FILE):
#         with open(KEY_FILE,"r") as f:
#             ENCRYPTION_KEY = f.read().strip()
#     else:
#         ENCRYPTION_KEY = Fernet.generate_key().decode()
#
#         with open(KEY_FILE,"w") as f:
#             f.write(ENCRYPTION_KEY)


class Config:

    KEY_FILE = "./encryption_key.json"

    if os.path.exists(KEY_FILE):

        with open(KEY_FILE, "r") as f:
            data = json.load(f)
            ENCRYPTION_KEY = data.get("ENCRYPTION_KEY", "").strip().encode()
            HMAC_KEY = data.get("HMAC_KEY", "").strip()
            HMAC_KEY = bytes.fromhex(HMAC_KEY)
    else:

        ENCRYPTION_KEY = Fernet.generate_key()

        HMAC_KEY = os.urandom(32)


        with open(KEY_FILE, "w") as f:
            json.dump({
                "ENCRYPTION_KEY": ENCRYPTION_KEY.decode(),
                "HMAC_KEY": HMAC_KEY.hex()
            }, f)

print(Config.ENCRYPTION_KEY,Config.HMAC_KEY)
# extensions.py
def create_encrypted_string(length):
    return StringEncryptedType(type_in=String(length),key=Config.ENCRYPTION_KEY, engine=FernetEngine)
