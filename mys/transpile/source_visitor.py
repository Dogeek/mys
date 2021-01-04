import textwrap
from pathlib import Path
from ..parser import ast
from .utils import CompileError
from .utils import InternalError
from .utils import TypeVisitor
from .utils import INTEGER_TYPES
from .utils import Context
from .utils import BaseVisitor
from .utils import get_import_from_info
from .utils import indent
from .utils import indent_lines
from .utils import has_docstring
from .utils import mys_to_cpp_type_param
from .utils import BodyCheckVisitor
from .utils import make_name
from .utils import format_parameters
from .utils import format_return_type
from .utils import format_method_name
from .definitions import is_method

def default_value(cpp_type):
    if cpp_type in INTEGER_TYPES:
        return '0'
    elif cpp_type in ['f32', 'f64']:
        return '0.0'
    elif cpp_type == 'Bool':
        return 'Bool(false)'
    elif cpp_type == 'String':
        return 'String()'
    elif cpp_type == 'Char':
        return 'Char()'
    else:
        return 'nullptr'

def create_class_init(class_name, member_names, member_types):
    params = []
    body = []

    for member_name, member_type in zip(member_names, member_types):
        if member_name.startswith('_'):
            value = default_value(member_type)
            body.append(f'this->{make_name(member_name)} = {value};')
        else:
            params.append(f'{member_type} {make_name(member_name)}')
            body.append(f'this->{make_name(member_name)} = {make_name(member_name)};')

    params = ', '.join(params)

    return [
        f'{class_name}::{class_name}({params})',
        '{'
    ] + indent_lines(body) + [
        '}'
    ]

def create_class_del(class_name):
    return [
        f'{class_name}::~{class_name}()',
        '{',
        '}'
    ]

def create_class_str(class_name):
    return [
        f'String {class_name}::__str__() const',
        '{',
        '    std::stringstream ss;',
        '    __format__(ss);',
        '    return String(ss.str().c_str());',
        '}'
    ]

def create_class_format(class_name, member_names):
    members = []

    for name in member_names[:-1]:
        members.append(f'    os << "{name}=" << this->{make_name(name)} << ", ";')

    if member_names:
        name = member_names[-1]
        members.append(f'    os << "{name}=" << this->{make_name(name)};')

    return [
        f'void {class_name}::__format__(std::ostream& os) const',
        '{',
        f'    os << "{class_name}(";'
    ] + members + [
        '    os << ")";',
        '}'
    ]

def create_enum_from_integer(enum):
    code = [
        f'{enum.type} enum_{enum.name}_from_value({enum.type} value)',
        '{',
        '    switch (value) {'
    ]

    for name, value in enum.members:
        code += [
            f'    case {value}:',
            f'        return ({enum.type}){enum.name}::{name};'
        ]

    code += [
        '    default:',
        '        throw ValueError("bad enum value");',
        '    }',
        '}'
    ]

    return code

class SourceVisitor(ast.NodeVisitor):

    def __init__(self,
                 module_levels,
                 module_hpp,
                 filename,
                 skip_tests,
                 namespace,
                 source_lines,
                 definitions,
                 module_definitions):
        self.module_levels = module_levels
        self.source_lines = source_lines
        self.module_hpp = module_hpp
        self.filename = filename
        self.skip_tests = skip_tests
        self.namespace = namespace
        self.forward_declarations = []
        self.add_package_main = False
        self.before_namespace = []
        self.context = Context(module_levels)
        self.definitions = definitions
        self.module_definitions = module_definitions
        self.enums = []

        for name, functions in module_definitions.functions.items():
            self.context.define_function(name, functions)

        for name, trait_definitions in module_definitions.traits.items():
            self.context.define_trait(name, trait_definitions)

        for name, class_definitions in module_definitions.classes.items():
            self.context.define_class(name, class_definitions)

        for enum in module_definitions.enums.values():
            self.enums += self.visit_enum(enum)
            self.enums += create_enum_from_integer(enum)

    def define_parameters(self, args):
        for (name, type_), node in args:
            self.context.define_variable(name, type_, node)

    def visit_AnnAssign(self, node):
        return AnnAssignVisitor(self.source_lines,
                                self.context,
                                self.source_lines).visit(node)

    def visit_Module(self, node):
        body = [
            self.visit(item)
            for item in node.body
        ]

        for name, definitions in self.module_definitions.classes.items():
            body.append(self.visit_class_definition(name, definitions))

        for functions in self.module_definitions.functions.values():
            for function in functions:
                body.append(self.visit_function_definition(function))

        return '\n'.join([
            '// This file was generated by mys. DO NOT EDIT!!!',
            '#include "mys.hpp"',
            f'#include "{self.module_hpp}"'
        ] + self.before_namespace + [
            f'namespace {self.namespace}',
            '{'
        ] + self.forward_declarations
          + self.enums
          + [constant[1] for constant in self.context.constants.values()]
          + body + [
            '}',
            ''
        ] + self.main())

    def main(self):
        if self.add_package_main:
            return [
                'void package_main(int argc, const char *argv[])',
                '{',
                f'    {self.namespace}::main(argc, argv);',
                '}'
            ]
        else:
            return []

    def visit_ImportFrom(self, node):
        module, name, asname = get_import_from_info(node, self.module_levels)
        imported_module = self.definitions.get(module)

        if name.startswith('_'):
            raise CompileError(f"cannot import private definition '{name}'", node)

        if name in imported_module.variables:
            self.context.define_global_variable(
                asname,
                imported_module.variables[name].type,
                node)
        elif name in imported_module.functions:
            self.context.define_function(asname,
                                         imported_module.functions[name])
        elif name in imported_module.classes:
            self.context.define_class(asname,
                                      imported_module.classes[name])
        else:
            raise CompileError(
                f"imported module '{module}' does not contain '{name}'",
                node)

        return ''

    def visit_enum(self, enum):
        members = [
            f"    {name} = {value},"
            for name, value in enum.members
        ]

        self.context.define_enum(enum.name, enum.type)

        return [
            f'enum class {enum.name} : {enum.type} {{'
        ] + members + [
            '};'
        ]

    def visit_ClassDef(self, node):
        return ''

    def visit_class_methods_definition(self,
                                       class_name,
                                       method_names,
                                       methods_definitions):
        body = []

        for method in methods_definitions:
            self.context.push()
            self.context.define_variable('self', class_name, method.node.args.args[0])
            self.define_parameters(method.args)
            method_names.append(method.name)
            method_name = format_method_name(method, class_name)
            parameters = format_parameters(method.args, self.context)
            self.context.return_mys_type = method.returns

            if method_name == class_name:
                body.append(f'{class_name}::{method_name}({parameters})')
            else:
                return_cpp_type = format_return_type(method.returns, self.context)
                body.append(f'{return_cpp_type} {class_name}::{method_name}({parameters})')

            body.append('{')
            body_iter = iter(method.node.body)

            if has_docstring(method.node, self.source_lines):
                next(body_iter)

            for item in body_iter:
                BodyCheckVisitor().visit(item)
                body.append(indent(BodyVisitor(self.source_lines,
                                               self.context,
                                               self.filename).visit(item)))

            body.append('}')
            self.context.pop()

        return '\n'.join(body)

    def visit_class_definition(self, class_name, definitions):
        member_cpp_types = []
        member_names = []
        method_names = []
        body = []

        for member in definitions.members.values():
            if not self.context.is_type_defined(member.type):
                raise CompileError(f"undefined type '{member.type}'",
                                   member.node.annotation)

            member_cpp_types.append(mys_to_cpp_type_param(member.type, self.context))
            member_names.append(member.name)

        for methods in definitions.methods.values():
            body.append(self.visit_class_methods_definition(class_name,
                                                            method_names,
                                                            methods))

        if '__init__' not in method_names:
            body += create_class_init(class_name,
                                      member_names,
                                      member_cpp_types)

        if '__del__' not in method_names:
            body += create_class_del(class_name)

        if '__str__' not in method_names:
            body += create_class_str(class_name)

        body += create_class_format(class_name, member_names)

        return '\n'.join(body)

    def visit_FunctionDef(self, node):
        return ''

    def visit_function_definition(self, function):
        self.context.push()
        self.define_parameters(function.args)
        function_name = function.node.name
        params = format_parameters(function.args, self.context)
        return_cpp_type = format_return_type(function.returns, self.context)
        self.context.return_mys_type = function.returns
        body = []
        body_iter = iter(function.node.body)

        if has_docstring(function.node, self.source_lines):
            next(body_iter)

        for item in body_iter:
            BodyCheckVisitor().visit(item)
            body.append(indent(BodyVisitor(self.source_lines,
                                           self.context,
                                           self.filename).visit(item)))

        if function_name == 'main':
            self.add_package_main = True

            if return_cpp_type != 'void':
                raise CompileError("main() must not return any value", function.node)

            if params not in ['const SharedList<String>& argv', 'void']:
                raise CompileError("main() takes 'argv: [string]' or no arguments",
                                   function.node)

            if params == 'void':
                body = [
                    '    (void)__argc;',
                    '    (void)__argv;'
                ] + body
            else:
                body = ['    auto argv = create_args(__argc, __argv);'] + body

            params = 'int __argc, const char *__argv[]'

        prototype = f'{return_cpp_type} {function_name}({params})'

        if function.is_test:
            if self.skip_tests:
                code = []
            else:
                parts = Path(self.module_hpp).parts
                full_test_name = list(parts[1:-1])
                full_test_name += [parts[-1].split('.')[0]]
                full_test_name += [function_name]
                full_test_name = '::'.join([part for part in full_test_name])
                code = [
                    '#if defined(MYS_TEST)',
                    '',
                    f'static {prototype}',
                    '{'
                ] + body + [
                    '}',
                    f'static Test mys_test_{function_name}("{full_test_name}", '
                    f'{function_name});',
                    '#endif'
                ]
        else:
            self.forward_declarations.append(prototype + ';')
            code = [
                prototype,
                '{'
            ] + body + [
                '}'
            ]

        self.context.pop()

        return '\n'.join(code)

    def visit_Expr(self, node):
        return self.visit(node.value) + ';'

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            if node.value.startswith('mys-embedded-c++-before-namespace'):
                self.before_namespace += [
                    '/* mys-embedded-c++-before-namespace start */',
                    textwrap.dedent(node.value[33:]).strip(),
                    '/* mys-embedded-c++-before-namespace stop */'
                ]
                return ''
            elif node.value.startswith('mys-embedded-c++'):
                return '\n'.join([
                    '/* mys-embedded-c++ start */\n',
                    textwrap.dedent(node.value[17:]).strip(),
                    '\n/* mys-embedded-c++ stop */'])

        raise CompileError("syntax error", node)

    def generic_visit(self, node):
        raise InternalError("unhandled node", node)

class BodyVisitor(BaseVisitor):
    pass

class AnnAssignVisitor(BaseVisitor):

    def visit_AnnAssign(self, node):
        target, mys_type, code = self.visit_ann_assign(node)
        self.context.define_global_variable(target, mys_type, node.target)

        return code
