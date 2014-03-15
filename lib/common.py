import os

def add_postfix(filename, postfix):
    filepath, fileext = os.path.splitext(filename)
    return filepath + '.' + postfix + fileext
