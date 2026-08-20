import re

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, Line:{self.line})"

def lex(source_code):
    # Regex specifications for Moon Script syntax
    token_specs = [
        ('DOWNLOAD',  r'\bdownload\b'),          # 'download' keyword
        ('VOCAL',     r'\bvocal\b'),             # 'vocal' keyword
        ('BREAK',     r'\bbreak\b'),             # 'break' keyword
        ('VAR_REF',   r'\[\![a-zA-Z_]\w*\]'),    # Variable references: [!Greeting]
        ('ID',        r'[a-zA-Z_]\w*'),          # Identifiers (module or variable names)
        ('STRING',    r'"[^"]*"'),               # String literals: "hello world!"
        ('LPAREN',    r'\('),                    # Left parenthesis (
        ('RPAREN',    r'\)'),                    # Right parenthesis )
        ('COMMENT',   r'//.*'),                  # Inline comments // like this
        ('NEWLINE',   r'\n'),                    # Track line numbers
        ('SKIP',      r'[ \t\r]+'),              # Skip spaces and tabs
        ('MISMATCH',  r'.'),                     # Catching any invalid syntax characters
    ]
    
    # Compile the master regular expression block
    master_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
    line_num = 1
    tokens = []

    for match in re.finditer(master_regex, source_code):
        kind = match.lastgroup
        value = match.group()

        if kind == 'SKIP' or kind == 'COMMENT':
            continue
        elif kind == 'NEWLINE':
            line_num += 1
            continue
        elif kind == 'STRING':
            value = value[1:-1]  # Clean off the outer quotes
        elif kind == 'VAR_REF':
            value = value[2:-1]  # Extract only the clean variable name out of [! ]
        elif kind == 'MISMATCH':
            raise SyntaxError(f"Moon Lexer Error: Unexpected character {repr(value)} on line {line_num}")

        tokens.append(Token(kind, value, line_num))
        
    return tokens
