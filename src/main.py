from src.function import Function

def prepare(filename):
    func_num = 0
    with open(filename, 'r') as f:
        data = f.read()
    data = data.split(';;')
    func_num = len(data)
    for i in range(len(data)):
        data[i] = data[i].split('\n\n')

    data = data[1:]

    for i,func in enumerate(data):
        for j,block in enumerate(func):
            print(i,j,block,'\n')
    return data

def main():
    data = prepare('../project/benchmark/t3.ssa')
    func_list = {}
    for func in data:
        func_obj = Function(func)
        func_list[func_obj.name()] = func_obj
main()