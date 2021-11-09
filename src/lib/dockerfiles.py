import dockerfile
import re


INSTRUCTIONS = [
    "MAINTAINER",
    "RUN",
    "CMD",
    "ENTRYPOINT",
    "LABEL",
    "EXPOSE",
    "ENV",
    "ADD",
    "COPY",
    "VOLUME",
    "USER",
    "WORKDIR",
    "ARG",
    "ONBUILD",
    "STOPSIGNAL",
    "HEALTHCHECK",
    "SHELL",
    "#"
]

class Dockerfile(object):
    """
        オリジナルのDockerfileクラス
    """
    def __init__(self, file_path):
        self._contexts = dockerfile.parse_file(file_path)

        def split_method_chain(scripts):
            """
                RUN命令の中のSCの分割
            """
            def check_by_regex(contents):
                if contents == "|":
                    return True
                elif contents == "||":
                    return True
                elif contents == ">":
                    return True
                elif contents == ">>":
                    return True
                elif contents == "[":
                    return True
                elif contents == "]":
                    return True
                elif contents == "(":
                    return True
                elif contents == ")":
                    return True
                elif contents == "{":
                    return True
                elif contents == "}":
                    return True
                else:
                    return bool(re.search(r"[a-zA-Z]", contents)) or \
                        bool(re.search(r"[0-9]", contents))
            
            def split_option(tokens):
                tokens = list(tokens)
                mark = tokens.pop(0)
                return [mark+token for token in tokens]

            scripts = re.sub("\n", " NL ", scripts)
            scripts = re.sub("\t", " NT ", scripts)
            # method-chainの共通化
            scripts = re.sub(";", " AND ", scripts)
            scripts = re.sub("&&", " AND ", scripts)

            tokens = ["RUN"] + [token.lstrip().rstrip() for token in scripts.split()]

            """
                ${} $()の処理を施す
            """


            tokens = [token.replace("[", " [ ") for token in tokens]
            tokens = [token.replace("]", " ] ") for token in tokens]
            tokens = [token.replace("(", " ( ") for token in tokens]
            tokens = [token.replace(")", " ) ") for token in tokens]
            tokens = [token.replace("{", " { ") for token in tokens]
            tokens = [token.replace("}", " } ") for token in tokens]
            # tokens = [token.lstrip().rstrip() for token in scripts.split()]

            sec_tokens = []
            for token in tokens:
                comps = [comp.lstrip().rstrip() for comp in token.split()]
                sec_tokens.extend(comps)
            tokens = [token for token in sec_tokens if check_by_regex(token)]

            return tokens


        commands = []
        for context in self._contexts:
            if context.cmd == "RUN":
                commands.append(split_method_chain(context.value[0]))
            elif context.cmd == "ENV" or "COPY" or "ADD" or "ARG" or "VOLUME":
                commands.append([context.cmd]+list(context.value[:2]))
            elif context.cmd == "CMD" or "ENTRYPOINT":
                commands.append([context.cmd]+list(context.value))
            else:
                commands.append([context.cmd. context.value[0]])
            
        self._commands = commands

    def get_run(self):
        """
            RUN命令のみを返すメソッド
        """
        return [comp for comp in self._commands if comp[0] == "RUN"]
    
    def get_shell_origin(self):
        """
            RUN命令の中のshellscriptを返すメソッド
        """
        res = []
        contents = [comp for comp in self._commands if comp[0] == "RUN"]
        for content in contents:

            comps = []
            comp = []
            comps.append(content.pop(0))
            while content:
                cnt = content.pop(0)
                if cnt == "AND":
                    comps.append(comp)
                    comp = []
                else:
                    comp.append(cnt)
            res.append(comps)
        return res
    
    def get_shell(self):
        """
            RUN命令の中のshellscriptを返すメソッド
            インデントを考慮している
        """
        res = []
        contents = [comp for comp in self._commands if comp[0] == "RUN"]
        for content in contents:
            # content = [cnt for cnt in content if cnt != "NT"]
            # content = [cnt for cnt in content if cnt != "NL"]
            comps = []
            comp = []
            # print()
            # print("================")
            # print("コンテンツの中身", "->", "ここはできているっぽい")
            # print("content", content)
            # print("================")
            # print()
            comps.append(content.pop(0))
            while content:
                cnt = content.pop(0)
                if cnt == "AND":
                    while comp:
                        cn = comp.pop(-1)
                        if cn != ("NT" or "NL"):
                            comp.append(cn)
                            break
                        else:
                            comps.append("AFTER")
                            # comps.append(cn)
                    while comp:
                        cn = comp.pop(0)
                        if cn != ("NT" or "NL"):
                            comp.insert(0, cn)
                            break
                        else:
                            comps.append("BEFORE")
                            # comps.append(cn)
                    comps.append(comp)
                    comp = []
                else:
                    comp.append(cnt)

            # print()
            # print("前後の改行処理", "->", "ここはできているっぽい")
            # print("================")
            # for comp in comps:
            #     print("comp", comp)
            # print("================")
            # print()

            afters = []
            ans = []
            while comps:
                cnt = comps.pop(0)
                if cnt == "AFTER":
                    afters.append(cnt)
                else:
                    ans.append(cnt)
                    while afters:
                        ans.append(afters.pop(0))
            
            # print()
            # print("AFTERの順番処理", "->", "OK?")
            # print("================")
            # for an in ans:
            #     print("an", an)
            # print("================")
            # print()

            subs = []
            for an in ans:
                if type(an) == list:
                    sub = []
                    ins = []
                    if ("NT" or "NL") in an:
                        while an:
                            cm = an.pop(0)
                            if cm != ("NT" or "NL"):
                                if not sub:
                                    sub.extend(ins)
                                sub.append(cm)
                                ins = []
                            else:
                                if sub:
                                    subs.append(sub)
                                ins.append(cm)
                                sub = []
                    else:
                        subs.append(an)
                else:
                    subs.append(an)
            # print()
            # print("命令の中の処理", "->", "できったぽい")
            # print("================")
            # for sub in subs:
            #     print(sub)
            # print("================")
            # print()

            res.append(subs)
        return res

    def word_check(self, word):
        """
            キーワードでDockerfileをフィルタリング
        """
        for command in self._commands:
            if word in command:
                return True
                break
        else:
            return False
    

    @property
    def contexts(self):
        return self._contexts

    @property
    def commands(self):
        return self._commands


class Indent(object):
    def __init__(self, file_path):
        pass


URL_RE_PATTERN = "https?://[^/]+/"

class Model(object):
    def __init__(self, file_path):
        self._contents = dockerfile.parse_file(file_path)
        # トークンの正規化
        def norm(token):
            """
                "とか'を削除
            """
            if token.startswith('"'):
                token = token[1:]
            if token.endswith('"'):
                token = token[:-1]
            if token.startswith("'"):
                token = token[1:]
            if token.endswith("'"):
                token = token[:-1]
            return token
        # メソッドチェーンやトークン, スペース, 改行コードの正規化
        def method_chain(scripts):
            """
                メソッドチェーンの分割やスペース, 改行コードの正規化
            """
            scripts = re.sub("\n", " NL ", scripts)
            scripts = re.sub("\t", " NT ", scripts)
            scripts = re.sub(";", " AND ", scripts)
            scripts = re.sub("&&", " AND ", scripts)
            scripts = re.sub(" ", " SPACE ", scripts)

            tokens = ["RUN"] + [token.lstrip().rstrip() for token in scripts.split()]
            Res = []
            while tokens:
                word = tokens.pop(0)
                if bool(re.search(URL_RE_PATTERN, word)):
                    word = norm(word)
                    Res.append(word)
                else:
                    if word == "\\(":
                        word = "BACKLEFT"
                        Res.append(word)
                    elif word == "\\)":
                        word = "BACKRIGHT"
                        Res.append(word)
                    elif word == "\\n":
                        word = "BACKNT"
                        Res.append(word)
                    elif word == "(":
                        word = "LEFT"
                        Res.append(word)
                    elif word == "[":
                        word = "LEFT"
                        Res.append(word)
                    elif word == "{":
                        word = "LEFT"
                        Res.append(word)
                    elif word == ")":
                        word = "RIGHT"
                        Res.append(word)
                    elif word == "]":
                        word = "RIGHT"
                        Res.append(word)
                    elif word == "}":
                        word = "RIGHT"
                        Res.append(word)
                    else:
                        if "$(" or "$[" or "${" in word:
                            word = word.replace("$(", " SUBLEFT ")
                            word = word.replace("$[", " SUBLEFT ")
                            word = word.replace("${", " SUBLEFT ")
                        if ")'" or ')"' in word:
                            word = word.replace(")'" , " SUBRIGHT ")
                            word = word.replace(')"', " SUBRIGHT ")

                        words = word.split()
                        for word in words:
                            word = norm(word)
                            backs = []
                            if word == "{}":
                                Res.append(word)
                            elif word.endswith(")") or word.endswith("]") or word.endswith("}"):
                                Res.append(word[:-1])
                                Res.append("SUBRIGHT")
                            else:
                                Res.append(word)

            Res = [norm(res) for res in Res]
            return Res


        self._commands = []
        for content in self._contents:
            if content.cmd == "RUN":
                self._commands.append(method_chain(content.value[0]))
            elif content.cmd == "ENV" or "COPY" or "ADD" or "ARG" or "VOLUME":
                self._commands.append([content.cmd]+list(content.value[:2]))
            elif content.cmd == "CMD" or "ENTRYPOINT":
                self._commands.append([content.cmd]+list(content.value))
            else:
                self._commands.append([content.cmd]+list(content.value[0]))
        
        self._runs = []
        for command in self._commands:
            com = command.pop(0)
            if com == "RUN":
                Req = []
                comp = []
                while command:
                    word = command.pop(0)
                    if word == "AND":
                        Req.append(comp)
                        comp = []
                    else:
                        comp.append(word)
                self._runs.append(Req)

        self._shells = []
        for run in self._runs:
            # self._shells.append([])
            for shells in run:
                shells = [shell for shell in shells if shell != "SPACE"]
                shells = [shell for shell in shells if shell != "NT"]
                shells = [shell.replace("(", "") for shell in shells]
                shells = [shell.replace("(", "") for shell in shells]
                shells = [shell.replace(")", "") for shell in shells]
                shells = [shell.replace(")", "") for shell in shells]
                shells = [shell.replace("[", "") for shell in shells]
                shells = [shell.replace("[", "") for shell in shells]
                shells = [shell.replace("]", "") for shell in shells]
                shells = [shell.replace("]", "") for shell in shells]

                shells = [shell.replace("\\n", "BACKNT") for shell in shells]

                shells = [norm(shell) for shell in shells]
                shells = [shell for shell in shells if shell]
                self._shells.append(shells)


    @property
    def contents(self):
        return self._contents
    
    @property
    def commands(self):
        return self._commands
    
    @property
    def runs(self):
        return self._runs
    
    @property
    def shells(self):
        return self._shells



def main():
    file_path = "../../python/3.10/bullseye/slim/Dockerfile"
    # file_path = "../../Others/Dockerfile"
    model = Model(file_path)
    commands = model.commands
    runs = model.runs
    for run in runs:
        print()
        for shells in run:
            shells = [shell for shell in shells if shell != ("SPACE" or "NT")]
            print(shells)
if __name__ == "__main__":
    main()
