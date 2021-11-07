import glob
import os
import pprint

import pyfpgrowth
import pprint

from collections import Counter
import itertools

from prefixspan import PrefixSpan

from src.lib.dockerfiles import Dockerfile
from src.lib.nlps import NLP




PYTHON_PROJECT = "./python/**"
OTHERS = "./Others/**"

def main():
    combinations = {}
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    words = []
    targets = []
    for file_path in file_paths:
        print()
        print()
        print()
        print(file_path)
        dock = Dockerfile(file_path)
        contents = dock.get_shell_2()
        for content in contents:
            # print()
            for comp in content:
                # print(comp)
                pass





if __name__ == "__main__":
    main()

# ps = PrefixSpan(contents)

    # for comp in ps.topk(100):
    #     print(comp)