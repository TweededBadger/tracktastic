import os
import random
import string

def rm(filename):
    os.remove(filename)

def random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase + string.digits + string.punctuation) for _ in range(length))