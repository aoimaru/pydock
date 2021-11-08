import glob
import os
import pprint

import pyfpgrowth
import pprint

from collections import Counter
import itertools

from prefixspan import PrefixSpan

from src.lib.dockerfiles import Dockerfile, Model
from src.lib.nlps import NLP
from src.lib.words import Token




PYTHON_PROJECT = "./python/**"
OTHERS = "./Others/**"

def norm(token):
    if token.startswith('"'):
        token = token[1:]
    if token.endswith('"'):
        token = token[:-1]
    if token.startswith("'"):
        token = token[1:]
    if token.endswith("'"):
        token = token[:-1]
    return token

def main():
    combinations = {}
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    words = []
    for file_path in file_paths:
        model = Model(file_path)
        shells = model.shells

        for shell in shells:
            print(shell)

        # for run in runs:
        #     print()
        #     for shells in run:
        #         shells = [shell for shell in shells if shell != "SPACE"]
        #         shells = [shell.replace("(", "") for shell in shells]
        #         shells = [shell.replace("(", "") for shell in shells]
        #         shells = [shell.replace(")", "") for shell in shells]
        #         shells = [shell.replace(")", "") for shell in shells]
        #         shells = [shell.replace("[", "") for shell in shells]
        #         shells = [shell.replace("[", "") for shell in shells]
        #         shells = [shell.replace("]", "") for shell in shells]
        #         shells = [shell.replace("]", "") for shell in shells]

        #         shells = [shell.replace("\\n", "BACKNT") for shell in shells]

        #         shells = [norm(shell) for shell in shells]
        #         print(shells)
                # print(kinds)
    # file_path = "./python/3.10/bullseye/slim/Dockerfile"
    # dock = Dockerfile(file_path)
    # contents = dock.get_shell()
    # for content in contents:
    #     print(content)
    #     for comps in content:
    #         kinds = []
    #         if type(comps) is list:
    #             print()
    #             print("===============================")
                
    #             print("comps", comps)
    #             for comp in comps:
    #                 token = Token(comp)
    #                 print("original", token.original)
    #                 # print("extentions", token.extentions)
    #                 # print("kinds", token.kinds)
    #                 # print("subs", token.subs)
    #                 kinds.append(token.kinds)
    #             print("kinds", kinds)
    #             print("===============================")
    #             print()



if __name__ == "__main__":
    main()

# ps = PrefixSpan(contents)

    # for comp in ps.topk(100):
    #     print(comp)