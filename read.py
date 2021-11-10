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
        model = word2vec.Word2Vec.load("./Delivers/result.model")
        result = model.wv.similarity("dcdc06206343aa7476046a5897e11abc9276f1766fb6cdcd900119830b32cf2b", key)
        # result = model.wv.most_similar("dcdc06206343aa7476046a5897e11abc9276f1766fb6cdcd900119830b32cf2b", topn=10)
        # print("rm", data[key], result)
    except Exception as e:
        return 0
    else:
        return result

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

        for shell in shells:
            hash_words = Hash.execute(shell)
            if not [cnt for cnt in hash_words] in hh:
                hh.append([cnt for cnt in hash_words])
            for key, value in hash_words.items():
                if not key in data:
                    data[key] = value
    
    results = {}

    for key, value in data.items():
        if value == "-rf":
            nh0 = [h for h in hh if key in h][0]
            command0 = [sub(n) for n in nh0]
            print(command0)
            try:
                nh1 = [h for h in hh if key in h][1]
            except:
                pass
            else:
                command1 = [sub(n) for n in nh1]
                print(command1)
            

        


      
        # results[value] = execute(key) 


            






if __name__ == "__main__":
    main()