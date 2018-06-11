from function import Function

def prepare(filename):
    with open(filename, 'r') as f:
        data = f.read()
    data = data.split(';;')
    data = data[1:] #Remove lines before first ';;'

    return data

def main():
    data = prepare('../project/benchmark/t3.ssa')
    func_list = {}
    for func in data:
        func_obj = Function(func)
        func_list[func_obj.name] = func_obj

main()
