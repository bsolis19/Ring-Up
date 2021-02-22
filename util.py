
seps = ['(', ')', '+', '-', '*', '/']
buff = list()

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
                    return ''
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
            #partial is a variable
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
    if input_str.startswith('.'):
        return input_str[1:].isdigit()

    else:
        temp = input_str.split('.')
        if len(temp) > 2:
            return False
        flag = True
        for c in temp:
            if not c.isdigit():
                flag = False
                break

        return flag

def parse(tokens):
    def parseExp(index):
        # if token is var
            # return instance of Var and index + 1

        # if token is num
            #return instance of Num and index + 1

        # token must be first in new expression

    (parsed_exp, next_index) = parseExp(0)
    return parsed_exp



