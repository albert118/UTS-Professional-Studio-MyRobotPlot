import os

def normalise_filepath(fn):
    return os.path.join(os.path.dirname(__file__), fn)