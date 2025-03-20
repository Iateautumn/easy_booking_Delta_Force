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
# from celery import Celery
import time
import random
from typing import Dict, Tuple
import os
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

    try:
        user = add_user(status, username, email, password_hash, salt)
    except Exception as e:
        raise BusinessError('Failed to register user: ' + str(e), 409)

    return user


def my_login_user(username, password):
    try:
        user = get_user_by_email(username)
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



# verification_store: Dict[str, dict] = {}



# def send_email_celery(email):
#     if not os.getenv('DJANGO_SETTINGS_MODULE'):
#         os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'
#     celery_app = Celery('booking_system')
#     @celery_app.task(bind=True, name='send_verify_email', retry_backoff=3)
#     def send_email_verification(email):
#         user = get_user_by_email(email)
#         code = str(random.randint(100000, 999999))
#         from_name = user.username
#         from_addr = "2543297@dundee.ac.uk"
#         from_pwd = "jjjjjjjjjj"
#         to_addr = user.email
#         my_title = "code verification"
#         my_msg = code
#         verification_store[email] = {
#             "code": code,
#             "timestamp": time.time(),
#         }
#         msg = MIMEText(my_msg, 'plain', 'utf-8')
#         msg['From'] = formataddr([from_name, from_addr])
#         msg['Subject'] = my_title

#         smtp_srv = "smtp.office365.com"

#         try:
#             srv = smtplib.SMTP_SSL(smtp_srv.encode(), 587)

#             srv.login(from_addr, from_pwd)

#             srv.sendmail(from_addr, [to_addr], msg.as_string())
#         except Exception as e:
#             raise BusinessError('send email failed', 401)
#         finally:
#             srv.quit()

#     celery_app.config_from_object('celery_tasks.config')
#     celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])
#     send_email_verification.delay(email)



# def verify_code(email, verification_code):
#     record = verification_store.get(email)

#     if not record:
#         raise BusinessError("get the code first", 401)
#     if time.time() - record['timestamp'] > 300:
#         del verification_store[email]
#         raise BusinessError("The verification code has expired", 401)
#     if record['code'] != verification_code:
#         return BusinessError("invalid code", 401)
#     del verification_store[email]
#     return get_user_by_email(email)

import asyncio
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import random
import time
from app.auth.models import get_user_by_email
from app.utils.exceptions import BusinessError

verification_store: Dict[str, dict] = {}


async def send_email_async(email):
    user = get_user_by_email(email)
    if not user:
        raise BusinessError("User not found", 404)

    code = str(random.randint(100000, 999999))
    from_name = user.name
    from_addr = "2543297@dundee.ac.uk"
    from_pwd = "jjjjjjjjjj"
    to_addr = user.email
    my_title = "Code Verification"
    my_msg = code

    verification_store[email] = {
        "code": code,
        "timestamp": time.time(),
    }

    msg = MIMEText(my_msg, 'plain', 'utf-8')
    msg['From'] = formataddr([from_name, from_addr])
    msg['To'] = to_addr
    msg['Subject'] = my_title

    smtp_srv = "smtp.office365.com"

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, send_email_sync, smtp_srv, from_addr, from_pwd, to_addr, msg)
        print('send!!!!!!!!!!!')
    except Exception as e:
        raise BusinessError(f"Failed to send email: {str(e)}", 500)


def send_email_sync(smtp_srv, from_addr, from_pwd, to_addr, msg):
    """Helper function to send email synchronously."""
    with smtplib.SMTP(smtp_srv, 587) as srv:
        srv.starttls()
        srv.login(from_addr, from_pwd)
        srv.sendmail(from_addr, [to_addr], msg.as_string())


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
    return get_user_by_email(email)