import os
import re

class Token(object):
    def __init__(self, word):
        def norm(word):
            if (word.startswith("'") or word.startswith('"')) and (word.endswith("'") or word.endswith('"')):
                if word.startswith('"'):
                    word = word[1:]
                if word.endswith('"'):
                    word = word[:-1]
                if word.startswith("'"):
                    word = word[1:]
                if word.endswith("'"):
                    word = word[:-1]
            return word
        def extent(word):
            ext = word.split("/")[-1]
            exts = ext.split(".")
            return exts[1:]
        
        def kind(word):
            pattern = "https?://[^/]+/"
            if bool(re.search(pattern, word)):
                return "URL"
            else:
                if word[-1] == "/":
                    return "DIRECTORY"
                else:
                    return "FILE"

        def sub(word):
            words = word.split("/")
            for word in words:
                if word.startswith("$"):
                    return True
            else:
                return False

        self._original = norm(word)
        self._extentions = extent(self._original)
        self._kinds = kind(self._original)
        self._types = []
        self._subs = sub(self._original)

        if not "/" in self._original:
            if self._original.startswith("-"):
                self._kinds = "OPTIONS"
            else:
                if not self._extentions:
                    if "$" in self._original:
                        self._kinds = "SUB"
                    else:
                        self._kinds = "SHELL"
                else:
                    if "$" in self._original:
                        self._kinds = "SUB"
                    else:
                        self._kinds = "FILE"
        
        if self._original == "NT":
            self._kinds = "NT"
        
        if self._original == "[":
            self._kinds = "[LEFT]"
        
        if self._original == "]":
            self._kinds = "[RIGHT]"
        
        if self._original == "(":
            self._kinds = "(LEFT)"
        
        if self._original == ")":
            self._kinds = "(RIGHT)"
        
        if self._original == "{":
            self._kinds = "{LEFT}"
        
        if self._original == "}":
            self._kinds = "{RIGHT}"
        
        if self._original == "|":
            self._kinds = "PIPE1"
        
        if self._original == "||":
            self._kinds = "PIPE2"
        
        if self._original == ">":
            self._kinds = "REDIRECT1"
        
        if self._original == ">>":
            self._kinds = "REDIRECT2"
            
    def change_kinds(self):
        pass

    @property
    def original(self):
        return self._original
    @property
    def extentions(self):
        return self._extentions
    @property
    def kinds(self):
        return self._kinds
    
    @property
    def subs(self):
        return self._subs
    @property
    def types(self):
        self._types = [cnt for cnt in self._types if cnt]
        return self._types







def main():
    words = [
        'wget', 
        '-O', 
        'python.tar.xz.asc', 
        '"https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"',
        '"http://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"',
        "/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION",
        "/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python/"
    ]

    for word in words:
        token = Token(word)
        print()
        print("original", token.original)
        print("extentions", token.extentions)
        print("kinds", token.kinds)
        print("subs", token.subs)



if __name__ == "__main__":
    main()