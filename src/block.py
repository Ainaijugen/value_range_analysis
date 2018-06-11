class Block:
    def __init__(self, list):
        list = list.splitlines()
        self.stat = []
        if list[0][0] != '<':
            self.id = '<bb 1>'
            list[0] = list[0][list[0].find('(') + 1:list[0].find(')')]
            list[0] = list[0].split(',')
            for s in list[0]:
                self.stat.append(s)
            for line in list[1:]:
                if line[0] != '{':
                    self.stat.append(line[:line.find(';')])
        else:
            self.id = list[0][:list[0].find(':')]
            for line in list[1:]:
                if line[0] != '}':
                    if line[-1] == ';':
                        self.stat.append(line[:-1])
                    else:
                        self.stat.append(line)
        
        print(self.id, self.stat)
        self.pred = []
        self.succ = []
        self.IN = {}
        self.OUT = {}
