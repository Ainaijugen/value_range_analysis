class Block:
    def __init__(self,_id,_pred,_succ,_stat,_IN,_OUT):
        self.id = _id       # block id, int
        self.pred = _pred     # pre list, a list of block id, int
        self.succ = _succ   # succ list, a list of block id, int
        self.stat = _stat   # statements, a list of statements, str
        self.IN = _IN       # IN, dictionary, dic[var] = (left,left_var,right,right_var)
        self.OUT = _OUT     # OUT，dictionary dic[var] = (left,left_var,right,right_var)

def prepare(filename):
    filename = './benchmark/t3.ssa'
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

prepare()
