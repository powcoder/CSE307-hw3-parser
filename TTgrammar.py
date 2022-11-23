https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
import sys

# Propositional Logic Grammar

# AST Nodes

class Node():
    def __init__(self):
        self.parent = None

    def parentCount(self):
        count = 0
        current = self.parent
        while current is not None:
            count += 1
            current = current.parent
        return count

class Assignment(Node):
    def __init__(self, lvalue, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.lvalue.parent = self
        self.rvalue.parent = self
        
    def eval(self):
        pass
        
    def __str__(self):
        res = "\t" * self.parentCount() + "Assignment"
        res += "\n" + str(self.lvalue)
        res += "\n" + str(self.rvalue)
        return res

class Negation(Node):
    def __init__(self, child):
        super().__init__()
        self.child = child
        self.child.parent = self

    def eval(self):
        return not self.child.eval()

    def __str__(self):
        res = "\t" * self.parentCount() + "Negation"
        res += "\n" + str(self.child)
        return res

class Conjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        return self.left.eval() and self.right.eval()

    def __str__(self):
        res = "\t" * self.parentCount() + "Conjunction"
        res += "\n" + str(self.left)
        res += "\n" + str(self.right)
        return res

class Disjunction(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        return self.left.eval() or self.right.eval()

    def __str__(self):
        res = "\t" * self.parentCount() + "Disjunction"
        res += "\n" + str(self.left)
        res += "\n" + str(self.right)
        return res
    
class MaterialImplication(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        return (not self.left.eval()) or self.right.eval()

    def __str__(self):
        res = "\t" * self.parentCount() + "Material Implication"
        res += "\n" + str(self.left)
        res += "\n" + str(self.right)
        return res
    
class Biconditional(Node):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
        self.left.parent = self
        self.right.parent = self

    def eval(self):
        return (((not self.left.eval()) or self.right.eval()) and
                ((not self.right.eval()) or self.left.eval()))

    def __str__(self):
        res = "\t" * self.parentCount() + "Biconditional"
        res += "\n" + str(self.left)
        res += "\n" + str(self.right)
        return res
    
class AST_True(Node):
    def __init__(self):
        super().__init__()
        self.value = True

    def eval(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "True"
        return res

class AST_False(Node):
    def __init__(self):
        super().__init__()
        self.value = False

    def eval(self):
        return self.value

    def __str__(self):
        res = "\t" * self.parentCount() + "False"
        return res

class Variable(Node):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def eval(self):
        if self.name in names:
            return names[self.name]
        else:
            print("Undefined name '%s'" % self.name)
            return True

    def __str__(self):
        res = "\t" * self.parentCount() + "Variable: " + self.name
        if self.name in names:
            res += " : " + str(names[self.name])
        else:
            res += " : " + "True"
        return res

# Tokens

tokens = ('EQUALS',
          'NEGATION',
          'CONJUNCTION',
          'DISJUNCTION',
          'MATERIAL_IMPLICATION',
          'BICONDITIONAL',
          'LEFT_PARENTHESIS',
          'RIGHT_PARENTHESIS',
          'TRUE',
          'FALSE',
          'VARIABLE',
          )

t_EQUALS = r'='
t_NEGATION = r'~'
t_CONJUNCTION = r'/\\'
t_DISJUNCTION = r'\\/'
t_MATERIAL_IMPLICATION = r'-->'
t_BICONDITIONAL = r'<-->'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_TRUE = r'T'
t_FALSE = r'F'

def t_VARIABLE(t):
    r'[a-z]\d*'
    return t

# Ignore whitespace
t_ignore = ' \t'

# Count newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Report lexing errors
def t_error(t):
    print("Illegal Character '%s', at %d, %d" %
          (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)

# Build lexer
import ply.lex as lex
lexer = lex.lex(debug = True)

def tokenize(inp):
    lexer.input(inp)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Parsing rules

names = {}

precedence = (('right', 'BICONDITIONAL'),
              ('right', 'MATERIAL_IMPLICATION'),
              ('right', 'DISJUNCTION'),
              ('right', 'CONJUNCTION'),
              ('right', 'NEGATION'),
)

def p_expr(p):
    '''expr : stat
            | prop'''
    p[0] = p[1]

def p_stat_assign_true(p):
    'stat : VARIABLE EQUALS TRUE'
    names[p[1]] = True
    print(names)

def p_stat_assign_false(p):
    'stat : VARIABLE EQUALS FALSE'
    names[p[1]] = False
    print(names)

def p_prop_negation(p):
    'prop : NEGATION prop'
    p[0] = Negation(p[2])

def p_prop_conjunction(p):
    'prop : prop CONJUNCTION prop'
    p[0] = Conjunction(p[1], p[3])

def p_prop_disjunction(p):
    'prop : prop DISJUNCTION prop'
    p[0] = Disjunction(p[1], p[3])

def p_prop_materialImplication(p):
    'prop : prop MATERIAL_IMPLICATION prop'
    p[0] = MaterialImplication(p[1], p[3])

def p_prop_biconditional(p):
    'prop : prop BICONDITIONAL prop'
    p[0] = Biconditional(p[1], p[3])

def p_prop_true(p):
    'prop : TRUE'
    p[0] = AST_True()

def p_prop_false(p):
    'prop : FALSE'
    p[0] = AST_False()

def p_prop_parenthetical(p):
    'prop : LEFT_PARENTHESIS prop RIGHT_PARENTHESIS'
    p[0] = p[2]

def p_prop_variable(p):
    'prop : VARIABLE'
    p[0] = Variable(p[1])

def p_error(p):
    print("Syntax error at '%s' (%d, %d)" % (p.value, p.lineno, p.lexpos))
    sys.exit()

import ply.yacc as yacc
parser = yacc.yacc(debug = True)

def parse(inp):
    result = parser.parse(inp, debug = 1)
    return result
        
def main():
    while True:
        inp = input("Enter a proposition: ")
        #tokenize(inp)
        result = parse(inp)
        print(result)
        if result is not None:
            print("Evaluation:", result.eval())

if __name__ == "__main__":
    main()
