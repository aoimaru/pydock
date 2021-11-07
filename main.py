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
from src.lib.words import Token




PYTHON_PROJECT = "./python/**"
OTHERS = "./Others/**"

def main():
    combinations = {}
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    words = []
    file_path = "./python/3.10/bullseye/slim/Dockerfile"
    dock = Dockerfile(file_path)
    contents = dock.get_shell_2()
    for content in contents:
        for comps in content:
            print()
            print("===============================")
            print("comps", comps)
            for comp in comps:
                token = Token(comp)
                if len(token.original) > 1:
                    print()
                    print("original", token.original)
                    print("extentions", token.extentions)
                    print("kinds", token.kinds)
                    print("subs", token.subs)
            print("===============================")
            print()



if __name__ == "__main__":
    main()

# ps = PrefixSpan(contents)

    # for comp in ps.topk(100):
    #     print(comp)