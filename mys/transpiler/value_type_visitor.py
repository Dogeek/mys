from ..parser import ast
from .generics import generic_class_setup
from .generics import replace_generic_types
from .utils import BUILTIN_CALLS
from .utils import BUILTIN_ERRORS
from .utils import LIST_METHODS
from .utils import NUMBER_TYPES
from .utils import REGEX_METHODS
from .utils import REGEXMATCH_METHODS
from .utils import STRING_METHODS
from .utils import CompileError
from .utils import InternalError
from .utils import is_primitive_type
from .utils import is_snake_case
from .utils import is_string
from .utils import make_integer_literal
from .utils import raise_if_types_differs
from .utils import split_dict_mys_type


def mys_to_value_type(mys_type):
    if isinstance(mys_type, tuple):
        return tuple([mys_to_value_type(item) for item in mys_type])
    elif isinstance(mys_type, list):
        return [mys_to_value_type(mys_type[0])]
    elif isinstance(mys_type, dict):
        key_mys_type, value_mys_type = split_dict_mys_type(mys_type)

        return Dict(mys_to_value_type(key_mys_type),
                    mys_to_value_type(value_mys_type))
    else:
        return mys_type


def format_value_type(value_type):
    if isinstance(value_type, tuple):
        if len(value_type) == 1:
            items = f'{format_value_type(value_type[0])}, '
        else:
            items = ', '.join([format_value_type(item) for item in value_type])

        return f'({items})'
    elif isinstance(value_type, list):
        if len(value_type) == 1:
            return f'[{format_value_type(value_type[0])}]'
        else:
            return '/'.join([format_value_type(item) for item in value_type])
    elif isinstance(value_type, dict):
        raise Exception('not implemented')
    else:
        return value_type


def intersection_of(type_1, type_2, node):
    """Find the intersection of given visited types.

    """

    if type_1 is None:
        if is_primitive_type(type_2):
            raise CompileError(f"'{type_2}' cannot be None", node)
        else:
            return type_2, type_2
    elif type_2 is None:
        if is_primitive_type(type_1):
            raise CompileError(f"'{type_1}' cannot be None", node)
        else:
            return type_1, type_1
    elif type_1 == type_2:
        return type_1, type_2
    elif isinstance(type_1, str) and isinstance(type_2, str):
        raise_if_types_differs(type_1, type_2, node)
    elif isinstance(type_1, tuple) and isinstance(type_2, tuple):
        if len(type_1) != len(type_2):
            return None, None
        else:
            new_type_1 = []
            new_type_2 = []

            for item_type_1, item_type_2 in zip(type_1, type_2):
                item_type_1, item_type_2 = intersection_of(item_type_1,
                                                           item_type_2,
                                                           node)

                if item_type_1 is None or item_type_2 is None:
                    return None, None

                new_type_1.append(item_type_1)
                new_type_2.append(item_type_2)

            return tuple(new_type_1), tuple(new_type_2)
    elif isinstance(type_1, Dict) and isinstance(type_2, Dict):
        key_value_type_1, key_value_type_2 = intersection_of(type_1.key_type,
                                                             type_2.key_type,
                                                             node)
        value_value_type_1, value_value_type_2 = intersection_of(type_1.value_type,
                                                                 type_2.value_type,
                                                                 node)

        return (Dict(key_value_type_1, value_value_type_1),
                Dict(key_value_type_2, value_value_type_2))
    elif isinstance(type_1, str):
        if not isinstance(type_2, list):
            return None, None
        elif type_1 not in type_2:
            type_1 = format_value_type(type_1)
            type_2 = format_value_type(type_2)

            raise CompileError(f"cannot convert '{type_1}' to '{type_2}'", node)
        else:
            return type_1, type_1
    elif isinstance(type_2, str):
        if not isinstance(type_1, list):
            return None, None
        elif type_2 not in type_1:
            type_1 = format_value_type(type_1)
            type_2 = format_value_type(type_2)

            raise CompileError(f"cannot convert '{type_1}' to '{type_2}'", node)
        else:
            return type_2, type_2
    elif isinstance(type_1, list) and isinstance(type_2, list):
        if len(type_1) == 0 and len(type_2) == 0:
            return [], []
        elif len(type_1) == 1 and len(type_2) == 1:
            item_type_1, item_type_2 = intersection_of(type_1[0], type_2[0], node)

            return [item_type_1], [item_type_2]
        elif len(type_1) == 1 and len(type_2) == 0:
            return type_1, type_1
        elif len(type_2) == 1 and len(type_1) == 0:
            return type_2, type_2
        elif len(type_1) == 1 and len(type_2) > 1:
            type_1 = format_value_type(type_1)
            type_2 = format_value_type(type_2)

            raise CompileError(f"cannot convert '{type_1}' to '{type_2}'", node)
        elif len(type_2) == 1 and len(type_1) > 1:
            type_1 = format_value_type(type_1)
            type_2 = format_value_type(type_2)

            raise CompileError(f"cannot convert '{type_1}' to '{type_2}'", node)
        else:
            new_type_1 = []
            new_type_2 = []

            for item_type_1 in type_1:
                for item_type_2 in type_2:
                    if isinstance(item_type_1, str) and isinstance(item_type_2, str):
                        if item_type_1 != item_type_2:
                            continue
                    else:
                        item_type_1, item_type_2 = intersection_of(item_type_1,
                                                                   item_type_2,
                                                                   node)

                        if item_type_1 is None or item_type_2 is None:
                            continue

                    new_type_1.append(item_type_1)
                    new_type_2.append(item_type_2)

            if len(new_type_1) == 0:
                type_1 = format_value_type(type_1)
                type_2 = format_value_type(type_2)

                raise CompileError(f"cannot convert '{type_1}' to '{type_2}'", node)
            elif len(new_type_1) == 1:
                return new_type_1[0], new_type_2[0]
            else:
                return new_type_1, new_type_2
    else:
        raise InternalError("specialize types", node)


def reduce_type(value_type):
    if isinstance(value_type, list):
        if len(value_type) == 0:
            return ['bool']
        elif len(value_type) == 1:
            return [reduce_type(value_type[0])]
        else:
            return reduce_type(value_type[0])
    elif isinstance(value_type, tuple):
        values = []

        for item in value_type:
            values.append(reduce_type(item))

        return tuple(values)
    elif isinstance(value_type, str):
        return value_type
    elif isinstance(value_type, Dict):
        return {reduce_type(value_type.key_type): reduce_type(value_type.value_type)}


class Dict:

    def __init__(self, key_type, value_type):
        self.key_type = key_type
        self.value_type = value_type

    def __str__(self):
        return f'Dict({self.key_type}, {self.value_type})'


class ValueTypeVisitor(ast.NodeVisitor):
    """Find the type of given value.

    """

    def __init__(self, source_lines, context):
        self.source_lines = source_lines
        self.context = context
        self.factor = 1

    def visit_BoolOp(self, _node):
        return 'bool'

    def visit_JoinedStr(self, _node):
        return 'string'

    def visit_BinOp(self, node):
        left_value_type = self.visit(node.left)
        right_value_type = self.visit(node.right)

        if right_value_type == 'string':
            return 'string'
        elif left_value_type == 'string':
            return 'string'
        else:
            return intersection_of(left_value_type, right_value_type, node)[0]

    def visit_Slice(self, node):
        lower = None
        upper = None
        step = None

        if node.lower:
            lower = self.visit(node.lower)

        if node.upper:
            upper = self.visit(node.upper)

        if node.step:
            step = self.visit(node.step)

        return lower, upper, step

    def visit_Subscript(self, node):
        value_type = self.visit(node.value)

        if isinstance(value_type, list):
            value_type = value_type[0]
        elif isinstance(value_type, tuple):
            index = make_integer_literal('i64', node.slice)
            value_type = value_type[int(index)]
        elif isinstance(value_type, Dict):
            value_type = value_type.value_type
        elif value_type == 'string':
            slice_type = self.visit(node.slice)
            if isinstance(slice_type, tuple):
                value_type = 'string'
            else:
                value_type = 'char'
        elif value_type == 'bytes':
            value_type = 'u8'
        else:
            raise Exception('todo')

        return value_type

    def visit_IfExp(self, node):
        return self.visit(node.body)

    def visit_Attribute(self, node):
        name = node.attr

        if isinstance(node.value, ast.Name):
            value = node.value.id

            if self.context.is_enum_defined(value):
                value_type = self.context.make_full_name(value)
            elif self.context.is_local_variable_defined(value):
                value_type = self.context.get_local_variable_type(value)
            elif self.context.is_global_variable_defined(value):
                value_type = self.context.get_global_variable_type(value)
            else:
                raise InternalError("attribute", node)
        else:
            value_type = self.visit(node.value)

        if self.context.is_class_defined(value_type):
            member = self.context.get_class_definitions(value_type).members[name]
            value_type = member.type

        if isinstance(value_type, dict):
            value_type = Dict(list(value_type.keys())[0],
                              list(value_type.values())[0])

        return value_type

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            factor = -1
        else:
            factor = 1

        self.factor *= factor
        value = self.visit(node.operand)
        self.factor *= factor

        return value

    def visit_Constant(self, node):
        if isinstance(node.value, bool):
            return 'bool'
        elif isinstance(node.value, int):
            types = ['i64', 'i32', 'i16', 'i8']

            if self.factor == 1:
                types += ['u64', 'u32', 'u16', 'u8']

            return types
        elif isinstance(node.value, float):
            return ['f64', 'f32']
        elif isinstance(node.value, str):
            if is_string(node, self.source_lines):
                return 'string'
            else:
                return 'char'
        elif isinstance(node.value, bytes):
            return 'bytes'
        elif isinstance(node.value, tuple):
            return 'regex'
        elif node.value is None:
            return None
        else:
            raise Exception('todo')

    def visit_Name(self, node):
        name = node.id

        if name == '__unique_id__':
            return 'i64'
        elif name == '__line__':
            return 'u64'
        elif name == '__name__':
            return 'string'
        elif name == '__file__':
            return 'string'
        elif self.context.is_local_variable_defined(name):
            value_type = self.context.get_local_variable_type(name)

            if isinstance(value_type, dict):
                value_type = Dict(list(value_type.keys())[0],
                                  list(value_type.values())[0])

            return value_type
        elif self.context.is_global_variable_defined(name):
            value_type = self.context.get_global_variable_type(name)

            if isinstance(value_type, dict):
                value_type = Dict(list(value_type.keys())[0],
                                  list(value_type.values())[0])

            return value_type
        else:
            raise CompileError(f"undefined variable '{name}'", node)

    def visit_List(self, node):
        if len(node.elts) == 0:
            return []

        item_type = self.visit(node.elts[0])

        for item in node.elts[1:]:
            item_type, _ = intersection_of(item_type, self.visit(item), item)

        return [item_type]

    def visit_Tuple(self, node):
        return tuple([self.visit(elem) for elem in node.elts])

    def visit_Dict(self, node):
        if len(node.keys) > 0:
            return Dict(self.visit(node.keys[0]), self.visit(node.values[0]))
        else:
            return Dict(None, None)

    def visit_call_function(self, name, _node):
        function = self.context.get_functions(name)[0]

        return mys_to_value_type(function.returns)

    def visit_call_class(self, mys_type, _node):
        return mys_type

    def visit_call_enum(self, mys_type, _node):
        return mys_type

    def visit_call_builtin(self, name, node):
        if name in NUMBER_TYPES:
            return name
        elif name == 'len':
            return 'u64'
        elif name == 'str':
            return 'string'
        elif name == 'char':
            return 'char'
        elif name == 'list':
            value_type = self.visit(node.args[0])

            if isinstance(value_type, Dict):
                return [(value_type.key_type, value_type.value_type)]
            else:
                raise InternalError(f"list('{value_type}') not supported", node)
        elif name in ['min', 'max', 'sum']:
            value_type = self.visit(node.args[0])

            if isinstance(value_type, list):
                return value_type[0]
            else:
                return value_type
        elif name == 'abs':
            return self.visit(node.args[0])
        elif name == 'range':
            return ['i64']
        elif name == 'enumerate':
            # ???
            return [('i64', self.visit(node.args[0]))]
        elif name == 'zip':
            # ???
            return [self.visit(node.args[0])]
        elif name == 'slice':
            # ???
            return [self.visit(node.args[0])]
        elif name == 'reversed':
            # ???
            return [self.visit(node.args[0])]
        elif name == 'input':
            return 'string'
        elif name in BUILTIN_ERRORS:
            return name
        else:
            raise InternalError(f"builtin '{name}' not supported", node)

    def visit_call_method_list(self, name, value_type, node):
        spec = LIST_METHODS.get(name, None)

        if spec is None:
            raise InternalError(f"string method '{name}' not supported", node)

        if spec[1] == '<listtype>':
            return value_type[0]
        else:
            return spec[1]

    def visit_call_method_dict(self, name, value_type, node):
        if name in ['get', 'pop']:
            return value_type.value_type
        elif name == 'keys':
            return [value_type.key_type]
        elif name == 'values':
            return [value_type.value_type]
        else:
            raise InternalError(f"dict method '{name}' not supported", node)

    def visit_call_method_string(self, name, node):
        spec = STRING_METHODS.get(name, None)

        if spec is None:
            raise InternalError(f"string method '{name}' not supported", node)

        return spec[1]

    def visit_call_method_regexmatch(self, name, node):
        spec = REGEXMATCH_METHODS.get(name, None)

        if spec is None:
            raise InternalError(f"regexmatch method '{name}' not supported", node)

        return spec[1]

    def visit_call_method_regex(self, name, node):
        spec = REGEX_METHODS.get(name, None)

        if spec is None:
            raise InternalError(f"regex method '{name}' not supported", node)

        return spec[1]

    def visit_call_method_class(self, name, value_type, node):
        definitions = self.context.get_class_definitions(value_type)

        if name in definitions.methods:
            method = definitions.methods[name][0]
            method = self.context.get_class_definitions(value_type).methods[name][0]
            returns = method.returns
        else:
            raise CompileError(
                f"class '{value_type}' has no method '{name}'",
                node)

        if isinstance(returns, dict):
            returns = Dict(list(returns.keys())[0], list(returns.values())[0])

        return returns

    def visit_call_method_trait(self, name, value_type, _node):
        method = self.context.get_trait_definitions(value_type).methods[name][0]
        returns = method.returns

        if isinstance(returns, dict):
            returns = Dict(list(returns.keys())[0], list(returns.values())[0])

        return returns

    def visit_call_method(self, node):
        name = node.func.attr
        value_type = self.visit(node.func.value)

        if isinstance(value_type, list):
            return self.visit_call_method_list(name, value_type, node.func)
        elif isinstance(value_type, Dict):
            return self.visit_call_method_dict(name, value_type, node.func)
        elif value_type == 'string':
            return self.visit_call_method_string(name, node.func)
        elif value_type == 'regexmatch':
            return self.visit_call_method_regexmatch(name, node.func)
        elif value_type == 'regex':
            return self.visit_call_method_regex(name, node.func)
        elif value_type == 'bytes':
            raise CompileError('bytes method not implemented', node.func)
        elif self.context.is_class_defined(value_type):
            return self.visit_call_method_class(name, value_type, node.func)
        elif self.context.is_trait_defined(value_type):
            return self.visit_call_method_trait(name, value_type, node)
        else:
            raise CompileError("None has no methods", node.func)

    def visit_call_generic_function(self, node):
        name = node.func.value.id
        full_name = self.context.make_full_name(name)
        function = self.context.get_functions(full_name)[0]
        types_slice = node.func.slice
        chosen_types = []

        if isinstance(types_slice, ast.Name):
            chosen_types.append(types_slice.id)
        elif isinstance(types_slice, ast.Tuple):
            for item in types_slice.elts:
                if not isinstance(item, ast.Name):
                    raise CompileError('unsupported generic type', node)

                chosen_types.append(item.id)
        else:
            raise CompileError('invalid specialization of generic function', node)

        return replace_generic_types(function.generic_types,
                                     function.returns,
                                     chosen_types)

    def visit_call_generic_class(self, node):
        _, specialized_full_name = generic_class_setup(node, self.context)

        return specialized_full_name

    def visit_call_generic(self, node):
        if isinstance(node.func.value, ast.Name):
            if self.context.is_class_defined(node.func.value.id):
                return self.visit_call_generic_class(node)
            else:
                return self.visit_call_generic_function(node)
        else:
            raise CompileError("only generic functions and classes are supported",
                               node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            name = node.func.id

            if name in BUILTIN_CALLS:
                return self.visit_call_builtin(name, node)
            else:
                full_name = self.context.make_full_name(name)

                if full_name is None:
                    if is_snake_case(name):
                        raise CompileError(f"undefined function '{name}'", node)
                    else:
                        raise CompileError(f"undefined class/trait/enum '{name}'",
                                           node)
                elif self.context.is_function_defined(full_name):
                    return self.visit_call_function(full_name, node)
                elif self.context.is_class_defined(full_name):
                    return self.visit_call_class(full_name, node)
                elif self.context.is_enum_defined(full_name):
                    return self.visit_call_enum(full_name, node)
        elif isinstance(node.func, ast.Attribute):
            return self.visit_call_method(node)
        elif isinstance(node.func, ast.Lambda):
            raise CompileError('lambda functions are not supported', node.func)
        elif isinstance(node.func, ast.Subscript):
            return self.visit_call_generic(node)
        else:
            raise CompileError("not callable", node.func)

    def visit_define_local_variables(self, node, mys_type):
        if isinstance(node, ast.Name):
            if not node.id.startswith('_'):
                self.context.define_local_variable(node.id, mys_type, node)
        elif isinstance(node, ast.Tuple):
            for item, item_mys_type in zip(node.elts, mys_type):
                self.visit_define_local_variables(item, item_mys_type)
        else:
            raise CompileError("unsupported type", node)

    def visit_ListComp(self, node):
        if len(node.generators) != 1:
            raise CompileError("only one for-loop allowed", node)

        generator = node.generators[0]
        iter_type = self.visit(generator.iter)

        if isinstance(iter_type, list):
            item_type = iter_type[0]
        elif isinstance(iter_type, Dict):
            item_type = (iter_type.key_type, iter_type.value_type)
        else:
            raise CompileError("unsupported type", node)

        self.context.push()
        self.visit_define_local_variables(generator.target, item_type)
        result_type = [self.visit(node.elt)]
        self.context.pop()

        return result_type

    def visit_DictComp(self, node):
        if len(node.generators) != 1:
            raise CompileError("only one for-loop allowed", node)

        generator = node.generators[0]
        iter_type = self.visit(generator.iter)

        if isinstance(iter_type, list):
            item_type = iter_type[0]
        elif isinstance(iter_type, Dict):
            item_type = (iter_type.key_type, iter_type.value_type)
        else:
            raise CompileError("unsupported type", node)

        self.context.push()
        self.visit_define_local_variables(generator.target, item_type)
        result_type = Dict(self.visit(node.key), self.visit(node.value))
        self.context.pop()

        return result_type

    def visit_SetComp(self, node):
        raise CompileError("set comprehension is not implemented", node)
