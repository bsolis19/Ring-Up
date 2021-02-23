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
        'LPAREN',
        'RPAREN',
    )
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'*'
t_DIVIDE = r'/'
t_ignore = ' \t'

def t_NUMBER_DOUBLE(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        # Handle value too large
        t.value = 0
        pass
    return t

def t_NUMBER_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        # Handle value too large
        t.value = 0
    return t

def t_error(t):
    # Handle illegal character 't.value[0]'
    t.lexer.skip(1)

precedence = (
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

variable = {
        'pi': math.pi,
        'e': math.e,
    }
start = 'statement'

def p_statement_expression(t):
    '''
    statement : expression
    '''
    print(t[1])

def p_expression_binop(t):
    '''
    expression: expression PLUS expression
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
        t[0] = t[1] / t[3]

def p_expression_uminus(t):
    '''
    expression : MINUS expression %prec UMINUS
    '''
    t[0] = -t[2]

def p_expression_group(t):
    '''
    expression: LPAREN expression RPAREN
    '''
    t[0] = t[2]

def p_expressions(t):
    '''
    expressions: expression COLON expression
               | expression
               |
    '''
    if len(t) == 0:
        t[0] = None
        return
    t[0] = [t[1]] if len(t) == 2 else t[1] + [t[3]]

def p_expression_function(t):
    '''
    expression: NAME LPAREN expressions RPAREN
    '''
    if t[1] == 'sin':
        if len(t[3]) == 1:
            t[0]=math.sin(float(t[3][0]))
        else:
            # Handle missing function arg
            pass
        return
    # Handle undefined function
    t[0] = None

def p_expression_number(t):
    '''
    expression : NUMBER_INT
               | NUMBER_DOUBLE
    '''
    t[0] = t[1]

def p_expression_name(t):
    '''
    expression: NAME
    '''
    try:
        t[0] = variables[t[1]]
    except LookupError:
        # Handle undefined name
        t[0] = None

def p_error(t):
    # Handle syntax error
    pass

lexer = lex.lex()
parser = yacc.yacc(debug=0, write_tables=0)

def tokenize(input_str):
    tokens = list()
    partial = str()
    c = str()

    def getch():
        for c in input_str:
            print('getch: ' + c)
            yield c

    def getchar():
        input_ = getch()
        print('made generator')
        while True:
            if len(buff) > 0:
                c = buff.pop(0)

            else:
                try:
                    c = next(input_)
                except StopIteration:
                    c = ''
            print('getchar: ' + c)
            yield c


    def ungetch(c):

        print('ungetch: ' + c)
        buff.append(c)

    input_ = getchar()
    c = next(input_)
    while c:
        print(c)
        if partial:
            # partial is a number
            if isnum(partial):
                if c.isdigit():
                    partial += c
                else:
                    if c in seps:
                        ungetch(c)
                    elif c != ' ' and c != '\t':
                        raise SyntaxError('invalid syntax')
                    tokens.append(partial)
                    partial = str()
            # partial is a variable
            else:
                if c.isalnum() or c == '_':
                    partial += c
                else:
                    if c in seps:
                        ungetch(c)
                    elif c != ' ' and c != '\t':
                        raise SyntaxError('invalid syntax')
                    tokens.append(partial)
                    partial = str()
        else:
            if c.isalnum() or c == '_':
                partial += c
            elif c in seps:
                tokens.append(c)
            elif c != ' ' and c != '\t':
                raise SyntaxError('invalid syntax')
        try:
            c = next(input_)
        except StopIteration:
            if partial:
                tokens.append(partial)
            break
    return tokens

def isnum(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        pass
    return False

def parse(tokens):
    def parseExp(index):
        # if token is var
            # return instance of Var and index + 1

        # if token is num
            #return instance of Num and index + 1

        # token must be LPAREN in new expression


        (parsed_exp, next_index) = parseExp(0)
    return parsed_exp



