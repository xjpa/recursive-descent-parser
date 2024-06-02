class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token(type={self.type}, value={self.value})"

class LetStatement:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        return (f"{indent_str}LetStatement {{\n"
                f"{indent_str}    identifier: {self.identifier.__str__(indent + 4)},\n"
                f"{indent_str}    value: {self.value.__str__(indent + 4)}\n"
                f"{indent_str}}}")

class IfStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        return (f"{indent_str}IfStatement {{\n"
                f"{indent_str}    condition: {self.condition.__str__(indent + 4)},\n"
                f"{indent_str}    body: {self.body.__str__(indent + 4)}\n"
                f"{indent_str}}}")

class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        return (f"{indent_str}BinaryExpression {{\n"
                f"{indent_str}    left: {self.left.__str__(indent + 4)},\n"
                f"{indent_str}    operator: {self.operator},\n"
                f"{indent_str}    right: {self.right.__str__(indent + 4)}\n"
                f"{indent_str}}}")

class Block:
    def __init__(self, statements):
        self.statements = statements

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        statements_str = ',\n'.join([stmt.__str__(indent + 4) for stmt in self.statements])
        return (f"{indent_str}Block {{\n"
                f"{indent_str}    statements: [\n{statements_str}\n{indent_str}    ]\n"
                f"{indent_str}}}")

class Assignment:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        return (f"{indent_str}Assignment {{\n"
                f"{indent_str}    identifier: {self.identifier.__str__(indent + 4)},\n"
                f"{indent_str}    value: {self.value.__str__(indent + 4)}\n"
                f"{indent_str}}}")

class Identifier:
    def __init__(self, name):
        self.name = name

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}Identifier {{ name: {self.name} }}"

class Number:
    def __init__(self, value):
        self.value = value

    def __str__(self, indent=0):
        indent_str = ' ' * indent
        return f"{indent_str}Number {{ value: {self.value} }}"

tokens = [
    Token('KEYWORD', 'let'),
    Token('IDENTIFIER', 'x'),
    Token('OPERATOR', '='),
    Token('NUMBER', '5'),
    Token('DELIMITER', ';'),
    Token('KEYWORD', 'if'),
    Token('DELIMITER', '('),
    Token('IDENTIFIER', 'x'),
    Token('OPERATOR', '>'),
    Token('NUMBER', '3'),
    Token('DELIMITER', ')'),
    Token('DELIMITER', '{'),
    Token('IDENTIFIER', 'x'),
    Token('OPERATOR', '='),
    Token('IDENTIFIER', 'x'),
    Token('OPERATOR', '+'),
    Token('NUMBER', '1'),
    Token('DELIMITER', ';'),
    Token('DELIMITER', '}')
]

current_token_index = 0

def lookahead():
    if current_token_index < len(tokens):
        return tokens[current_token_index]
    return Token('EOF', '')

def match(expected_type, expected_value=None):
    global current_token_index
    token = lookahead()
    if token.type == expected_type and (expected_value is None or token.value == expected_value):
        current_token_index += 1
        return token
    raise SyntaxError(f"Expected {expected_type} {expected_value if expected_value else ''}, got {token.type} {token.value}")

def match_operator():
    global current_token_index
    token = lookahead()
    if token.type == 'OPERATOR':
        current_token_index += 1
        return token.value
    raise SyntaxError(f"Expected OPERATOR, got {token.type}")

def parse_number():
    token = match('NUMBER')
    return Number(int(token.value))

def parse_identifier():
    token = match('IDENTIFIER')
    return Identifier(token.value)

def parse_if_statement():
    match('KEYWORD', 'if')
    match('DELIMITER', '(')
    condition = parse_condition()
    match('DELIMITER', ')')
    match('DELIMITER', '{')
    body = parse_block()
    match('DELIMITER', '}')
    return IfStatement(condition, body)

def parse_let_statement():
    match('KEYWORD', 'let')
    identifier = parse_identifier()
    match('OPERATOR', '=')
    value = parse_expression()
    match('DELIMITER', ';')
    return LetStatement(identifier, value)

def parse_condition():
    expr = parse_expression()
    return expr

def parse_expression():
    left = parse_term()
    while lookahead().type == 'OPERATOR':
        operator = match_operator()
        right = parse_term()
        left = BinaryExpression(left, operator, right)
    return left

def parse_term():
    token = lookahead()
    if token.type == 'NUMBER':
        return parse_number()
    elif token.type == 'IDENTIFIER':
        return parse_identifier()
    else:
        raise SyntaxError(f"Unexpected token: {token.type}")

def parse_block():
    statements = []
    while lookahead().type != 'DELIMITER' or lookahead().value != '}':
        statements.append(parse_statement())
    return Block(statements)

def parse_statement():
    token = lookahead()
    if token.type == 'KEYWORD' and token.value == 'let':
        return parse_let_statement()
    elif token.type == 'KEYWORD' and token.value == 'if':
        return parse_if_statement()
    elif token.type == 'IDENTIFIER':
        return parse_assignment()
    else:
        raise SyntaxError(f"Unexpected token: {token.type}")

def parse_assignment():
    identifier = parse_identifier()
    match('OPERATOR', '=')
    expr = parse_expression()
    match('DELIMITER', ';')
    return Assignment(identifier, expr)

def parse_program():
    statements = []
    while lookahead().type != 'EOF':
        statements.append(parse_statement())
    return Block(statements)

ast = parse_program()
print(ast.__str__())
