class SymbolTable:
    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.current_sub_index = 0
        self.static_count = 0
        self.field_count = 0

    def find_symbol(self, symbol):
        if symbol not in self.subroutine_table.keys():
            return None
        return self.subroutine_table[symbol]
    
    def find_in_class_scope(self, symbol):
        if symbol not in self.class_table.keys():
            return None
        return self.class_table[symbol]

    def add_symbol(self, name, type, scope):
        if scope in ['static', 'field']:
            count = self.static_count if scope == 'static' else self.field_count
            self.class_table[name] = (type, scope, count)
            self.current_class_index += 1
            if scope == 'static':
                self.static_count += 1
            else:
                self.field_count += 1
        else:
            self.subroutine_table[name] = (type, scope, self.current_sub_index)
            self.current_sub_index += 1
    
    def var_count(self, scope):
        count = 0
        for key in self.subroutine_table.keys():
            if self.subroutine_table[key][1] == scope:
                count += 1
        
        return count
    
    def reset_sub_scope(self):
        self.subroutine_table = {}
        self.current_sub_index = 0