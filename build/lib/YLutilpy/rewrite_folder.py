import shutil
import os

def rewrite_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
