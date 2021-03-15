import math
import ply.lex as lex
import ply.yacc as yacc

tokens = (
        'NAME',
        'NUMBER_INT',
        'NUMBER_DOUBLE',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'COMMA',
        'LPAREN',
        'RPAREN',
    )

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_COMMA = r','
t_ignore = ' \t'

VALUE_ERR_T = "invalid value: '%s'"
SYNTAX_ERR_T = "invalid character: '%s'"


def t_NUMBER_DOUBLE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_NUMBER_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_error(t):
    # Handle illegal character
    raise SyntaxError(SYNTAX_ERR_T % t.value[0])


precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

variables = {
        'pi': math.pi,
        'e': math.e,
    }

start = 'statement'


def p_statement_expression(t):
    '''
    statement : expression
    '''
    global value
    value = t[1]


def p_expression_binop(t):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression DIVIDE expression
               | expression TIMES expression
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        if t[3] == 0:
            raise ValueError('division by zero invalid')
        t[0] = t[1] / t[3]


def p_expression_uminus(t):
    '''
    expression : MINUS expression %prec UMINUS
    '''
    t[0] = -t[2]


def p_expression_group(t):
    '''
    expression : LPAREN expression RPAREN
    '''
    t[0] = t[2]


def p_expressions(t):
    '''
    expressions : expression COMMA expression
               | expression
               |
    '''
    if len(t) == 0:
        t[0] = None
        return
    t[0] = [t[1]] if len(t) == 2 else t[1] + [t[3]]


def p_expression_function(t):
    '''
    expression : NAME LPAREN expressions RPAREN
    '''
    if t[1] == 'sin':
        if len(t[3]) == 1:
            t[0] = math.sin(float(t[3][0]))
            return
        else:
            # Handle missing/too many function arg
            raise SyntaxError(SYNTAX_ERR_T % t[3])
    else:
        # Handle undefined function
        raise ValueError(VALUE_ERR_T % t[1])


def p_expression_number(t):
    '''
    expression : NUMBER_INT
               | NUMBER_DOUBLE
    '''
    t[0] = t[1]


def p_expression_name(t):
    '''
    expression : NAME
    '''
    t[0] = variables[t[1]]


def p_error(t):
    # Handle syntax error
    raise SyntaxError(SYNTAX_ERR_T % t[0])


lexer = lex.lex()
parser = yacc.yacc(debug=0, write_tables=0)

# use value for debugging
value = None
parse = parser.parse
