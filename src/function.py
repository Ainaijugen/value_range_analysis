from block import Block

class Function:
    def __init__(self, list):
        list = list.splitlines()
        tmp_list = []
        for line in list:
            if line.strip() != '':
                tmp_list.append(line.lstrip())
        tmp_list = tmp_list[1:]
        for i in range(len(tmp_list)):
            if tmp_list[i][0] == '<':
                tmp_list[i] = '@@' + tmp_list[i]
        list = '\n'.join(tmp_list)
        
        self.name = list[:list.find('(') - 1]
        print('Function: ' + self.name + ' detected, Creating basic blocks:')
        
        list = list.split('@@')
        self.blocklist = {}
        for blocks in list:
            block_obj = Block(blocks)
            self.blocklist[block_obj.id] = block_obj

    def calculate(self, _IN):
        temp = ()
        
        return
