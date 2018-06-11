class Block:
    def __init__(self, List):
        List = List.splitlines()
        self.stat = []
        if List[0][0] != '<':
            self.id = '<bb 1>'
            List[0] = List[0][List[0].find('(') + 1:List[0].find(')')]
            List[0] = List[0].split(',')
            for s in List[0]:
                self.stat.append(s)
            for line in List[1:]:
                if line[0] != '{':
                    self.stat.append(line[:line.find(';')])
        else:
            self.id = List[0][:List[0].find(':')]
            for line in List[1:]:
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
