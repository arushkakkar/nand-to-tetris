from Parser import Parser
import os
import glob

class CodeWriter:
    def __init__(self, path):
        self.write_file = None
        self.parser = None
        files = []
        if os.path.isfile(path):
            write_file_path = path[:path.index('.')] + '.asm'
            self.write_file = open(write_file_path, 'w')
            files = [path]
        else:
            temp = path.split('/')
            write_file_name = temp[len(temp)-2]
            write_file_path = path + write_file_name + '.asm'
            self.write_file = open(write_file_path, 'w')
            files = glob.glob(path + '*.vm')
        
        self.current_file_name = ''
        self.current_line_asm_file = 0
        self.init_written = False
        for file_path in files:
            current_file_name = os.path.basename(file_path)
            self.current_file_name = current_file_name[:current_file_name.index('.')]
            self.parser = Parser(file_path)
            self.start_writing()
        
        self.write_file.close()

    def start_writing(self):
        if not self.init_written:
            self.write_init()
            self.init_written = True
        while self.parser.has_more_commands():
            self.current_line_asm_file += 1
            self.parser.advance()
            code_type = self.parser.code_type()
            if code_type in ['push', 'pull']:
                self.write_push_pop()
            elif code_type == 'arithmetic':
                self.write_arithmetic()
            elif code_type == 'function':
                self.write_function()
            elif code_type == 'label':
                self.write_label()
            elif code_type == 'goto':
                self.write_goto()
            elif code_type == 'ifgoto':
                self.write_ifgoto()
            elif code_type == 'return':
                self.write_return()
            elif code_type == 'call':
                self.write_call()

    def write_function(self):
        function = self.parser.arg1()
        count = self.parser.arg2()
        self.write_file.write('(%s)\n' % function)
        self.write_file.write('@%s\n'  % count)
        self.write_file.write('D=A\n')
        self.write_file.write('@13\n')
        self.write_file.write('M=D\n')
        self.write_file.write('(loop.%s)\n' % function)
        self.write_file.write('@13\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@break.%s\n' % function)
        self.write_file.write('D;JEQ\n')
        self.write_file.write('@SP\n')
        self.write_file.write('A=M\n')
        self.write_file.write('M=0\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=M+1\n')
        self.write_file.write('@13\n')
        self.write_file.write('M=M-1\n')
        self.write_file.write('@loop.%s\n' % function)
        self.write_file.write('0;JMP\n')
        self.write_file.write('(break.%s)\n' % function)

    def write_label(self):
        self.write_file.write('(%s)\n' % self.parser.arg1())

    def write_goto(self):
        self.write_file.write('@%s\n' % self.parser.arg1())

    def write_ifgoto(self):
        self.write_file.write('@SP\n')
        self.write_file.write('A=M-1\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=M-1\n')
        self.write_file.write('@%s\n' % self.parser.arg1())
        self.write_file.write('D;JNE\n')

    def write_return(self):
        self.write_file.write('@LCL\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@13\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@13\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@5\n')
        self.write_file.write('D=D-A\n')
        self.write_file.write('A=D\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@14\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@SP\n')
        self.write_file.write('A=M-1\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@ARG\n')
        self.write_file.write('A=M\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=M-1\n')
        self.write_file.write('@ARG\n')
        self.write_file.write('D=M+1\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@13\n')
        self.write_file.write('A=M-1\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@THAT\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@13\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@2\n')
        self.write_file.write('A=D-A\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@THIS\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@13\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@3\n')
        self.write_file.write('A=D-A\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@ARG\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@13\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@4\n')
        self.write_file.write('A=D-A\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@LCL\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@14\n')
        self.write_file.write('A=M\n')
        self.write_file.write('0;JMP\n')

    def write_call(self):
        function = self.parser.arg1()
        num_args = self.parser.arg2()
        return_label = 'return.' + str(self.current_line_asm_file)
        self.write_file.write('@%s\n' % return_label)
        self.write_file.write('D=A\n')
        self.write_file.write('@SP\n')
        self.write_file.write('A=M\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=M+1\n')
        self.write_file.write('@LCL\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@SP\n')
        self.write_file.write('A=M\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=M+1\n')
        self.write_file.write('@ARG\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@SP\n')
        self.write_file.write('A=M\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=M+1\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@SP\n')
        self.write_file.write('A=M\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=M+1\n')
        self.write_file.write('@SP\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@%s\n' % num_args)
        self.write_file.write('D=D-A\n')
        self.write_file.write('@5\n')
        self.write_file.write('D=D-A\n')
        self.write_file.write('@ARG\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@SP\n')
        self.write_file.write('D=M\n')
        self.write_file.write('@LCL\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@%s\n' % function)
        self.write_file.write('0;JMP\n')
        self.write_file.write('(%s)\n' % return_label)
    
    def write_init(self):
        self.write_file.write('@256\n')
        self.write_file.write('D=A\n')
        self.write_file.write('@SP\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@300\n')
        self.write_file.write('D=A\n')
        self.write_file.write('@LCL\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@400\n')
        self.write_file.write('D=A\n')
        self.write_file.write('@ARG\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@3000\n')
        self.write_file.write('D=A\n')
        self.write_file.write('@THIS\n')
        self.write_file.write('M=D\n')
        self.write_file.write('@3010\n')
        self.write_file.write('D=A\n')
        self.write_file.write('@THAT\n')
        self.write_file.write('M=D\n')

    def write_arithmetic(self):
        arg = self.parser.arg1()
        if arg == 'add':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('D=M\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('D=D+M\n')
            self.write_file.write('M=D\n')
            self.write_file.write('@SP\n')
            self.write_file.write('M=M-1\n')
        elif arg == 'sub':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('D=M\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('D=M-D\n')
            self.write_file.write('M=D\n')
            self.write_file.write('@SP\n')
            self.write_file.write('M=M-1\n')
        elif arg == 'neg':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('M=-M\n')
        elif arg == 'eq':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('D=M\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('D=M-D\n')
            self.write_file.write('@true.%s\n' % self.parser.current_index)
            self.write_file.write('D;JEQ\n')
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('M=0\n')
            self.write_file.write('@break.%s\n' % self.parser.current_index)
            self.write_file.write('0;JMP\n')
            self.write_file.write('(true.%s)\n' % self.parser.current_index)
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('M=-1\n')
        elif arg == 'gt':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('D=M\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('D=M-D\n')
            self.write_file.write('@true.%s\n' % self.parser.current_index)
            self.write_file.write('D;JGT\n')
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('M=0\n')
            self.write_file.write('@break.%s\n' % self.parser.current_index)
            self.write_file.write('0;JMP\n')
            self.write_file.write('(true.%s)\n' % self.parser.current_index)
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('M=-1\n')
            self.write_file.write('(break.%s)\n' % self.parser.current_index)
            self.write_file.write('@SP\n')
            self.write_file.write('M=M-1\n')
        elif arg == 'lt':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('D=M\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('D=M-D\n')
            self.write_file.write('M=0\n')
            self.write_file.write('@break.%s\n' % self.parser.current_index)
            self.write_file.write('0;JMP\n')
            self.write_file.write('(true.%s)\n' % self.parser.current_index)
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('M=-1\n')
            self.write_file.write('(break.%s)\n' % self.parser.current_index)
            self.write_file.write('@SP\n')
            self.write_file.write('M=M-1\n')
        elif arg == 'and':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('D=M\n')
            self.write_file.write('A=A-1\n')
            self.write_file.write('M=D&M\n')
            self.write_file.write('@SP\n')
            self.write_file.write('M=M-1\n')
        elif arg == 'or':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('D=M\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('M=-M\n')
        elif arg == 'not':
            self.write_file.write('@SP\n')
            self.write_file.write('A=M-1\n')
            self.write_file.write('M=!M\n')

    def write_push_pop(self):
        arg1 = self.parser.arg1()
        arg2 = self.parser.arg2()
        if self.parser.code_type() == 'push':
            if arg1 == 'constant':
                self.write_file.write('@%s\n' % arg2)
                self.write_file.write('D=A\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
            if arg1 == 'temp':
                self.write_file.write('@%s\n' % arg2)
                self.write_file.write('D=A\n')
                self.write_file.write('@5\n')
                self.write_file.write('A=D+A\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
            if arg1 == 'pointer':
                self.write_file.write('@%s\n' % arg2)
                self.write_file.write('D=A\n')
                self.write_file.write('@3\n')
                self.write_file.write('A=D+A\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
            if arg1 == 'local':
                self.write_file.write('@%s\n' % arg2)
                self.write_file.write('D=A\n')
                self.write_file.write('@LCL\n')
                self.write_file.write('A=D+M\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
            if arg1 == 'argument':
                self.write_file.write('@%s\n' % arg2)
                self.write_file.write('D=A\n')
                self.write_file.write('@ARG\n')
                self.write_file.write('A=D+M\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
            if arg1 == 'this':
                self.write_file.write('@%s\n' % arg2)
                self.write_file.write('D=A\n')
                self.write_file.write('@THIS\n')
                self.write_file.write('A=D+M\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
            if arg1 == 'that':
                self.write_file.write('@%s\n' % arg2)
                self.write_file.write('D=A\n')
                self.write_file.write('@THAT\n')
                self.write_file.write('A=D+M\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
            if arg1 == 'static':
                self.write_file.write('@%s.%s\n' % (self.current_file_name, arg2))
                self.write_file.write('D=M\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')

            self.write_file.write('@SP\n')
            self.write_file.write('M=M+1\n')

        if self.parser.code_type() == 'pop':
            self.write_file.write('@%s\n' % arg2)
            self.write_file.write('D=A\n')
            if arg1 == 'local':
                self.write_file.write('@LCL\n')
                self.write_file.write('D=D+M\n')
                self.write_file.write('@13\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M-1\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@13\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('M=M-1\n')
            elif arg1 == 'argument':
                self.write_file.write('@ARG\n')
                self.write_file.write('D=D+M\n')
                self.write_file.write('@13\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M-1\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@13\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('M=M-1\n')
            elif arg1 == 'this':
                self.write_file.write('@THIS\n')
                self.write_file.write('D=D+M\n')
                self.write_file.write('@13\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M-1\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@13\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('M=M-1\n')
            elif arg1 == 'that':
                self.write_file.write('@THAT\n')
                self.write_file.write('D=D+M\n')
                self.write_file.write('@13\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M-1\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@13\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('M=M-1\n')
            elif arg1 == 'temp':
                self.write_file.write('@5\n')
                self.write_file.write('D=D+A\n')
                self.write_file.write('@13\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M-1\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@13\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('M=M-1\n')
            elif arg1 == 'pointer':
                self.write_file.write('@3\n')
                self.write_file.write('D=D+A\n')
                self.write_file.write('@13\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('A=M-1\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@13\n')
                self.write_file.write('A=M\n')
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('M=M-1\n')
            elif arg1 == 'static':
                self.write_file.write('@SP\n')
                self.write_file.write('A=M-1\n')
                self.write_file.write('D=M\n')
                self.write_file.write('@%s.%s\n' % (self.current_file_name, arg2))
                self.write_file.write('M=D\n')
                self.write_file.write('@SP\n')
                self.write_file.write('M=M-1\n')
            else:
                pass
        

if __name__ == '__main__':
    dirs = ['/home/arush/Desktop/project78/project78/07/MemoryAccess/BasicTest/',
            '/home/arush/Desktop/project78/project78/07/MemoryAccess/PointerTest/',
            '/home/arush/Desktop/project78/project78/07/MemoryAccess/StaticTest/',
            '/home/arush/Desktop/project78/project78/07/StackArithmetic/SimpleAdd/',
            '/home/arush/Desktop/project78/project78/07/StackArithmetic/StackTest/',
            '/home/arush/Desktop/project78/project78/08/FunctionCalls/FibonacciElement/',
            '/home/arush/Desktop/project78/project78/08/FunctionCalls/NestedCall/',
            '/home/arush/Desktop/project78/project78/08/FunctionCalls/SimpleFunction/',
            '/home/arush/Desktop/project78/project78/08/FunctionCalls/StaticsTest/',
            '/home/arush/Desktop/project78/project78/08/ProgramFlow/BasicLoop/',
            '/home/arush/Desktop/project78/project78/08/ProgramFlow/FibonacciSeries/'
            ]
    for path in dirs:
        code_writer = CodeWriter(path)