


class NLP(object):
    @staticmethod
    def n_gram(contents, rg):
        return [contents[cnt: cnt+rg] for cnt in range(len(contents)-rg+1)]
    
    @staticmethod
    def co_occurrence(contents):
        pass