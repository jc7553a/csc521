import sys
import pprint
import itertools
import collections

pp = pprint.PrettyPrinter(indent=1, depth=100)


# start utilities
def lookup_in_scope_stack(name, scope):
    '''Returns values (including declared functions!) from the scope.
    name - A string value holding the name of a bound variable or function.
    scope - The scope that holds names to value binding for variables and
        functions.
    returns - the value associated with the name in scope.
    '''
    # turn this on for better debugging
    # print("lookup_in_scope_stack() "+ str(name))

    if name in scope:
        return scope[name]
    else:
        if "__parent__" in scope:
            # print("not found in scope. Looking at __parent__")
            return lookup_in_scope_stack(name, scope["__parent__"])
        # else:
            # print("ERROR: variable " + name + " was not found in scope stack!")


def get_name_from_ident(tok):
    '''Returns the string lexeme associated with an IDENT token, tok.
    '''
    # print("get_name_from_ident() " + tok)
    colon_index = tok.find(":")
    return tok[colon_index+1:]


def get_number_from_ident(tok):
    '''Returns the float lexeme associated with an NUMBER token, tok.
    '''
    # print("get_number_from_ident()" + tok)
    colon_index = tok.find(":")
    return float(tok[colon_index+1:])


def func_by_name(*args):
    '''Calls a function whos name is given as a parameter. It requires the parse
        tree associated with that point in the grammar traversal and the current
        scope.

    *args is interpreted as
        name = args[0] -- the name of the function to call
        pt = args[1] -- the subtree of the parse tree associated with the name
        scope = args[2] -- the scope the subtree should use
    return - Pass through the return value of the called function.
    '''
    name = args[0]
    pt = args[1]
    scope = args[2]
    return globals()[name](pt, scope)
# end utilities


# <Program> -> <Statement> <Program> | <Statement>
def Program0(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)
    func_by_name(pt[2][0], pt[2], scope)


def Program1(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


# <Statement> -> <FunctionDeclaration> | <Assignment> | <Print>
def Statement0(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


def Statement1(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


def Statement2(pt, scope):
    func_by_name(pt[1][0], pt[1], scope)


# <FunctionDeclaration> -> FUNCTION <Name> PAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
def FunctionDeclaration0(pt, scope):
    '''
    1. Get function name.
    2. Get names of parameters.
    3. Get reference to function body subtree.
    4. In scope, bind the function's name to the following list:
        "foo": [['p1', 'p2', 'p3'], [FunctionBodySubtree]]
        where foo is the function names, p1, p2, p2 are the parameters and
        FunctionBodySubtree represents the partial parse tree that holds the
        FunctionBody0 expansion. This would correspond to the following code:
        function foo(p1, p2, p3) { [the function body] }

    #Bonus: check for return value length at declaration time
    '''
    function_name = func_by_name(pt[2][0], pt[2], scope)[1]
    param_names = func_by_name(pt[4][0], pt[4], scope)
    scope[function_name] = [param_names, pt[6]]


# <FunctionParams> -> <NameList> RPAREN | RPAREN
# should return a list of values
def FunctionParams0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def FunctionParams1(pt, scope):
    return []


# <FunctionBody> -> <Program> <Return> | <Return>
def FunctionBody0(pt, scope):
    programPart = func_by_name(pt[1][0], pt[1], scope)
    returnPart = func_by_name(pt[2][0], pt[2], scope)
    return [programPart] + [returnPart]


def FunctionBody1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Return> -> RETURN <ParameterList>
def Return0(pt, scope):
    return func_by_name(pt[2][0], pt[2], scope)


# <Assignment> -> <SingleAssignment> | <MultipleAssignment>
def Assignment0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def Assignment1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <SingleAssignment> -> VAR <Name> ASSIGN <Expression>
def SingleAssignment0(pt, scope):
    # 1. Get name of the variable.
    # 2. Get value of <Expression>
    # 3. Bind name to value in scope.
    # Bonus: error if the name already exists in scope -- no rebinding
    names = func_by_name(pt[2][0], pt[2], scope)
    names = names[1]
    values = func_by_name(pt[4][0], pt[4], scope)
    scope[names] = values


# <MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
def MultipleAssignment0(pt, scope):
    # 1. Get list of variable names
    # 2. Get the values returned from the fuction call
    # Bonus: error if any name already exists in scope -- no rebinding
    # Bonus: error if the number of variable names does not match the number of values
    names = func_by_name(pt[2][0], pt[2], scope)
    values = func_by_name(pt[4][0], pt[4], scope)
    values = values[1]
    for i in range(0, len(values)):
        scope[names[i]] = values[i]


# <Print> -> PRINT <Expression>
def Print0(pt, scope):
    print(str(func_by_name(pt[2][0], pt[2], scope)))


# <NameList> -> <Name> COMMA <NameList> | <Name>
def NameList0(pt, scope):
    param_name = func_by_name(pt[1][0], pt[1], scope)[1]
    return [param_name] + func_by_name(pt[3][0], pt[3], scope)


def NameList1(pt, scope):
    # getting the [1] of the return value for name as it returns a [val, name]
    return [func_by_name(pt[1][0], pt[1], scope)[1]]


# <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
# should return a a list of values.
def ParameterList0(pt, scope):
    value = func_by_name(pt[1][0], pt[1], scope)
    return [value] + [func_by_name(pt[3][0], pt[3], scope)]


def ParameterList1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Parameter> -> <Expression> | <Name>
def Parameter0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def Parameter1(pt, scope):
    # pull value out of [value,name]
    value = func_by_name(pt[1][0], pt[1], scope)
    return value


# <Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
def Expression0(pt, scope):
    # <Term> ADD <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value + right_value


def Expression1(pt, scope):
    # <Term> SUB <Expression>
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value - right_value


def Expression2(pt, scope):
    # <Term>
    return func_by_name(pt[1][0], pt[1], scope)


# <Term> -> <Factor> MULT <Term> | <Factor> DIV <Term> | <Factor>
def Term0(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[3], scope)
    return left_value*right_value


def Term1(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope)
    right_value = func_by_name(pt[3][0], pt[1], scope)
    return left_value/right_value


def Term2(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Factor> -> <SubExpression> EXP <Factor> | <SubExpression> | <FunctionCall> | <Value> EXP <Factor> | <Value>
def Factor0(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope, scope)
    right_value = func_by_name(pt[3][0], pt[3], scope, scope)
    return left_value ** right_value


def Factor1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope, scope)


def Factor2(pt, scope):
    # returns multiple values -- use the first by default.
    return func_by_name(pt[1][0], pt[1], scope, scope)


def Factor3(pt, scope):
    left_value = func_by_name(pt[1][0], pt[1], scope, scope)
    right_value = func_by_name(pt[3][0], pt[3], scope, scope)
    return left_value ** right_value


def Factor4(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope, scope)


# <FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
def FunctionCall0(pt, scope):
    '''
    This is the most complex part of the interpreter as it involves executing a
    a partial parsetree that is not its direct child.

    1. Get the function name.
    2. Retrieve the stored function information from scope.
    3. Make a new scope with old scope as __parent__
    4. Get the list of parameter values.
    5. Bind parameter names to parameter values in the new function scope.
    6. Run the FunctionBody subtree that is part of the stored function information.
    7. Return the list of values generated by the <FunctionBody>
    '''
    # Creating new Scope
    func_scope = {"__parent__": ''}
    # Grabbing PT that I need
    function_tree = func_by_name(pt[1][0], pt[1], scope)
    function_name = function_tree[1]
    function_store = function_tree[0]
    param_values = func_by_name(pt[3][0], pt[3], scope)
    param_names = function_store[0]
    # This will be Index that I need after colon
    index = int(func_by_name(pt[5][0], pt[5], scope))
    param_values = param_values
    paramArray = []
    paramArray.append(param_values)
    # Binding Valuees to Names in Function Scope
    for i in range(0, len(paramArray)):
        placeHolder = str(param_names[i])
        placeHolder2 = paramArray[i]
        func_scope[placeHolder] = placeHolder2
    # Getting List of Return Values
    return_values = func_by_name(function_store[1][0], function_store[1], func_scope)
    new_values = []
    # Compressing myCrazy List of subLists
    new_values = list(compressList(return_values))
    # Returning the right return Value
    return new_values[index]


def FunctionCall1(pt, scope):
    '''
    1.Get Function Name
    2. Retrieve the stored function information from scope
    3. Make a new scope with old scope as __parent__
    4 Bind Values
    5. REturn stuff
    '''
    # Making New Scope
    func_scope = {"__parent__": ''}
    # Grabbing PT I Need
    function_tree = func_by_name(pt[1][0], pt[1], scope)
    function_name = function_tree[1]
    function_store = function_tree[0]
    param_values = func_by_name(pt[3][0], pt[3], scope)
    param_names = function_store[0]
    # Binding Values to Names in Function Scope
    for i in range(0, len(param_values)):
        placeHolder = str(param_names[i])
        placeHolder2 = param_values[i]
        func_scope[placeHolder] = placeHolder2
    return_values = func_by_name(function_store[1][0], function_store[1], func_scope)
    return return_values


# <FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
def FunctionCallParams0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


def FunctionCallParams1(pt, scope):
    return[]


# <SubExpression> -> LPAREN <Expression> RPAREN
def SubExpression0(pt, scope):
    return func_by_name(pt[2][0], pt[1], scope)


# <Value> -> <Name> | <Number>
def Value0(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)[0]


def Value1(pt, scope):
    return func_by_name(pt[1][0], pt[1], scope)


# <Name> -> IDENT | SUB IDENT | ADD IDENT
def Name0(pt, scope):
    name = get_name_from_ident(pt[1])
    return [lookup_in_scope_stack(name, scope), name]


def Name1(pt, scope):
    name = get_name_from_ident(pt[2])
    return[-lookup_in_scope_stack(name, scope), name]


def Name2(pt, scope):
    name = get_name_from_ident(pt[2])
    return[lookup_in_scope_stack(name, scope), name]


# <Number> -> NUMBER | SUB NUMBER | ADD NUMBER
def Number0(pt, scope):
    return get_number_from_ident(pt[1])


def Number1(pt, scope):
    return -get_number_from_ident(pt[2])


def Number2(pt, scope):
    return get_number_from_ident(pt[2])


def compressList(source, ltypes=collections.Sequence):
    '''
       Function Created to Fix List of Sublists given back in FunctionCall0
       Needed to Compress a wierd List of SubLists
       '''
    newList = list(source)
    i = 0
    while i < len(newList):
        while isinstance(newList[i], ltypes):
            if not newList[i]:
                newList.pop(i)
                i -= 1
                break
            else:
                newList[i:i+1] = newList[i]
        yield newList[i]
        i = i + 1


def ReadInput():
    '''
    Reading Input from StdIn
    '''
    lines = sys.stdin.read()
    return lines


if __name__ == '__main__':
    scope = {}
    tree = eval(ReadInput())
    func_by_name(tree[0], tree, scope)
    # pp.pprint(scope)
