from src.lib.dockerfiles import Indent

import glob
import os

PYTHON_PROJECT = "./python/**"

def main():

    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]

    with open(file_paths[10], mode="r") as f:
        data = f.readlines()
    for comp in data:
        if comp.startswith("\t\t\t\t"):
            print(4, comp)
        elif comp.startswith("\t\t\t"):
            print(3, comp)
        elif comp.startswith("\t\t"):
            print(2, comp)
        elif comp.startswith("\t"):
            print(1, comp)
        else:
            print(0, comp)

if __name__ == "__main__":
    main()