from functools import wraps
from flask import request, redirect, url_for, session
from views.fingerprint import fingerprint

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "id" not in session:
            return redirect(url_for("fingerprint.fingerprint_func"))
        return f(*args, **kwargs)
    return decorated_function

