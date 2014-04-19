# -----------------------------------------------------------------------------
# Calculator with English words and numbers.
# Oscar Rubio Pons, oscar.rubio.pons@gmail.com
# 16 Sept 2013, Hamburg, Germany
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input
#Import words to numbers
import w2n

# Make a calculator function

def make_calculator():
    import ply.lex as lex
    import ply.yacc as yacc

    # ------- Internal calculator state

    variables = {  }       # Dictionary of stored variables

    # ------- Calculator tokenizing rules

    tokens = (
        'NAME', 'NUMBER','PLUS', 'MINUS', 'DIVIDE', 'TIMES', 'one', 'two', 'three',
    )

    literals = ['=','+','-','*','/', '(',')']

    t_ignore = " \t"

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'
    t_one = 'one'
    t_two = 'two'
    t_three = 'three'

#expression
#
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
    # Build the lexer
    lexer = lex.lex()

    # ------- Calculator parsing rules

    precedence = (
        ('left','+','-'),
        ('left','*','/'),
        ('right','UMINUS'),
    )

# Alternative to the expresion can be +,- * and /
    def p_expression_binop(p):
        '''expression : NUMBER '+' NUMBER
                      | NUMBER PLUS NUMBER 
                      | NUMBER '-' NUMBER 
                      | NUMBER '*' NUMBER 
                      | NUMBER '/' NUMBER 
                      | TXTNUMBER PLUS TXTNUMBER 
                      | TXTNUMBER DIVIDE  TXTNUMBER 
                      | TXTNUMBER '/' TXTNUMBER'''
        if p[2] ==   '+'  : p[0] = p[1] + p[3]
        elif p[2] == PLUS: p[0] = p[1] + p[3]
        elif p[2] == PLUS_text: p[0] = p[1] + p[3]
        elif p[2] == '-': p[0] = p[1] - p[3]
        elif p[2] == '*': p[0] = p[1] * p[3]
        elif p[2] == '/': p[0] = p[1] / p[3]

    def p_binary_operators(p):
        '''expression : expression PLUS expression
                      | expression MINUS expression 
                      | expression TIMES expression
                      | expression  DIVIDE expression'''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]


    def p_expression_uminus(p):
        "expression : '-' expression %prec UMINUS"
        p[0] = -p[2]

    def p_expression_group(p):
        "expression : '(' expression ')'"
        p[0] = p[2]

    def p_expression_number(p):
        '''expression : NUMBER
                      | TXTNUMBER
        '''
        p[0] = p[1]

    def p_expression_name(p):
        "expression : NAME"
        try:
            p[0] = variables[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0

    def p_error(p):
        if p:
            print("ERROR at '%s'" % p.value)
        else:
            print("ERROR at EOF")

    def p_txtnumber(p):
        '''TXTNUMBER : one
         | two
         | three
        '''
        p[0] = w2n.w2n(p[1])

#Check the complete implementation for Words to numbers
#http://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers-python for a complete implementation

    def w2n(s):
        if s == 'one': return 1
        elif s == 'two': return 2
        elif s == 'three': return 3
        assert(False)


    # Build the parser
    parser = yacc.yacc()

    # ------- Input function 
    
    def input(text):
        result = parser.parse(text,lexer=lexer)
        return result

    return input

# Make a calculator object and use it
calc = make_calculator()

while True:
    try:
        s = raw_input(" Enter your input, Calc: > ")
    except EOFError:
        break
    r = calc(s)
    if r:
        print(r)

    
