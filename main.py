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
from src.lib.cluster import Dived
from src.lib.blocks import Hash
from src.lib.zlibs import Zlib

from gensim.models import word2vec

import datetime


PYTHON_PROJECT = "./python/**"
GOLANG_PROJECT = "./golang/**"
OTHERS = "./Others/**"


def create_model(data):
    model = word2vec.Word2Vec(
        data,
        size=10,
        window=5,
        iter=3
    )
    model.save("./Delivers/result.model")




def main():
    combinations = {}
    file_paths = []
    file_paths.extend([comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")])
    # file_paths.extend([comp for comp in glob.glob(GOLANG_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")])
    print(len(file_paths))
    results = {}
    query = ['apt-get', 'install', '-y', '--no-install-recommends']
    query = ["ln", "-s"]
    query = ["./configure"]
    query = ["mkdir", "-p"]
    query = ["set", "-ex"]
    query = ["find", "/usr/local", "-depth"]
    # hash_query = Hash.execute(query)
    # query = [cnt for cnt in hash_query]
    query = "".join(query)
    print(query)
    data = []
    maps = {}
    for file_path in file_paths:
        model = Model(file_path)
        shells = model.shells
        for shell in shells:
            shell_words = "".join(shell)
            if query in shell_words:
                print(shell)
            # shell_dict = Hash.execute(shell)
            # data.append([cnt for cnt in shell_dict])
            # for key, value in shell_dict.items():
            #     if not key in maps:
            #         maps[key] = value
    
    # for shell_hash in data:
    #     if query[-1] in shell_hash:
    #         shell = [maps[sh] for sh in shell_hash]
    #         print(shell)

            



            




if __name__ == "__main__":
    main()

