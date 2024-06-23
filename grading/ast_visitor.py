import ast


class LoopAndRecursionVisitor(ast.NodeVisitor):
    """
    This class is used to visit the AST of a function and store all the nodes and visits.
    """
    def __init__(self, func, source):
        self.func = func
        self.source = source
        self.visits = {"for": [], "while": [], "if": [], "recursion": [], "break": [], "continue": [], "return": [], "else": []}

    def visit_For(self, node):
        # print the node:
        # get the whole source code for the loop:
        self.generic_visit(node)
        self.visits['for'].append(node)

    def visit_While(self, node):
        self.generic_visit(node)
        self.visits['while'].append(node)

    def visit_If(self, node):
        # Handle if statement
        self.generic_visit(node)
        self.visits['if'].append(node)

    def visit_FunctionDef(self, node):
        # Handle function definition
        self.generic_visit(node)

    def visit_Break(self, node):
        # Handle break statement
        self.generic_visit(node)
        self.visits['break'].append(node)

    def visit_Continue(self, node):
        # Handle continue statement
        self.generic_visit(node)
        self.visits['continue'].append(node)

    def visit_Return(self, node):
        # Handle return statement
        self.generic_visit(node)
        self.visits['return'].append(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.func.__name__:
            self.has_recursion = True
            self.visits['recursion'].append(node)

    def visit_Else(self, node):
        self.generic_visit(node)
        self.visits['else'].append(node)

        self.generic_visit(node)

