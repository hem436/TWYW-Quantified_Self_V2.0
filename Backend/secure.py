import jwt
import uuid4 as uuid
from werkzeug.security import generate_password_hash as hpw, check_password_hash as cpw
from functools import wraps
