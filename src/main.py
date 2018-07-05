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
    data, input_variables = prepare('../project/benchmark/t9.ssa')
    func_list = {}
    for func in data:
        func_obj = Function(func)
        func_list[func_obj.name] = func_obj

    print(func_list)
    func_list['foo'].inputs = read_range(input_variables)
    func_list['foo'].start()




main()
