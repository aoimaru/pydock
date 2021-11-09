


class Dived(object):
    @staticmethod
    def mask(shells: list):
        def n_gram(contents, rg):
            return [contents[cnt: cnt+rg] for cnt in range(len(contents)-rg+1)]
        
        comp = []
        for shell in shells:
            ngrams = n_gram(shell, 2) 
            print(ngrams)


def main():
    pass


if __name__ == "__main__":
    main()