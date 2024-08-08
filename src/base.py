import pickle
from pathlib import Path

def SaveObjects(path : Path, object):
    pickle.dump(object, open(path,'wb'))
