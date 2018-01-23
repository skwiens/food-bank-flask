from flask import flash, session, url_for, redirect
from functools import wraps

def user_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Please log in to see this page', 'danger')
            return redirect(url_for('user_login'))
    return wrap

def admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session and session['user']=='admin':
            return f(*args, **kwargs)
        else:
            flash('You must have admin privileges to complete this action', 'danger')
            return redirect(url_for('index'))
    return wrap
