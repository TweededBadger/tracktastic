import sys
import os
import random
import string

def rm(filename):
    os.remove(filename)

def random_string(length=10):
    # return ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase + string.digits + string.punctuation) for _ in range(length))
    return ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase + string.digits) for _ in range(length))

def get_platform():
    if sys.platform.startswith("win"):
        return  'windows'
    elif sys.platform.startswith("linux"):
        return 'linux'
    else:
        raise ImportError("I don't support your system yet. Sorry!")