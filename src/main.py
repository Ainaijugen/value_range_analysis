from src.my_function import Function

def prepare(filename):
    with open(filename, 'r') as f:
        data = f.read()
    data = data.split(';;')
    data = data[1:] #Remove lines before first ';;'

    return data

def main():
    data = prepare('../project/benchmark/t9.ssa')
    func_list = {}
    for func in data:
        func_obj = Function(func)
        func_list[func_obj.name] = func_obj
    print(func_list)
    func_list['foo'].start()
    for x in func_list['foo'].blocklist:
        print(x, func_list['foo'].blocklist[x].IN)

main()
