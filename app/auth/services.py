import hashlib

from werkzeug.security import generate_password_hash
from app.auth.models import User, add_user, get_user_by_email
from app.utils.exceptions import BusinessError
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import asyncio
import time
import random
from typing import Dict, Tuple
from app.utils.database_encryption import Config
import os
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import time
from app.auth.models import get_user_by_email
from app.utils.exceptions import BusinessError
import smtplib
from email.mime.text import MIMEText
import hmac

def generate_password_hash(password, salt=None):
    if salt is None:
        salt = os.urandom(4)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    password_hash = kdf.derive(password.encode())
    return password_hash.hex(), salt.hex()


def register_user(status, username, email, password):
    password_hash, salt = generate_password_hash(password)
    email_hash = hmac.new(
        key=Config.HMAC_KEY,
        msg=email.encode(),
        digestmod='sha256'
    ).hexdigest()
    name_hash = hmac.new(
        key=Config.HMAC_KEY,
        msg=username.encode(),
        digestmod='sha256'
    ).hexdigest()
    try:
        user = add_user(status=status, name=username, email=email, password_hash=password_hash, salt = salt, emailHash = email_hash, nameHash=name_hash)
    except Exception as e:
        raise BusinessError('Failed to register user: ' + str(e), 409)

    return user

def my_login_user(username, password):
    try:
        email_hash = hmac.new(
            key=Config.HMAC_KEY,
            msg=username.encode(),
            digestmod='sha256'
        ).hexdigest()
        user = get_user_by_email(emailHash=email_hash)
    except Exception as e:
        raise BusinessError('Failed to login user: ' + str(e), 500)
    if not user:
        raise BusinessError('Invalid username or password', 401)

    salt = bytes.fromhex(user.salt)
    password_hash = user.password

    hashed_password, salt = generate_password_hash(password, salt=salt)

    if password_hash == hashed_password:
        return user
    else:
        raise BusinessError('Invalid username or password', 401)

verification_store: Dict[str, dict] = {}

def my_get_hash(str):
    hash_value = hmac.new(
        key=Config.HMAC_KEY,
        msg=str.encode(),
        digestmod='sha256'
    ).hexdigest()
    return hash_value


async def send_email_async(email):
    user = get_user_by_email(my_get_hash(email))
    if not user:
        raise BusinessError("User not found", 404)

    code = str(random.randint(100000, 999999))


    from_name = user.name
    from_addr = "1534433057@qq.com"
    from_pwd = "oeisscrfcfukgccf"
    to_addr = user.email
    my_title = "Your Easy Booking Verification Code"
    my_msg = "Your Easy Booking verification code is:" + str(code)

    verification_store[email] = {
        "code": code,
        "timestamp": time.time(),
    }

    msg = MIMEText(my_msg, 'plain', 'utf-8')
    msg['From'] = formataddr([from_name, from_addr])
    msg['To'] = to_addr
    msg['Subject'] = my_title

    smtp_srv = "smtp.qq.com"

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, send_email_sync, smtp_srv, from_addr, from_pwd, to_addr, msg)
    except Exception as e:
        raise BusinessError(f"Failed to send email: {str(e)}", 500)


def send_email_sync(smtp_srv, from_addr, from_pwd, to_addr, msg):
    """Helper function to send email synchronously."""
    smtpobj = smtplib.SMTP_SSL(smtp_srv)
    smtpobj.connect(smtp_srv, 465)
    smtpobj.login(from_addr, from_pwd)
    smtpobj.sendmail(from_addr, to_addr, msg.as_string())


def verify_code(email, verification_code):
    record = verification_store.get(email)

    if not record:
        raise BusinessError("Get the code first", 401)
    if time.time() - record['timestamp'] > 300:
        del verification_store[email]
        raise BusinessError("The verification code has expired", 401)
    if record['code'] != verification_code:
        raise BusinessError("Invalid code", 401)
    del verification_store[email]
    return get_user_by_email(my_get_hash(email))