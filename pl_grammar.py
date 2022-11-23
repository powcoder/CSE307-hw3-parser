https://powcoder.com
代写代考加微信 powcoder
Assignment Project Exam Help
Add WeChat powcoder
# Propositional Logic Grammar

# Tokens

# This tuple contains the names of the tokens that will be used in my language
# for propositional logic. All tokens that will be included in your PLY grammar
# must be included in this tuple. Each token name appears as a string. Using
# all capitals for the token names is done be convention. It is not necessary,
# but it helps distinguish these elements of the grammar.
tokens = ('NEGATION',
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

# Single-line specifications of the tokens as regular expressions. Each
# regular expression pattern is written as a raw Python string (that's what the
# 'r' preceding the string means.
# What you are specifying is the sequence characters read from the character
# stream that comprise the token. Look at the examples below.
# Please read the PLY documentation concerning the order in which these 
# regular expressions are applied to the character stream.
t_NEGATION = r'~'
t_CONJUNCTION = r'/\\'
t_DISJUNCTION = r'\\/'
t_MATERIAL_IMPLICATION = r'-->'
t_BICONDITIONAL = r'<-->'
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_TRUE = r'T'
t_FALSE = r'F'

# Function based definition of VARIABLE tokens.
# As specified, all variables begin with a lower case letter followed by 0 or
# more digits. We return the token itself.
def t_VARIABLE(t):
    r'[a-z]\d*'
    return t

# t_ignore is a special name. The regular expression indicates which characters
# the scanner will skip past while tokenizing.
# Ignore whitespace and tab.
t_ignore = ' \t'

# Another special name. Determines what counts as a newline and what gets done
# when a newline character is read. Here the number of sequential newlines is
# counted, and the count is added to the current lineno, as tracked by the
# lexer. This allows the lexer to determine the line on which each token occurs
# for debugging and error reporting.
# Count newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# A third special name. The body of this function determines what happens when
# the lexer encounters an illegal character. In this case, we print the
# character, its line number, and its column number, then skip it and look at
# the next character.
# Report lexing errors
def t_error(t):
    print("Illegal Character '%s', at %d, %d" %
          (t.value[0], t.lineno, t.lexpos))
    t.lexer.skip(1)

# Build lexer
import ply.lex as lex
lexer = lex.lex(debug = True)

# This function only calls the lexer to tokenize input. You should try something
# like this when you begin writing your grammar to make sure your source inputs
# are being broken up into tokens properly.
def tokenize(inp):
    lexer.input(inp)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Parsing rules

# This will establish the precedence and associativity properties for the
# elements of the grammar. The name of the tuple must be 'precedence'. The
# elements are also tuples. The first element will indicate the associativity
# 'right', 'left', or 'nonassoc'. The rest of the elements of an inner tuple are
# the names of tokens of the grammar. Each inner tuple can contain multiple
# token names separated by commas. All tokens named within the same token have
# the same precedence within the language.
# The inner tuples are ordered from lowest precedence to highest precedence. In
# the precedence tuple below the 'BICONDITIONAL' operator has the lowest 
# precedence in the language, while 'NEGATION' has the highest.
precedence = (('right', 'BICONDITIONAL'),
              ('right', 'MATERIAL_IMPLICATION'),
              ('right', 'DISJUNCTION'),
              ('right', 'CONJUNCTION'),
              ('right', 'NEGATION'),
)

# Production rules are defined using functions as follows.
# The name of the function must begin with "p_". The rest of the name is up to
# you, but it should properly describe the kind of language element that will
# be specified by the production.
# The production itself is given as a string at the top of the function (the
# doc string; a real triple-quoted doc string can be used for multi-line
# productions). The left-hand side of the production is a non-terminal symbol,
# the right-hand side is a pattern made up of nonterminal symbols and terminal
# symbols (token names). You do not need to declare or introduce nonterminal
# symbols anywhere else in the file. The two sides of the production are
# separated by a colon ":" rather than an arrow.

def p_prop_negation(p):
    'prop : NEGATION prop'

def p_prop_conjunction(p):
    'prop : prop CONJUNCTION prop'

def p_prop_disjunction(p):
    'prop : prop DISJUNCTION prop'

def p_prop_materialImplication(p):
    'prop : prop MATERIAL_IMPLICATION prop'

def p_prop_biconditional(p):
    'prop : prop BICONDITIONAL prop'

def p_prop_true(p):
    'prop : TRUE'

def p_prop_false(p):
    'prop : FALSE'

def p_prop_parenthetical(p):
    'prop : LEFT_PARENTHESIS prop RIGHT_PARENTHESIS'

def p_prop_variable(p):
    'prop : VARIABLE'

# A special name for productions that triggers when a parsing error
# occurs.
def p_error(p):
    print("Syntax error at '%s' (%d, %d)" %
          (p.value, p.lineno, p.lexpos))

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc(debug = True)

# A small function to run the parser
def parse(inp):
    result = parser.parse(inp, debug = 1)
    return result
        
# A small main function to collect input from the user, and then 
# run it through the lexer or the parser.
def main():
    while True:
        inp = input("Enter a proposition: ")
        #tokenize(inp)
        result = parse(inp)
        print(result)

if __name__ == "__main__":
    main()
