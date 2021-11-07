import os
import re

class Token(object):
    def __init__(self, word):
        self._original = word
        self._types = []
        if self._original.startswith("-"):
            self._types.append("option")
        else:
            word = self._original
            if (word.startswith("'") or word.startswith('"')) and (word.endswith("'") or word.endswith('"')):
                if word.startswith('"'):
                    word = word[1:]
                if word.endswith('"'):
                    word = word[:-1]
                if word.startswith("'"):
                    word = word[1:]
                if word.endswith("'"):
                    word = word[:-1]
            word = list(os.path.splitext(word))
            flag = 0
            while word:
                comp = word.pop(-1)
                word = "".join(word)
                word = list(os.path.splitext(word))
                self._types.append(comp)
                flag = 1
                if not word[-1]:
                    break
                if flag == 1:
                    self._types.append("FILE")
            word = [cnt for cnt in word if cnt][0]
            # subs = r"[/^$]{?[a-zA-Z]}?"
            subs = r"$"
            if bool(re.search(subs, word)):
                self._types.append("SUB")
                # print(word)
                # word = re.sub(subs, "%%SUB%%", word)
                # print("word", word)
            pattern = "https?://[^/]+/"
            if bool(re.search(pattern, word)):
                self._types.append("URL")
                # word = re.sub(r"https?://[^/]+", "%%URL%%", word)
                # print("word", word)
            else:
                slash = "/"
                if bool(re.search(slash, word)):
                    self._types.append("PATH")
                    if word[-1] == "/":
                        self._types.append("DIRECTORY")
                    else:
                        self._types.append("FILE")
                else:
                    pass
                    # self._types.append("SHELL")

    @property
    def original(self):
        return self._original
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
        print(token.original)
        types = token.types
        print(types)



if __name__ == "__main__":
    main()