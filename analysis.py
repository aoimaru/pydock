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


class UnionFind(object):
    """
    ナイーブなUnionFind木
    - find関数で繋ぎかえる効率化を行なっていない
    """
    def __init__(self, n):
        self._n = n
        self._parents = [-1]*n
    def find(self, x):
        if self._parents[x] < 0:
            return x
        else:
            return self.find(self._parents[x])
    
    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        
        if x == y:
            return
        # if self._parents[x] > self._parents[y]:
        #     x, y = y, x
        
        self._parents[x] += self._parents[y]
        self._parents[y] = x
        
    def size(self, x):
        return -self._parents[self.find(x)]
    
    @property
    def parents(self):
        return self._parents



PYTHON_PROJECT = "./python/**"
OTHERS = "./Others/**"

def main():
    combinations = {}
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    words = []
    targets = []
    for file_path in file_paths:
        dock = Dockerfile(file_path)
        contents = dock.commands
        for content in contents:
            content = [cnt for cnt in content if cnt != "AND"]
            content = [cnt for cnt in content if cnt != "RUN"]
            content = [cnt for cnt in content if cnt != "set"]
            # content = [cnt for cnt in content if cnt != "-ex"]
            # content = [cnt for cnt in content if cnt != "wget"]
            content = [cnt for cnt in content if cnt != "CMD"]
            content = [cnt for cnt in content if cnt != "ENV"]
            words.extend(content)
            n_grams = NLP.n_gram(content, 2)
            for ng in n_grams:
                targets.append(ng)
    
    words = set(words)
    Dit = {val: ix for ix, val in enumerate(words)}
    Dit2 = {ix: val for ix, val in enumerate(words)}
    print(len(words))
    uf = UnionFind(len(words))
    for target in targets:
        uf.union(Dit[target[0]], Dit[target[1]])

    prts = uf.parents
    for prt in prts:
        try:
            print(Dit2[prt])
        except:
            pass

    

if __name__ == "__main__":
    main()

# ps = PrefixSpan(contents)

    # for comp in ps.topk(100):
    #     print(comp)