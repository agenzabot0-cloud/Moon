class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        """Look at the current token without removing it."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type):
        """Ensure token matches expectations and move the pointer forward."""
        token = self.peek()
        if token and token.type == expected_type:
            self.pos += 1
            return token
        
        current_val = token.value if token else "EOF"
        current_type = token.type if token else "EOF"
        line = token.line if token else "Unknown"
        raise SyntaxError(f"Moon Parser Error on line {line}: Expected token type '{expected_type}', but found '{current_type}' with value '{current_val}'")

    def parse(self):
        """Main entry point to parse the whole script."""
        statements = []
        while self.peek() is not None:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.peek()
        
        if token.type == 'DOWNLOAD':
            return self.parse_download()
        elif token.type == 'VOCAL':
            return self.parse_vocal()
        elif token.type == 'BREAK':
            return self.parse_break()
        else:
            raise SyntaxError(f"Moon Parser Error on line {token.line}: Invalid statement starting with '{token.value}'")

    def parse_download(self):
        self.consume('DOWNLOAD')
        module_token = self.consume('ID')
        return {
            "type": "DownloadStatement",
            "module_name": module_token.value
        }

    def parse_vocal(self):
        self.consume('VOCAL')
        var_token = self.consume('ID')
        return {
            "type": "VocalStatement",
            "variable_name": var_token.value
        }

    def parse_break(self):
        self.consume('BREAK')
        self.consume('LPAREN')
        
        arg_token = self.peek()
        if arg_token and arg_token.type == 'STRING':
            self.consume('STRING')
            argument_node = {"type": "StringLiteral", "value": arg_token.value}
        elif arg_token and arg_token.type == 'VAR_REF':
            self.consume('VAR_REF')
            argument_node = {"type": "VariableReference", "value": arg_token.value}
        else:
            line = arg_token.line if arg_token else "EOF"
            val = arg_token.value if arg_token else "EOF"
            raise SyntaxError(f"Moon Parser Error on line {line}: break() requires a text string or a [!variable], but found '{val}'")
            
        self.consume('RPAREN')
        return {
            "type": "BreakStatement",
            "argument": argument_node
        }
