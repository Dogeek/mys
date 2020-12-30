from ..parser import ast
from .utils import get_import_from_info
from .utils import CompileError

class DefinitionsVisitor(ast.NodeVisitor):

    def __init__(self, module, fully_qualified_names, imports):
        self.module = module
        self.fully_qualified_names = fully_qualified_names
        self.imports = imports

    def define(self, name):
        self.fully_qualified_names[name] = f'{self.module}.{name}'

    def visit_ImportFrom(self, node):
        module, name, asname = get_import_from_info(node, self.module.split('.'))

        if asname is None:
            asname = name

        self.imports[asname] = (module, name, node)

    def visit_AnnAssign(self, node):
        self.define(node.target.id)

    def visit_ClassDef(self, node):
        self.define(node.name)

    def visit_FunctionDef(self, node):
        self.define(node.name)

class NamesTransformer(ast.NodeVisitor):

    def __init__(self, module, fully_qualified_names):
        self.module = module
        self.fully_qualified_names = fully_qualified_names
        self.in_class = False

    def make_fully_qualified(self, name):
        return self.fully_qualified_names.get(name, name)

    def visit_Name(self, node):
        node.id = self.make_fully_qualified(node.id)

    def visit_ClassDef(self, node):
        self.in_class = True
        node.name = self.make_fully_qualified(node.name)
        self.generic_visit(node)
        self.in_class = False

    def visit_FunctionDef(self, node):
        if not self.in_class:
            node.name = self.make_fully_qualified(node.name)

        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            node.name = self.make_fully_qualified(node.func.id)

        self.generic_visit(node)

def add_imports(module, fully_qualified_names, imports):
    for asname, (import_from, name, node) in imports[module].items():
        if name in fully_qualified_names[import_from]:
            fully_qualified_names[module][asname] = f'{import_from}.{name}'
        elif name in imports[import_from]:
            raise CompileError(f"imported module '{module}' does not exist", node)
        else:
            raise CompileError(
                f"imported module '{import_from}' does not contain '{name}'",
                node)
