import os
#import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def substrings(a, b, n):
    """return substrings of length n"""
    #get a list of words in strings
    a_strip = a.strip(' ')
    b_strip = b.strip(' ')

    #initialize array for substrings of length n
    a_list = []
    b_list = []
    substringlist = []

    #populate arrays with all possible substrings and matching substrings between the 2 arrays
    for i in range(len(a_strip) -n + 1):
        a_list.append(a_strip[i:i+n])
    for j in range(len(b_strip) -n + 1):
        b_list.append(b_strip[j:j+n])

    for substring in a_list:
        if substring in b_list and substring not in substringlist:
            substringlist.append(substring)

    return substringlist


