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

def execute(key):
    try:
        # print(data["dcdc06206343aa7476046a5897e11abc9276f1766fb6cdcd900119830b32cf2b"])
        model = word2vec.Word2Vec.load("./Delivers/result.model")
        results = model.wv.similarity("rm", key)
        # results = model.wv.most_similar("rm", topn=30)
        
        # for result in results:
        #     print("rm", data[key], result)
    except Exception as e:
        return 0
    else:
        return results

def sub(key):
    return data[key]

PYTHON_PROJECT = "./python/**"
def main():
    combinations = {}
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    global data
    data = {}
    hh =  []
    for file_path in file_paths:
        model = Model(file_path)
        shells = model.shells

    
    results = execute("-rf")
    # for result in results:
    print(results)
            

   


            






if __name__ == "__main__":
    main()