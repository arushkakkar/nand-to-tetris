from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable

class CompilationEngine11:
    def __init__(self, tokenizer, write_file):
        self.tokenizer = tokenizer
        self.symbols = SymbolTable()
        self.counter = 0
        self.write_file = write_file
        self.compile_class()

    def compile_class(self):
        self.tokenizer.advance()

        #class keyword
        self.tokenizer.advance()

        #class name
        assert self.tokenizer.token_type() == 'identifier'
        self.class_name = self.tokenizer.identifier()
        self.tokenizer.advance()

        # { symbol
        assert self.tokenizer.token_type() == 'symbol'
        
        self.class_field_count = 0
        
        while(self.tokenizer.has_more_tokens()):
            self.tokenizer.advance()
            if self.tokenizer.token_type() == 'symbol':
                break
            elif self.tokenizer.key_word() in ['static', 'field']:
                self.compile_class_var_dec()
                self.class_field_count += 1
            else:
                break
        
        while(self.tokenizer.has_more_tokens()):
            if self.tokenizer.token_type() == 'symbol':
                break
            else:
                self.compile_subroutine()

    def compile_class_var_dec(self):
        #scope
        assert self.tokenizer.token_type() == 'keyword'
        var_scope = self.tokenizer.key_word()
        self.tokenizer.advance()

        #type
        assert self.tokenizer.token_type() in ['keyword', 'identifier']
        var_type = self.tokenizer.key_word()
        self.tokenizer.advance()

        #name
        assert self.tokenizer.token_type() == 'identifier'
        name = self.tokenizer.identifier()
        self.tokenizer.advance()

        #semicolon
        assert self.tokenizer.token_type() == 'symbol'

        self.symbols.add_symbol(name, var_type, var_scope)

    def compile_subroutine(self):
        if self.tokenizer.key_word() == 'constructor':
            self.write_file.write('function ' + self.class_name + '.new 0' + '\n')
            self.write_file.write('push constant ' + str(self.class_field_count) + '\n')
            self.write_file.write('call Memory.alloc 1' + '\n')
            self.write_file.write('pop pointer 0' + '\n')
        
        #method type keyword
        self.tokenizer.advance()

        #return keyword
        assert self.tokenizer.token_type() in ['keyword', 'identifier']
        self.tokenizer.advance()

        #method name
        assert self.tokenizer.token_type() == 'identifier'
        self.write_file.write('function ' + self.class_name + '.' + self.tokenizer.identifier() + ' 0' + '\n')
        self.tokenizer.advance()

        #( symbol
        assert self.tokenizer.token_type() == 'symbol'
        self.tokenizer.advance()

        #parameter list
        self.compile_parameter_list()

        #) symbol
        assert self.tokenizer.token_type() == 'symbol'
        self.tokenizer.advance()

        #{ symbol
        assert self.tokenizer.token_type() == 'symbol'

        while(self.tokenizer.has_more_tokens()):
            if self.tokenizer.symbol() == '}':
                self.tokenizer.advance()
                break
            self.tokenizer.advance()
            if self.tokenizer.key_word() == 'var':
                self.compile_var_dec()
            else:
                self.compile_statements()

    def compile_parameter_list(self):
        if self.tokenizer.token_type() == 'keyword' and self.tokenizer.key_word() not in ['true', 'false']:
            self.symbols.reset_sub_scope()
            while self.tokenizer.symbol() != ')':
                assert self.tokenizer.token_type() in ['identifier', 'keyword']
                var_type = self.tokenizer.key_word()
                self.tokenizer.advance()

                assert self.tokenizer.token_type() in ['identifier']
                var_name = self.tokenizer.identifier()
                self.tokenizer.advance()

                self.symbols.add_symbol(var_name, var_type, 'argument')

                assert self.tokenizer.token_type() == 'symbol'
                if self.tokenizer.symbol() == ',':
                    self.tokenizer.advance()

    def compile_var_dec(self):
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.key_word() != 'var':
                break
            else:
                var_scope = 'var'
                self.tokenizer.advance()

                assert self.tokenizer.token_type() in ['keyword', 'identifier']
                var_type = self.tokenizer.key_word()
                self.tokenizer.advance()

                assert self.tokenizer.token_type() == 'identifier'
                var_name = [self.tokenizer.identifier()]
                self.tokenizer.advance()
                while(self.tokenizer.symbol() != ';'):
                    assert self.tokenizer.symbol() == ','
                    self.tokenizer.advance()
                    assert self.tokenizer.token_type() == 'identifier'
                    var_name.append(self.tokenizer.identifier())
                    self.tokenizer.advance()
                
                for name in var_name:
                    if self.symbols.find_symbol(name) != None:
                        raise NameError(name + ' already exists in method scope.')
                    self.symbols.add_symbol(name, var_type, 'var')

    def compile_statements(self):
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.symbol() == '}':
                break
            elif self.tokenizer.key_word() == 'let':
                self.compile_let()
            elif self.tokenizer.key_word() == 'do':
                self.compile_do()
            elif self.tokenizer.key_word() == 'while':
                self.compile_while()
            elif self.tokenizer.key_word() == 'return':
                self.compile_return()
            elif self.tokenizer.key_word() == 'if':
                self.compile_if()

    def compile_do(self):
        name2 = ''

        assert self.tokenizer.key_word() == 'do'
        self.tokenizer.advance()

        assert self.tokenizer.token_type() == 'identifier'
        name1 = self.tokenizer.identifier()
        self.tokenizer.advance()

        if self.tokenizer.symbol() == '.':
            self.tokenizer.advance()

            assert self.tokenizer.token_type() == 'identifier'
            name2 = self.tokenizer.identifier()
            self.tokenizer.advance()
        
        assert self.tokenizer.symbol() == '('
        self.tokenizer.advance()
        self.compile_expression_list()
        
        if self.tokenizer.symbol() == ';':
            self.tokenizer.unadvance()
        assert self.tokenizer.symbol() == ')'
        self.tokenizer.advance()

        call_name = name1 if name2 == '' else name1 + '.' + name2

        self.write_file.write('call ' + call_name + ' 0' + '\n')

        assert self.tokenizer.symbol() == ';'
        self.tokenizer.advance()

    def compile_let(self):
        self.tokenizer.advance()

        #var name
        assert self.tokenizer.token_type() == 'identifier'
        dest_var_name = self.tokenizer.identifier()
        self.tokenizer.advance()

        #check if we are referring to an array entry
        assert self.tokenizer.token_type() == 'symbol'
        is_array = self.tokenizer.symbol() == '['
        if is_array:
            self.tokenizer.advance()
            self.compile_expression()
            dest = self.symbols.find_symbol(dest_var_name)
            if dest != None:
                if dest[1] == 'var':
                    number = dest[2] - self.symbols.var_count('argument')
                    self.write_file.write('push local ' + str(number) + '\n')
                else:
                    number = dest[2]
                    self.write_file.write('push argument ' + str(number) + '\n')
                
                self.write_file.write('add' + '\n')
                self.write_file.write('pop pointer 1' + '\n')
                self.write_file.write('push that 0' + '\n')
            else:
                dest = self.symbols.find_in_class_scope(dest_var_name)
                number = dest[3]
                if dest[1] == 'static':
                    self.write_file.write('push static ' + str(dest[3]) + '\n')
                else:
                    self.write_file.write('push this ' + str(dest[3]) + '\n')

                self.write_file.write('add' + '\n')
                self.write_file.write('pop pointer 1' + '\n')
                self.write_file.write('push that 0' + '\n')

            assert self.tokenizer.symbol() == ']'
            self.tokenizer.advance()
        
        assert self.tokenizer.symbol() == '='
        self.tokenizer.advance()

        self.compile_expression()

        if is_array:
            self.write_file.write('pop temp 0' + '\n')
            self.write_file.write('pop pointer 1' + '\n')
            self.write_file.write('push temp 0' + '\n')
            self.write_file.write('pop that 0' + '\n')
        else:
            dest = dest = self.symbols.find_symbol(dest_var_name)
            if dest != None:
                if dest[1] == 'var':
                    number = dest[2] - self.symbols.var_count('argument')
                    self.write_file.write('pop local ' + str(number) + '\n')
                else:
                    number = dest[2]
                    self.write_file.write('pop argument ' + str(number) + '\n')
        
        if self.tokenizer.symbol() == ';':
            self.tokenizer.advance()

    def compile_while(self):
        assert self.tokenizer.key_word() == 'while'
        self.tokenizer.advance()

        self.write_file.write('label WHILE' + str(self.counter) + '\n')

        assert self.tokenizer.symbol() == '('
        self.tokenizer.advance()

        self.compile_expression()

        self.write_file.write('if-goto WHILE_END' + str(self.counter) + '\n')

        assert self.tokenizer.symbol() == ')'
        self.tokenizer.advance()

        assert self.tokenizer.symbol() == '{'
        self.tokenizer.advance()

        self.compile_statements()

        self.write_file.write('goto WHILE' + str(self.counter) + '\n')
        self.write_file.write('label WHILE_END' + str(self.counter) + '\n')

        self.counter += 1
        
        assert self.tokenizer.symbol() == '}'
        self.tokenizer.advance()

    def compile_return(self):
        assert self.tokenizer.key_word() == 'return'
        self.tokenizer.advance()

        if self.tokenizer.token_type() == 'symbol' and self.tokenizer.symbol() == ';':
            self.write_file.write('push constant 0\nreturn' + '\n')
            self.tokenizer.advance()
        else:
            self.compile_expression()
            self.write_file.write('return' + '\n')
            assert self.tokenizer.symbol() == ';'
            self.tokenizer.advance()

    def compile_if(self):
        assert self.tokenizer.key_word() == 'if'
        self.tokenizer.advance()

        assert self.tokenizer.symbol() == '('
        self.tokenizer.advance()

        self.compile_expression()

        self.write_file.write('if-goto IF_TRUE' + str(self.counter) + '\n')
        self.write_file.write('goto IF_FALSE' + str(self.counter) + '\n')
        self.write_file.write('label IF_TRUE' + str(self.counter) + '\n')
        assert self.tokenizer.symbol() == ')'
        self.tokenizer.advance()

        assert self.tokenizer.symbol() == '{'
        self.tokenizer.advance()

        self.compile_statements()

        assert self.tokenizer.symbol() == '}'
        self.tokenizer.advance()

        self.write_file.write('label IF_FALSE' + str(self.counter) + '\n')
        self.counter += 1

        if self.tokenizer.key_word() == 'else':
            self.tokenizer.advance()

            assert self.tokenizer.symbol() == '{'
            self.tokenizer.advance()

            self.compile_statements()

            assert self.tokenizer.symbol() == '}'
            self.tokenizer.advance()

    def compile_expression(self):
        self.compile_term()
        while self.tokenizer.token_type() == 'symbol' and self.tokenizer.symbol() in '+-*/&|<>=':
            operator = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            if operator == '+':
                self.write_file.write('add' + '\n')
            elif operator == '-':
                self.write_file.write('subtract' + '\n')
            elif operator == '*':
                self.write_file.write('call Math.multiply 0' + '\n')
            elif operator == '/':
                self.write_file.write('call Math.divide 0' + '\n')
            elif operator == '>':
                self.write_file.write('gt' + '\n')
            elif operator == '=':
                self.write_file.write('eq' + '\n')
            elif operator == '<':
                self.write_file.write('lt' + '\n')
            elif operator == '|':
                self.write_file.write('or' + '\n')
            elif operator == '&':
                self.write_file.write('and' + '\n')

    def compile_term(self):
        if self.tokenizer.token_type() == 'int_constant':
            self.write_file.write('push constant ' +  self.tokenizer.key_word() + '\n')
        elif self.tokenizer.token_type() == 'str_constant':
            self.write_file.write('push ' + self.tokenizer.string_value() + '\n')
        elif self.tokenizer.token_type() == 'keyword':
            if self.tokenizer.key_word() == 'true':
                self.write_file.write('push constant 1\nneg' + '\n')
            if self.tokenizer.key_word() == 'false':
                self.write_file.write('push constant 0\nnot' + '\n')
            if self.tokenizer.key_word() == 'null':
                self.write_file.write('push constant 0' + '\n')
            if self.tokenizer.key_word() == 'this':
                self.write_file.write('push pointer 0' + '\n')
        elif self.tokenizer.symbol() == '(':
            self.tokenizer.advance()
            self.compile_expression()
            assert self.tokenizer.symbol() == ')'
        elif self.tokenizer.symbol() == '~':
            self.tokenizer.advance()
            self.compile_term()
            self.write_file.write('not' + '\n')
            self.tokenizer.unadvance()
        elif self.tokenizer.symbol() == '-':
            self.tokenizer.advance()
            self.compile_term()
            self.write_file.write('neg' + '\n')
            self.tokenizer.unadvance()
        elif self.tokenizer.token_type() == 'identifier':
            name = self.tokenizer.identifier()
            self.tokenizer.advance()
            location = self.symbols.find_symbol(name)
            if location == None:
                location = self.symbols.find_in_class_scope(name)

            if self.tokenizer.symbol() not in '[(.':
                if location[1] == 'var':
                    number = location[2] - self.symbols.var_count('argument')
                    self.write_file.write('push local ' + str(number) + '\n')
                elif location[1] == 'argument':
                    self.write_file.write('push argument ' + str(location[2]) + '\n')
                elif location[1] == 'static':
                    self.write_file.write('push static ' + str(location[2]) + '\n')
                elif location[1] == 'field':
                    self.write_file.write('push this ' + str(location[2]) + '\n')
                self.tokenizer.unadvance()
            
            elif self.tokenizer.symbol() == '[':
                if location[1] == 'var':
                    number = location[2] - self.symbols.var_count('argument')
                    self.write_file.write('push local ' + str(number) + '\n')
                elif location[1] == 'argument':
                    number = location[2]
                    self.write_file.write('push argument ' + str(number) + '\n')
                elif location[1] == 'static':
                    self.write_file.write('push static ' + str(location[2]) + '\n')
                elif location[1] == 'field':
                    self.write_file.write('push this ' + str(location[2]) + '\n')
                self.tokenizer.advance()
                self.compile_expression()
                self.write_file.write('add' + '\n')
                self.write_file.write('pop pointer 1' + '\n')
                self.write_file.write('push that 0' + '\n')
                assert self.tokenizer.symbol() == ']'
            
            elif self.tokenizer.symbol() == '.':
                self.tokenizer.advance()
                method_name = self.tokenizer.identifier()
                self.tokenizer.advance()

                assert self.tokenizer.symbol() == '('
                self.compile_expression_list()
                assert self.tokenizer.symbol() == ';'

                self.write_file.write('call' + name + '.' + method_name + '\n')
            
        self.tokenizer.advance()
                
    def compile_expression_list(self):
        self.compile_expression()
        while self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.compile_expression()