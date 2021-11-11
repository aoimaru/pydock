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
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]

    results = {}
    # query = ['apt-get', 'install', '-y', '--no-install-recommends', 'uuid-dev']
    query = ['apt-get', 'install', '-y', '--no-install-recommends']
    # query = ['find', '/usr/local', '-depth', 'BACKLEFT', 'BACKLEFT', '-type', 'd', '-a', 'BACKLEFT']
    # query = ["rm", "-rf"]
    # hash_query = Hash.execute(query)
    # query = [cnt for cnt in hash_query]
    print(query)
    for file_path in file_paths:
        model = Model(file_path)
        shells = model.shells
        for shell in shells:
            # shell_dict = Hash.execute(shell)
            # data = [cnt for cnt in shell_dict]
            # print(data)
            result = Zlib.ncd(query, shell)
            # print(result, ":", shell)
            results[" ".join(shell)] = result
    
    # results = sorted(results.items(), key=lambda x:x[1])
    # for result in results[:10]:
    #     print(result)
    
    for key, value in results.items():
        if value < 0.50:
            print(value, key)
    
    
    # for comp in data:
    #     print(data)
        # result = Zlib.ncd(query, data)
        # print(result)
            
            




if __name__ == "__main__":
    main()

