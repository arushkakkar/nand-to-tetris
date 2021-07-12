import os
import glob
from CompilationEngine11 import CompilationEngine11
from JackTokenizer import JackTokenizer

class FileExplorer:
    def __init__(self, path):
        files = []
        if os.path.isfile(path):
            files = [path]
        else:
            files = glob.glob(path + '*.jack')

        for file_path in files:
            tokenizer = JackTokenizer(file_path)
            write_file_path = file_path[:file_path.index('.')] + '.vm'
            write_file = open(write_file_path, 'w')
            CompilationEngine11(tokenizer, write_file)
            write_file.close()

if __name__ == '__main__':
    start = FileExplorer('/home/arush/Desktop/project10_11/')