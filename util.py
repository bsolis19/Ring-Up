
seps = ['(', ')', '+', '-', '*', '/']
buff = list()

def tokenize(input_str):
    tokens = list()
    partial = ''
    c = ''

    def getch():
        for c in input_str:
            yield c

    def getchar():
        input_ = getch()

        if len(buff) > 0:
            c = buff.pop(0)

        else:
            try:
                c = next(input_)
            except StopIteration:
                return ''
        return c

    def ungetch(c):
        buff.append(c)

    while getchar():
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
                    partial = ''
            #partial is a variable
            else:
                if c.isalnum() or c == '_':
                    partial += c
                else:
                    if c in seps:
                        ungetch(c)
                    elif c != ' ' or c != '\t':
                        raise SyntaxError('invalid syntax')
                    tokens.append(partial)
                    partial = ''
        else:
            if c.isalnum() or c == '_':
                partial = c
            elif c in seps:
                tokens.append(c)
            elif c != ' ' and c != '\t':
                raise SyntaxError('invalid syntax')
    return tokens

def isnum(input_str):
    if input_str.startswith('.'):
        return input_str[1:].isdigit()

    else:
        temp = partial.split('.')
        if len(temp) != 2:
            return False

        return temp[0].isdigit() and temp[1].isdigit()




