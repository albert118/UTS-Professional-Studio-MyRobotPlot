import os
from pathlib import Path


def normalise_filepath(fn):
    curr_dir = Path(os.path.dirname(__file__))
    par_dir = curr_dir.parent.absolute()
    norm_path = os.path.join(par_dir, fn)
    
    return norm_path
