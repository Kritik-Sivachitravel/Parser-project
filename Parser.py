import ASTNodeDefs as AST
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position]
        self.tokens = []
    
    # Move to the next position in the code increment by one.
    def advance(self):
        self.position += 1
        if self.position >= len(self.code):
            self.current_char = None
        else:
            self.current_char = self.code[self.position]

    # If the current char is whitespace, move ahead.
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    # Tokenize the identifier.
    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return ('IDENTIFIER', result)
    

    # Tokenize numbers, including float handling
    def number(self):
        result = ''
        is_float = False
        # TODO: Update this code to handle floating-point numbers 
    
        # To handle floating-point numbers, I am checking for '.' in the current character to determine a float or an integer here
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                is_float = True
            result += self.current_char
            self.advance()
        if is_float:
            return ('FNUMBER', float(result))
        else:
            return ('NUMBER', int(result))
        #Satisfied all todo requirements

    def token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalpha():
                ident = self.identifier()
                if ident[1] == 'if':
                    return ('IF', 'if')
                elif ident[1] == 'else':
                    return ('ELSE', 'else')
                elif ident[1] == 'while':
                    return ('WHILE', 'while')
                elif ident[1] == 'int':
                    return ('INT', 'int')
                elif ident[1] == 'float':
                    return ('FLOAT', 'float')
                return ident  # Generic identifier
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()
            if self.current_char == '+':
                self.advance()
                return ('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return ('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return ('MULTIPLY', '*')
            if self.current_char == '/':
                self.advance()
                return ('DIVIDE', '/')
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('EQ', '==')
                return ('EQUALS', '=')
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return ('NEQ', '!=')
            if self.current_char == '<':
                self.advance()
                return ('LESS', '<')
            if self.current_char == '>':
                self.advance()
                return ('GREATER', '>')
            if self.current_char == '(':
                self.advance()
                return ('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return ('RPAREN', ')')
            if self.current_char == ',':
                self.advance()
                return ('COMMA', ',')
            if self.current_char == ':':
                self.advance()
                return ('COLON', ':')
            # TODO: Implement handling for '{' and '}' tokens here (see `tokens.txt` for exact names)
            if self.current_char == '{':
                self.advance()
                return ('LBRACE', '{')
            if self.current_char == '}':
                self.advance()
                return ('RBRACE', '}')
            if self.current_char == '\n':
                self.advance()
                continue

            raise ValueError(f"Illegal character at position {self.position}: {self.current_char}")

        return ('EOF', None)

    # Collect all the tokens in a list.
    def tokenize(self):
        while True:
            token = self.token()
            self.tokens.append(token)
            if token[0] == 'EOF':
                break
        return self.tokens



import ASTNodeDefs as AST

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens.pop(0)
        # Use these to track the variables and their scope
        self.symbol_table = {'global': {}}
        self.scope_counter = 0
        self.scope_stack = ['global']
        self.messages = []

    def error(self, message):
        self.messages.append(message)
    
    def advance(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)

    # TODO: Implement logic to enter a new scope, add it to symbol table, and update `scope_stack`
    def enter_scope(self):
        self.scope_counter += 1
        scope_new = f"scope_{self.scope_counter}" #Logic to enter a new scope
        self.symbol_table[scope_new] = {} #Adding to symbol table
        self.scope_stack.append(scope_new) #Updating scope_stack
        pass
        #Satisfied all todo requirements

    # TODO: Implement logic to exit the current scope, removing it from `scope_stack`
    def exit_scope(self):
        self.scope_stack.pop() #Using the pop function to remove the top element from a stack
        pass
        #Satisfied all todo requirements

    # Return the current scope name
    def current_scope(self):
        return self.scope_stack[-1]

    # TODO: Check if a variable is already declared in the current scope; if so, log an error
    def checkVarDeclared(self, identifier):
        scope_curr = self.current_scope() #Assigning current scope to a new variable
        if identifier in self.symbol_table[scope_curr]: #Checking if variable is already declared in current scope
            self.error(f"Variable {identifier} has already been declared in the current scope") #Raising an error if variable is already declared
        #Satisfied all todo requirements

    # TODO: Check if a variable is declared in any accessible scope; if not, log an error
    def checkVarUse(self, identifier):
        for i in reversed(self.scope_stack): #Initiating a for loop
            #If a variable was declared in any accessible scope, returns True
            if identifier in self.symbol_table[i]: 
                return True
        #Logs an error otherwise
        self.error(f"Variable {identifier} has not been declared in the current or any enclosing scopes")
        return False
        #Satisfied all todo requirements

    # TODO: Check type mismatch between two entities; log an error if they do not match
    def checkTypeMatch2(self, vType, eType, var, exp):

        # If both are int/float and are not equal to each other, it is a type mismatch
        if vType and eType in ('int','float'): 
            if vType != eType:
                self.error(f"Type Mismatch between {vType} and {eType}") #Logs an error upon type mismatch
        #Satisfied all todo requirements

    # TODO: Implement logic to add a variable to the current scope in `symbol_table`
    def add_variable(self, name, var_type):
        scope_curr = self.current_scope() #Assigning current scope to a variable
        if name in self.symbol_table[scope_curr]:
            # If it's already declared, we would get a second identical error
            self.error(f"Variable {name} has already been declared in the current scope")
        else:
            self.symbol_table[scope_curr][name] = var_type #Adds the variable to the current scope in 'symbol_table'
        pass
        #Satisfied all todo requirements

    # TODO: Retrieve the variable type from `symbol_table` if it exists
    def get_variable_type(self, name):
        for i in reversed(self.scope_stack):
            if name in self.symbol_table[i]: #Checking if variable type is in 'symbol_table'
                return self.symbol_table[i][name] #Retrieving it if it exists
        return None
        #Satisfied all todo requirements

    def parse(self):
        return self.program()

    def program(self):
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.statement())
        return AST.Block(statements)

    # TODO: Modify the `statement` function to dispatch to declare statement
    def statement(self):
        if self.current_token[0] in ['INT', 'FLOAT']:
            return self.decl_stmt()
        #Modification done to dispatch to declare statement
        if self.current_token[0] == 'IDENTIFIER':
            if self.peek() == 'EQUALS':
                return self.assign_stmt()
            elif self.peek() == 'LPAREN':
                return self.function_call()
            else:
                raise ValueError(f"Unexpected token after identifier: {self.current_token}")
        elif self.current_token[0] == 'IF':
            return self.if_stmt()
        elif self.current_token[0] == 'WHILE':
            return self.while_stmt()
        else:
            raise ValueError(f"Unexpected token: {self.current_token}")
        #Satisfied all todo requirements

    # TODO: Implement the declaration statement and handle adding the variable to the symbol table
    def decl_stmt(self):
        var_type = self.current_token[1]
        self.advance() # skip type
        var_name = self.current_token[1]
        self.advance() # skip identifier
        # Check if already declared
        scope_curr = self.current_scope()
        var_decl = var_name in self.symbol_table[scope_curr]
        self.checkVarDeclared(var_name)
        # Only add variable if it wasn't already declared
        # This prevents a second identical error message
        if not var_decl:
            self.add_variable(var_name, var_type)
        self.expect('EQUALS')
        expression = self.expression()
        # Check type mismatch after expression
        expr_type = expression.value_type
        # If both are int/float and are not equal to each other, it is a type mismatch
        if var_type and expr_type in ('int','float'):
            if var_type != expr_type:
                self.error(f"Type Mismatch between {var_type} and {expr_type}")
        return AST.Declaration(var_type, var_name, expression)
        #Satisfied all todo requirements

    # TODO: Parse assignment statements, handle type checking
    def assign_stmt(self):
        var_name = self.current_token[1] #Extracting name of the variable
        self.checkVarUse(var_name)
        self.advance()
        self.expect('EQUALS')
        expression = self.expression() #Parsing the expression to be assigned
        var_type = self.get_variable_type(var_name)
        expr_type = expression.value_type
        # If both are int/float and are not equal to each other, it is a type mismatch
        if var_type and expr_type in ('int','float'):
            if var_type != expr_type:
                self.error(f"Type Mismatch between {var_type} and {expr_type}")
        return AST.Assignment(var_name, expression)
        #Satisfied all todo requirements

    # TODO: Implement the logic to parse the if condition and blocks of code
    def if_stmt(self):
        self.advance() # skip IF
        condition = self.boolean_expression() #Parsing the boolean condition expression
        self.expect('LBRACE') #Expect the '{' that starts the 'if' statement
        self.enter_scope() #Entering a new scope for the 'if' statement
        then_block = self.block() #Parsing all statements inside the 'if' statement
        self.exit_scope()
        self.expect('RBRACE') #Expect the '}' that ends the 'if' statement
        else_block = None
        if self.current_token[0] == 'ELSE':
            self.advance()
            self.expect('LBRACE') #Expect the '{' that starts the 'else' statement
            self.enter_scope() #Entering a new scope for the 'else' statement
            else_block = self.block() #Parsing all statements inside the 'else' statement
            self.exit_scope()
            self.expect('RBRACE') #Expect the '}' that ends the 'else' statement
        return AST.IfStatement(condition, then_block, else_block)
        #Satisfied all todo requirements

    # TODO: Implement the logic to parse while loops with a condition and a block of statements
    def while_stmt(self):
        self.advance() # skip WHILE
        condition = self.boolean_expression()
        self.expect('LBRACE') #Expect the '{' that starts the 'while' statement
        self.enter_scope() #Parsing all statements inside the 'while' statement
        block = self.block()
        self.exit_scope()
        self.expect('RBRACE') #Expect the '}' that ends the 'while' statement
        return AST.WhileStatement(condition, block)
        #Satisfied all todo requirements

    # TODO: Implement logic to capture multiple statements as part of a block
    def block(self):
        statements = []
        while self.current_token[0] not in ['RBRACE', 'EOF']:
            if self.current_token[0] in ['INT','FLOAT','IDENTIFIER','IF','WHILE']:
                statements.append(self.statement())
            else:
                break
        return AST.Block(statements)
        #Satisfied all todo requirements


    # For the expression and term functions, if there's a mismatch, I don't unify result_type to float automatically.
    # I just leave the type as int if that was original, so next operation may give the opposite mismatch.
    # TODO: Implement logic to parse binary operations (e.g., addition, subtraction) with correct precedence and type checking
    def expression(self):
        left = self.term()
        while self.current_token[0] in ['PLUS', 'MINUS']:
            op = self.current_token[0]
            self.advance()
            right = self.term()
            # Checking for a mismatch before changing types
            len_of_msgs = len(self.messages)
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            # If mismatch happened now, I do not unify the types to float
            # I just pick a type that doesn't prevent future mismatches
            # Choosing the left.value_type regardless of a mismatch
            mismatch = (len(self.messages) > len_of_msgs)
            if mismatch:
                # If there's a mismatch, then I do not unify to float and just keep left.value_type so next operation can differ
                result_type = left.value_type
            else:
                # If no mismatch, normal logic
                if left.value_type == 'float' or right.value_type == 'float':
                    result_type = 'float'
                else:
                    result_type = left.value_type
            left = AST.BinaryOperation(left, op, right, result_type)
        return left
        #Satisfied all todo requirements

    # TODO: Implement parsing for boolean expressions and check for type compatibility
    def boolean_expression(self):
        left = self.expression()
        if self.current_token[0] in ['EQ', 'NEQ', 'LESS', 'GREATER']:
            op = self.current_token[0]
            self.advance()
            right = self.expression()
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            return AST.BooleanExpression(left, op, right)
        return left
        #Satisfied all todo requirements

    # TODO: Implement parsing for multiplication and division and check for type compatibility
    def term(self):
        left = self.factor() #Parsing the initial factor as the left operand of the term
        while self.current_token[0] in ['MULTIPLY', 'DIVIDE']:
            op = self.current_token[0]
            self.advance()
            right = self.factor()
            len_of_msgs = len(self.messages)
            self.checkTypeMatch2(left.value_type, right.value_type, left, right)
            mismatch = (len(self.messages) > len_of_msgs)
            if mismatch:
                #If there's a mismatch, I keep the original type of the left operand
                result_type = left.value_type
            else:
                #If there's no mismatch, I determine the result type based on operands
                if left.value_type == 'float' or right.value_type == 'float':
                    result_type = 'float'
                else:
                    result_type = left.value_type
            left = AST.BinaryOperation(left, op, right, result_type)
        return left #Returning the fully parsed term node
        #Satisfied all todo requirements

    def factor(self):
        if self.current_token[0] == 'NUMBER':
            num = self.current_token[1]
            self.advance()
            return AST.Factor(num, 'int')
        elif self.current_token[0] == 'FNUMBER':
            num = self.current_token[1]
            self.advance()
            return AST.Factor(num, 'float')
        elif self.current_token[0] == 'IDENTIFIER':
            var_name = self.current_token[1]
            self.checkVarUse(var_name)
            self.advance()
            var_type = self.get_variable_type(var_name)
            return AST.Factor(var_name, var_type)
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        else:
            raise ValueError(f"Unexpected token in factor: {self.current_token}")

    def function_call(self):
        func_name = self.current_token[1]
        self.advance()
        self.expect('LPAREN')
        args = self.arg_list()
        self.expect('RPAREN')
        return AST.FunctionCall(func_name, args)

    def arg_list(self):
        args = []
        if self.current_token[0] != 'RPAREN':
            args.append(self.expression())
            while self.current_token[0] == 'COMMA':
                self.advance()
                args.append(self.expression())
        return args

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise ValueError(f"Expected token {token_type}, but got {self.current_token[0]}")

    def peek(self):
        return self.tokens[0][0] if self.tokens else None








