class Parser:
    
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
            
            self.code[i] = self.code[i].replace(' ', '')
            self.code[i] = self.code[i].replace('\n', '')
            i += 1

        self.current_index = -1
        self.current_line = None

    def has_more_commands(self):
        return self.current_index < len(self.code) - 1

    def advance(self):
        self.current_index += 1
        self.current_line = self.code[self.current_index]

    def code_type(self):
        if self.current_line in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return 'arithmetic'
        elif 'push' in self.current_line:
            return 'push'
        elif 'pop' in self.current_line:
            return 'pop'
        elif 'label' in self.current_line:
            return 'label'
        elif 'if-goto' in self.current_line:
            return 'ifgoto'
        elif 'goto' in self.current_line:
            return 'goto'
        elif 'function' in self.current_line:
            return 'function'
        elif 'call' in self.current_line:
            return 'call'
        elif 'return' in self.current_line:
            return 'return'

    def arg1(self):
        if self.code_type() == 'arithmetic':
            return self.current_line
        else:
            arguments = self.remove_command_helper()
            return arguments[:self.find_first_digit_helper(arguments)]

    def arg2(self):
        if self.code_type() == 'arithmetic':
            return self.current_line
        else:
            return self.current_line[self.find_first_digit_helper(self.current_line):]

    def remove_command_helper(self):
        if(self.code_type() == 'push'):
            return self.current_line[4:]
        elif(self.code_type() == 'pop'):
            return self.current_line[3:]
        elif(self.code_type() == 'label'):
            return self.current_line[5:]
        elif(self.code_type() == 'ifgoto'):
            return self.current_line[6:]
        elif(self.code_type() == 'goto'):
            return self.current_line[4:]
        elif(self.code_type() == 'function'):
            return self.current_line[8:]
        elif(self.code_type() == 'call'):
            return self.current_line[4:]
        elif(self.code_type() == 'return'):
            return self.current_line[6:]

    def find_first_digit_helper(self, s):
        for c in s:
            if c.isdigit():
                return s.index(c)
