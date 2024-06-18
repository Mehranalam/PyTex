import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def tokenize(expression):
    token_specification = [
        ('NUMBER',    r'\d+(\.\d*)?'),    # Integer or decimal number
        ('IDENT',     r'[A-Za-z]'),       # Identifiers (variables)
        ('OP',        r'[+\-*/^]'),       # Arithmetic operators
        ('FRAC',      r'\\frac'),         # Fraction
        ('LBRACE',    r'\{'),             # Left brace
        ('RBRACE',    r'\}'),             # Right brace
        ('WS',        r'\s+'),            # Whitespace
        ('MISMATCH',  r'.'),              # Any other character
    ]
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, expression):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'WS':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')
        tokens.append(Token(kind, value))
    return tokens

class ASTNode:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

def parse(tokens):
    def parse_expression(index):
        node, index = parse_term(index)
        while index < len(tokens) and tokens[index].type == 'OP' and tokens[index].value in '+-':
            op = tokens[index].value
            index += 1
            right, index = parse_term(index)
            node = ASTNode('OP', op, [node, right])
        return node, index

    def parse_term(index):
        node, index = parse_factor(index)
        while index < len(tokens) and tokens[index].type == 'OP' and tokens[index].value in '*/':
            op = tokens[index].value
            index += 1
            right, index = parse_factor(index)
            node = ASTNode('OP', op, [node, right])
        return node, index

    def parse_factor(index):
        token = tokens[index]
        if token.type == 'NUMBER' or token.type == 'IDENT':
            return ASTNode(token.type, token.value), index + 1
        elif token.type == 'OP' and token.value == '-':
            node, index = parse_factor(index + 1)
            return ASTNode('NEG', None, [node]), index
        elif token.type == 'FRAC':
            index += 1  # Skip \frac
            if tokens[index].type != 'LBRACE':
                raise SyntaxError("Expected '{' after \\frac")
            index += 1
            numerator, index = parse_expression(index)
            if tokens[index].type != 'RBRACE':
                raise SyntaxError("Expected '}' after numerator")
            index += 1
            if tokens[index].type != 'LBRACE':
                raise SyntaxError("Expected '{' before denominator")
            index += 1
            denominator, index = parse_expression(index)
            if tokens[index].type != 'RBRACE':
                raise SyntaxError("Expected '}' after denominator")
            index += 1
            return ASTNode('FRAC', None, [numerator, denominator]), index
        elif token.type == 'LBRACE':
            index += 1
            node, index = parse_expression(index)
            if tokens[index].type != 'RBRACE':
                raise SyntaxError("Expected '}'")
            return node, index + 1
        elif token.type == 'IDENT' and index + 1 < len(tokens) and tokens[index + 1].type == 'OP' and tokens[index + 1].value == '^':
            base = ASTNode(token.type, token.value)
            index += 2  # Skip base and '^'
            exponent, index = parse_factor(index)
            return ASTNode('SUP', None, [base, exponent]), index
        else:
            raise SyntaxError(f"Unexpected token: {token.value}")

    node, index = parse_expression(0)
    if index != len(tokens):
        raise SyntaxError(f"Unexpected token at the end: {tokens[index].value}")
    return node

expression = r"\frac{a+b}{c^2} - 3*d"
tokens = tokenize(expression)
ast = parse(tokens)

def print_ast(node, indent=0):
    print(' ' * indent + f'{node.type}: {node.value}')
    for child in node.children:
        print_ast(child, indent + 2)

print_ast(ast)