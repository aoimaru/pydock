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
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]

    data = []
    for file_path in file_paths:
        model = Model(file_path)
        shells = model.shells

        for shell in shells:
            print()
            print(shell)
            # hash_words = Hash.execute(shell)
            # data.append([cnt for cnt in hash_words])
            # for key, value in hash_words.items():
            #     print(key, value)
            # kinds = [Token(word).kinds for word in shell]

    # create_model(data)




if __name__ == "__main__":
    main()

# ps = PrefixSpan(contents)

    # for comp in ps.topk(100):
    #     print(comp)