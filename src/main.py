from src.my_function import Function


def prepare(filename):
    with open(filename, 'r') as f:
        data = f.read()
    input_variables = data[data.find('\nfoo') + 6:]
    input_variables = input_variables[:input_variables.find(')')]
    if input_variables.strip() != '':
        input_variables = input_variables.split(', ')
        for i in range(len(input_variables)):
            input_variables[i] = input_variables[i].split(' ')
    data = data.split(';;')
    data = data[1:]  # Remove lines before first ';;'

    return data, input_variables


def read_range(input_variables):
    n = len(input_variables)
    value_range = {}
    if n == 0:
        print('No input variables needed.')
        return value_range
    else:
        for i in range(n):
            print('Please enter information about variable {}'.format(input_variables[i][1]))
            print('(Please notice that -inf/inf match [/])')
            left = input('Please enter lower bound open/closed with [ = 1, ( = 0:')
            right = input('Please enter upper bound open/closed with ] = 1, ) = 0:')
            lower = input('Please enter lower bound:')
            upper = input('Please enter upper bound:')
            if lower == '-inf':
                lower = float('-inf')
            elif input_variables[i][0] == 'int':
                lower = int(lower)
            elif input_variables[i][0] == 'float':
                lower = float(lower)
            if upper == 'inf':
                upper = float('inf')
            elif input_variables[i][0] == 'int':
                upper = int(upper)
            elif input_variables[i][0] == 'float':
                upper = float(upper)
            value_range[input_variables[i][1]] = [int(left), int(right), lower, upper]
        print('Range read success:')
        print(value_range)
        return value_range


def main():
    data, input_variables = prepare('../project/benchmark/t10.ssa')
    func_list = {}
    for func in data:
        func_obj = Function(func)
        func_list[func_obj.name] = func_obj
    print(func_list)

    inline_func = ''
    for func in data:
        if func.find('Function foo') != -1:
            inline_func = func

    call_cnt = 1
    is_inline = False
    for f in func_list:
        for bb in func_list['foo'].blocklist:
            for ii in range(len(func_list['foo'].blocklist[bb].stat)):
                if f.strip() != 'foo' and func_list['foo'].blocklist[bb].stat[ii].find(f) != -1:
                    for b in func_list[f].blocklist:
                        for s in func_list[f].blocklist[b].stat:
                            if s.find('return') != -1 and len(s) > 7:
                                is_inline = True
                                print('The function', f, 'needs to inline in\"', func_list['foo'].blocklist[bb].stat[ii], '\"!')
                                # Get inline code
                                inline_code = ''
                                for func in data:
                                    if func.find('Function ' + f) != -1:
                                        inline_code = func
                                variables_inline = inline_code[inline_code.find(')') + 1:]
                                variables_inline = variables_inline[variables_inline.find('(') + 1:variables_inline.find(')')]
                                variables_inline = variables_inline.split(', ')
                                inline_code = inline_code[inline_code.find('{') + 1:inline_code.find('}')]
                                # Inline variables
                                for i in range(len(variables_inline)):
                                    variables_inline[i] = variables_inline[i] + '@' + str(call_cnt)
                                    inline_code = '  ' + variables_inline[i] + ';\n' + inline_code
                                inline_code = '<bb 1@' + str(call_cnt) + '>:\n' + inline_code
                                # Change bb names
                                for bb_old in func_list[f].blocklist:
                                    bb_new = bb_old[:-1] + '@' + str(call_cnt) + bb_old[-1]
                                    inline_code = inline_code.replace(bb_old, bb_new)
                                # Change variables names
                                inline_code = inline_code.split(' ')
                                for i in range(len(inline_code)):
                                    if inline_code[i].find('_') != -1:
                                        if inline_code[i].find('_') > 0 \
                                           and (inline_code[i][inline_code[i].find('_') - 1].isdigit() or inline_code[i][inline_code[i].find('_') - 1].isalpha()):
                                            inline_code[i] = inline_code[i].replace('_', '@' + str(call_cnt) + '_')
                                        else:
                                            if inline_code[i][inline_code[i].find('_'):].find('(') != -1:
                                                inline_code[i] = inline_code[i][:inline_code[i].find('_')] + \
                                                                 inline_code[i][inline_code[i].find('_'):].replace('(', '@' + str(call_cnt) + '(')
                                            elif inline_code[i].find(';') != -1:
                                                inline_code[i] = inline_code[i].replace(';', '@' + str(call_cnt) + ';')
                                            else:
                                                inline_code[i] = inline_code[i] + '@' + str(call_cnt)
                                inline_code = ' '.join(inline_code)

                                # Change PHI labels
                                inline_code = inline_code.splitlines()
                                for i in range(len(inline_code)):
                                    if inline_code[i].find('PHI') != -1:
                                        inline_code[i] = inline_code[i].replace(')', '@' + str(call_cnt) + ')')
                                inline_code = '\n'.join(inline_code)
                                # Generate input and return commands
                                in_variable = func_list['foo'].blocklist[bb].stat[ii][func_list['foo'].blocklist[bb].stat[ii].find('(') + 1:func_list['foo'].blocklist[bb].stat[ii].rfind(')')]
                                in_variable = in_variable.split(', ')
                                in_variable_code = []
                                find_value = {}
                                for i in range(len(in_variable)):
                                    find_value[variables_inline[i][variables_inline[i].find(' ') + 1:]] = in_variable[i]
                                inline_code = inline_code.split('(D)')
                                for i in range(len(inline_code) - 1):
                                    variable_flag = inline_code[i].rfind('@') - 1
                                    while inline_code[i][variable_flag].isalpha() or inline_code[i][variable_flag].isdigit():
                                        variable_flag -= 1
                                    in_variable_code.append(inline_code[i][variable_flag + 1:] + ' = ' + \
                                                            find_value[inline_code[i][variable_flag + 1:inline_code[i].rfind('_')]] + '\n')
                                in_variable_code = list(set(in_variable_code))
                                in_variable_code = ''.join(in_variable_code)
                                inline_code = ''.join(inline_code)
                                inline_code = inline_code.replace('<bb 2', in_variable_code + '\n  <bb 2')
                                inline_code = inline_code.replace('return', func_list['foo'].blocklist[bb].stat[ii][:func_list['foo'].blocklist[bb].stat[ii].find('=') + 1].strip())
                                # Inline and separate bb
                                inline_func = inline_func.replace(func_list['foo'].blocklist[bb].stat[ii] + ';\n', inline_code)
                                inline_func = inline_func.splitlines()
                                for i in range(len(inline_func) - 1):
                                    if inline_func[i].strip() != '' and inline_func[i].strip()[0] == '<' and inline_func[i + 1].strip()[0] == '<':
                                        inline_func[i] = ''
                                inline_func = '\n'.join(inline_func)
                                '''
                                print(func_list['foo'].blocklist[bb].stat[ii - 1][:func_list['foo'].blocklist[bb].stat[ii - 2].find(' ')])
                                if ii == 0:
                                    for bbb in func_list:
                                        if func_list['foo'].blocklist[bb].stat[ii - 1].find(bbb) == -1:
                                            print('Yes!')
                                '''
                                # Change goto and PHI

                                print(inline_func)
                                call_cnt += 1

    if is_inline == True:
        last_func = Function(inline_func)
        last_func.inputs = read_range(input_variables)
        last_func.start()
    else:
        func_list['foo'].inputs = read_range(input_variables)
        func_list['foo'].start()


main()
