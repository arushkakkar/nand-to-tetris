class JackTokenizer:
    
    def __init__(self, path):
        code_file = open(path, 'r')
        self.code = code_file.readlines()
        i = 0
        while(i < len(self.code)):
            if self.code[i][:2] == '//' or self.code[i] == '\n':
                self.code.pop(i)
                continue
            if '//' in self.code[i]:
                self.code[i] = self.code[i][:self.code[i].find('//')]
            
            self.code[i] = self.code[i].replace('\n', '')
            self.code[i] = self.code[i].replace('\t', '')
            i += 1

        self.tokens = []
        for line in self.code:
            for t in self.get_tokens(line):
                self.tokens.append(t)
        
        self.current_index = -1
        self.current_token = None

    def has_more_tokens(self):
        return self.current_index < len(self.tokens) - 1

    def advance(self):
        self.current_index += 1
        self.current_token = self.tokens[self.current_index]
    
    def unadvance(self):
        self.current_index -= 1
        self.current_token = self.tokens[self.current_index]

    def get_tokens(self, line):
        tokens = []
        token_start = 0
        token_end = 0
        while(True):
            if line[token_start] == '"':
                token_end += 1
                while line[token_end] != '"':
                    token_end += 1
                token_end +=1
                tokens.append(line[token_start:token_end])
                token_start = token_end
            elif line[token_end] in [' ', '{', '}', '[', ']', '.', '(', ')', ';', '=', '+', '-', '*', ',', '/', '&', '|', '=', '~']:
                tokens.append(line[token_start:token_end])
                if line[token_end] != ' ':
                    tokens.append(line[token_end])
                if token_end == len(line) - 1:
                    break
                token_end += 1
                token_start = token_end
            elif line[token_end] in ['<', '>']:
                tokens.append(line[token_start:token_end])
                if line[token_end + 1] == '=':
                    tokens.append(line[token_end:token_end+2])
                    token_end += 2
                    token_start = token_end
                else:
                    tokens.append(line[token_end])
                    token_end += 1
                    token_start = token_end
            elif token_end == len(line) - 1:
                tokens.append(line[token_start:token_end])
                break
            else:
                token_end += 1
        try:
            while True:
                tokens.remove('')
        except ValueError:
            pass

        return tokens

    def token_type(self):
        if self.current_token in ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                     'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']:
            return 'keyword'
        elif self.current_token in [' ', '{', '}', '[', ']', '.', '(', ')', ';', '=', '+', '-', '*', ',', '/', '&', '|', '=', '~', '<', '>', '<=', '>=']:
            return 'symbol'
        else:
            try:
                int(self.current_token)
                return 'int_constant'
            except(ValueError):
                if self.current_token[0] == '"':
                    return 'str_constant'
                else:
                    return 'identifier'

    def key_word(self):
        return self.current_token
    
    def symbol(self):
        return self.current_token
    
    def identifier(self):
        return self.current_token
    
    def int_value(self):
        return int(self.current_token)
    
    def string_value(self):
        return self.current_token[1:-1]