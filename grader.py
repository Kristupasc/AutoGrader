import inspect
import ast
import sys
from io import StringIO

from ast_visitor import LoopAndRecursionVisitor


class Grader:
    """
    This class is used to grade a student's code.
    """
    def __init__(self, func, output=None):
        """
        Initialize the grader with a function and expected output. The function can either be an actual function or
        a string with the source code.
        """
        self.initialized = False
        if isinstance(func, str):
            try:
                parsed_code = ast.parse(func)
                self.func = compile(parsed_code, '<string>', 'exec')
                self.source = func
                # TODO: Cleaner way to do this
                # Redirect stdout to suppress print statements
                original_stdout = sys.stdout
                sys.stdout = StringIO()
                try:
                    exec(self.func, globals())
                finally:
                    sys.stdout = original_stdout
                # Dynamically find the function in the global namespace
                self.func = globals()[parsed_code.body[0].name]
            except Exception as e:
                print(f"error in code: {e}")
                self.error = e
                return
        else:
            self.func = func
            self.source = inspect.getsource(func)
        self.students = []
        self.tree = ast.parse(self.source)
        self.visitor = LoopAndRecursionVisitor(self.func, self.source)
        self.output = output
        self.visitor.visit(self.tree)
        self.initialized = True

    def set_output(self, output):
        self.output = output

    def begin_output_analysis(self):
        """
        Begin the output analysis of the function. This works if the output is set.
        """
        analysis = self.check_outputs()
        if analysis[0]:
            print("Output analysis passed!")
        else:
            print("Output analysis failed on input of " + str(analysis[1][0]))
            print("Actual Result: " + str(analysis[1][1]))
        return analysis[0]

    def includes_if(self):
        return len(self.visitor.visits['if']) > 0

    def get_ifs(self):
        return self.visitor.visits['if']

    def includes_for(self):
        return len(self.visitor.visits['for']) > 0

    def includes_nested_loop(self):
        return len(self.visitor.visits['for']) > 1 or len(self.visitor.visits['while']) > 1 or (
                    len(self.visitor.visits['for']) > 0 and len(self.visitor.visits['while']) > 0)

    def includes_while(self):
        return len(self.visitor.visits['while']) > 0

    def includes_return(self):
        return len(self.visitor.visits['return']) > 0

    def includes_break(self):
        return len(self.visitor.visits['break']) > 0

    def includes_continue(self):
        return len(self.visitor.visits['continue']) > 0

    def includes_recursion(self):
        return len(self.visitor.visits['recursion']) > 0

    def inclues_else(self):
        return len(self.visitor.visits['else']) > 0

    def check_outputs(self):
        """
        Check an array of outputs of the function against the expected outputs.
        """
        for test_case in self.output:
            try:
                *args, expected = test_case  # Unpack all but the last element as arguments
                # Redirect stdout to suppress print statements
                original_stdout = sys.stdout
                sys.stdout = StringIO()
                try:
                    result = self.func(*args)  # Convert tuple to list before passing to the function
                finally:
                    sys.stdout = original_stdout
                if result != expected:
                    return False, [test_case, result]
            except Exception as e:
                return False, [test_case, e]
        return True, []

    def check_single_output(self, args, expected):
        """
        Check a single output of the function against the expected output.
        """
        try:
            # TODO: Cleaner way to do this
            original_stdout = sys.stdout
            sys.stdout = StringIO()
            try:
                result = self.func(*args)  # Convert tuple to list before passing to the function
            finally:
                sys.stdout = original_stdout
            if result != expected:
                return False
        except Exception as e:
            return False
        return True

    def statement_includes(self, node_type, statement, body=None):
        """
        Check if a statement is included in the body of a node.
        node_type: The type of node to check for. ("if", "for", etc.)
        statement: The statement to check for. ("x > 5", "isinstance", etc.)
        body: The body of the node to check in. This is optional, and it is used if we know exactly which body to check.
        """
        if not body:
            try:
                for node in self.visitor.visits[node_type]:
                    if statement in ast.get_source_segment(self.source, node.test):
                        return True
            except KeyError:
                print("ERROR: Node type of " + str(node_type) + " not found. The type can be one of " + str(
                    self.visitor.visits.keys()))
                print("Automatically returning False....")
                return False
            return False
        else:
            try:
                # iterate through the nodes in the body
                for b in body:
                    if statement in ast.get_source_segment(self.source, b.test):
                        return True
                return False
            except KeyError:
                print("ERROR: Node type of " + str(node_type) + " not found. The type can be one of " + str(
                    self.visitor.visits.keys()))
                print("Automatically returning False....")
                return False

    def body_includes(self, node_type, statement, body=None):
        """
        Check if a statement is included in the body of a node. The same as for statement_includes, but for the body.
        """
        if not body:
            bodies = []
            try:
                for node in self.visitor.visits[node_type]:
                    for b in node.body:
                        if statement in ast.get_source_segment(self.source, b):
                            bodies.append(b)
                if len(bodies) > 0:
                    return True, bodies
                return False, []
            except KeyError:
                print("ERROR: Node type of " + str(node_type) + " not found. The type can be one of " + str(
                    self.visitor.visits.keys()))
                print("Automatically returning False....")
                return False, []
        else:
            try:
                # iterate through the nodes in the body
                for b in body:
                    if statement in ast.get_source_segment(self.source, b):
                        return True
                return False
            except KeyError:
                print("ERROR: Node type of " + str(node_type) + " not found. The type can be one of " + str(
                    self.visitor.visits.keys()))
                print("Automatically returning False....")
                return False

    def convert_body_to_string(self, body):
        return ast.get_source_segment(self.source, body)

    def nested_body_includes(self, node_type, statement):
        """
        The same as body_includes, but for nested bodies.
        """
        try:
            for node in self.visitor.visits[node_type]:
                for body in node.body:
                    if body in self.visitor.visits[node_type]:
                        # check if the statement is not commented out.
                        for line in ast.get_source_segment(self.source, body).split("\n"):
                            if statement in line and "#" not in line:
                                return True
            return False
        except KeyError:
            print("ERROR: Node type of " + str(node_type) + " not found. The type can be one of " + str(
                self.visitor.visits.keys()))
            print("Automatically returning False....")
            return False

    def run_code_on_input(self, args):
        try:
            return self.func(*args)
        except Exception as e:
            print("Exception caught of type: " + str(e))
            return None

