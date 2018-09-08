import sys
import constants as const
import clint.textui as clint_ui
import parser_classes as classes
import clint.textui.prompt as prompt
import clint.textui.core as clint_core

#from clint.textui import puts, colored
#from clint.textui.core import puts_err, indent
		
def get_subformula(expr, idx):
    
    """Matches the brackets in an expression and returns the contents
    between the brackets. If the expression is invalid it returns None."""

    str_length = len(expr)
    bstack = classes.Stack()
    lpos = -1
    rpos = str_length
    for i in range(idx, str_length):        
        c = expr[i]
        if c == '(':
            bstack.push(c)
            if lpos == -1:
                lpos = i + 1
                continue

        if lpos > -1:
            if (c == ')') and (bstack.peek() == '('):
                bstack.pop()
                if bstack.is_empty():
                    rpos = i
                    break
                
        elif c == ')':
            rpos = i
            break
    else:
        if lpos == -1:
            lpos = 0
    
    if (lpos == -1 and rpos != str_length) or \
       (lpos > 0 and rpos == str_length) or \
       (lpos == rpos):
        return (None, 0)
    
    return (expr[lpos:rpos], rpos) 

	
def get_operator(formula, start_index):

    max_number_of_chars = 1
    op = ''
    
    if start_index < len(formula):            
        for i in range(max_number_of_chars, 0, -1):
            op = ''
            for j in range(start_index, start_index + i):
                op += formula[j]
                if op in const.OPERATORS:
                    return op, start_index + len(op)
               
    return '', start_index


def get_number(formula, start_index):

    number = ''
    dot_count = 0
    next_i = start_index

    for i in range(start_index, len(formula)):
        c = formula[i]
        if not(c in const.NUMBER_COMPONENTS):
            next_i = i
            break
        elif c == const.NUMBER_COMPONENTS[0]:
            dot_count += 1

        number += c
    else:
        next_i = len(formula)
    
    if dot_count > 1:
        return
    else:
        return number, next_i


def calculate(op_list, num_list):

    if len(op_list) != len(num_list) - 1:
        return
    
    while len(op_list) > 0:

        min_prec = 4
        pos = 0
        for i in range(len(op_list)):
            if (op_list[i].prec() < min_prec) or \
               (op_list[i].prec() == 1 and op_list[i].prec() <= min_prec):
                min_prec = op_list[i].prec()
                pos = i

        n1 = num_list[pos]
        n2 = num_list[pos + 1]
        num_list[pos] = op_list[pos].calculate(n1, n2)
        num_list.pop(pos + 1)
        op_list.pop(pos)
        
    return num_list[0]


def get_function(formula, end_idx):

    if end_idx > 4:
        max_length = 4
    else:
        max_length = end_idx
    
    check_list = ['(']
    check_list.extend(const.OPERATORS)
    
    for i in range(end_idx - 1, -1, -1):
        if formula[i] in check_list:
            start_idx = i + 1
            break
    else:
        start_idx = 0
    
    substr_length = end_idx - start_idx
    func_length = substr_length
    if substr_length > 3:
        func_length = 4
    elif substr_length < 2:
        return ''
    
    function_name = ''
    invalid_function_names = []
    for length in range(func_length, 1, -1):
        for pos in range(start_idx, end_idx - length + 1):
            end_pos = pos + length
            tmp_str = formula[pos:end_pos].strip()
            if tmp_str in const.MATH_FUNCTIONS: 
                function_name = tmp_str
                break

        if function_name:
            break
    
    if function_name != formula[start_idx:end_idx].strip():        
        return

    return function_name


def get_symbol_function_value(formula, number, start_idx):    
    
    pos = 0
    chars_between = ''
    for i in range(start_idx, len(formula)):
        if formula[i] in const.SYMBOL_FUNCTIONS:
            pos = i
            break
        else:
            chars_between += formula[i]
    else:
        return number, start_idx

    #Thus pos > 0
    chars_between = chars_between.split()
    if chars_between:
        return number, start_idx
    
    func = classes.Symbol_Function(formula[i])
    return func.calculate(number), pos + 1

def get_previous_line_value(formula, idx):
    
    sline_no = ''
    next_pos = idx + 1
    
    check_list = ['(',')']
    check_list.extend(const.OPERATORS)

    for i in range(next_pos, len(formula)):
        if formula[i] in check_list:
            next_pos = i
            break
        sline_no += formula[i]
    else:
        next_pos = len(formula)
    
    try:
        line_no = int(sline_no.strip())
        for i in range(0, len(calculation_history)):
            if line_no == calculation_history[i]['line']:
                if calculation_history[i]['err']:
                    raise Exception('An error occurred on line ' + str(line_no))
                elif calculation_history[i]['operation'] != 'calc':
                    raise Exception('No calculation was performed on line ' + str(line_no))
                
                return calculation_history[i]['operation_result'], next_pos
        else:
            raise Exception('No such line number exists.')
    except Exception as e:
        #Not a valid integer value for $
        raise Exception('{}'.format(e))
            
    
def evaluate(formula):
    
    """Algorithm: formula can be understood to be in the form
    f1 op1 f2 op2 f3 op3 ... op(n-1) fn where each of fk can
    be in the same form as subformulas. This definition is recursive.

         { fk1 op(k1) fk2 op(k2) ... op(k(j - 1)) fkj
    fk = {
         { m, m > R

    fk is either a number or a set of brackets (holding a subformula)
    """
    
    i = 0
    number_list = []
    operation_list = []
    
    if formula and formula[0] == '-':
        formula = '0' + formula

    while i < len(formula):        
        if formula[i] == '(':
            function = get_function(formula, i)
            sub_formula, i = get_subformula(formula, i)

            if sub_formula == None or function == None:
                raise Exception(const.INVALID_FORMULA_MESSAGE)
           
            if not function:
                value = evaluate(sub_formula)
            else:
                func = classes.Function(function)
                value = func.calculate(evaluate(sub_formula))

            value, i = get_symbol_function_value(formula, value, i + 1)
            number_list.append(value)

        elif formula[i] == ')':
            raise Exception(const.INVALID_FORMULA_MESSAGE)

        elif not formula[i].isspace():
            if formula[i] == '$':
                value, i = get_previous_line_value(formula, i)
                number_list.append(value)
            else:
                num, i = get_number(formula, i)
                if num:
                    if num.rfind('.') == -1:
                        value = int(num)
                    else:
                        value = float(num)
                    value, i = get_symbol_function_value(formula, value, i)
                    number_list.append(value)
                else:
                    operator, i = get_operator(formula, i)
                    if operator:
                        operation_list.append(classes.Operator(operator))
                    elif not(num):
                        i += 1
        else:
            i += 1            

    value = calculate(operation_list, number_list)
    if value == None:
        raise Exception(const.INVALID_FORMULA_MESSAGE)
    
    return value


def main():
    with clint_core.indent(4):
        print('\n')
        title = (' '*24) + ('<'*3) + ('CLI CALCULATOR') + ('>'*3)
        clint_ui.puts(clint_ui.colored.cyan(title))
        print('\n\n')
        line_no = 0
        global calculation_history; calculation_history = []
        while True:
            line_no += 1
            try:
                formula = input('<'+str(line_no)+'> ')
                if formula == '..' or formula.lower() == 'exit':
                    break

                if (formula.lower() == 'help') or (formula == '?'):
                    #use input() to stall the program while displaying help
                    input(const.HELP_TEXT)
                    line_data = {'line':line_no,
                                 'operation':'help',
                                 'operation_result':calc,
                                 'err':False}
                    calculation_history.append(line_data)
                else:
                    calc = evaluate(formula)                
                    clint_ui.puts(clint_ui.colored.yellow('= '+str(calc)))
                    line_data = {'line':line_no,
                                 'operation':'calc',
                                 'operation_result':calc,
                                 'err':False}
                    calculation_history.append(line_data)
            except Exception as err:
                line_data = {'line':line_no,
                             'operation':'calc',
                             'operation_result':0,
                             'err':True}
                calculation_history.append(line_data)
                clint_core.puts_err(clint_ui.colored.red('Error: {}'.format(err)))

if __name__ == "__main__":
    main()
