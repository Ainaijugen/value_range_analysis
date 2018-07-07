import re
import copy
import math

re_float = re.compile(r'^[-+]?([0-9]+(\.[0-9]+)?|\.[0-9]+)([eE][-+]?[0-9]+)?$')
re_int = re.compile(r'^[-+]?[0-9]+$')
re_def = re.compile(r'^([a-zA-Z@]*)[0-9]*_[0-9]+$')


class Block:
    def __init__(self, List, _func_ref):
        List = List.splitlines()
        # print(List)
        self.stat = []
        self.func_ref = _func_ref
        self.is_visited = False
        self.live_is_visited = False
        if List[0][0] != '<':
            self.id = '<bb 1>'  # the f
            List[0] = List[0][List[0].find('(') + 1:List[0].find(')')]
            List[0] = List[0].split(', ')
            for s in List[0]:
                self.stat.append(s)

            for line in List[1:]:
                if line[0] != '{':
                    self.stat.append(line[:line.find(';')])
        else:
            self.id = List[0][:List[0].find(':')]
            if_buffer = []
            for line in List[1:]:
                if line[0] != '}':
                    if len(if_buffer) > 0:
                        if_buffer.append(line.strip())
                    elif line.strip()[0:2] == 'if':
                        if_buffer.append(line.strip())
                    elif line[-1] == ';':
                        self.stat.append(line[:-1])
                    else:
                        self.stat.append(line)
                    if len(if_buffer) == 4:
                        tmp = ' '.join(if_buffer)
                        self.stat.append(tmp)
                        # print(if_buffer)
                        if_buffer = []

        print(self.id, self.stat)

        # pred and succ will be initialize in Function init
        self.pred = []
        self.succ = []

        self.IN = {}  # key: id_def, value: ([/(, ]/), min_val, max_val)  []:1 ():0
        self.OUT = {}

        self.TYPE = {}

        self.live_IN = set()
        self.live_OUT = set()
        self.greater = set()
        self.less = set()

    def valueof(self, x):
        print(x)
        if x[-3:] == "(D)":
            x = x[:-3]
            if x not in self.OUT:
                self.OUT[x] = self.func_ref.inputs[x if x[0] == '_' or x.find("_") == -1 else x[:x.find("_")]]
        if re_int.search(x) is not None:
            return (1, 1, int(x), int(x))
        if re_float.search(x) is not None:
            return (1, 1, float(x), float(x))
        if re_def.search(x) is not None:
            if x not in self.OUT:
                # self.OUT[x] = (1, 1, float('-inf'), float('inf'))
                return None
            return self.OUT[x]
        if x[0] == '_' and x.find('@')!=-1:
            if x not in self.OUT:
                # self.OUT[x] = (1, 1, float('-inf'), float('inf'))
                return None
            return self.OUT[x]
        raise ValueError("Cannot handle %s!" % x)

    def typeof(self, x):

        if re_int.search(x) is not None:
            return 'int'
        if re_float.search(x) is not None:
            return 'float'
        if (x if x[0] == '_' or x.find("_") == -1 else x[:x.find("_")]) in self.TYPE:
            return self.TYPE[x if x[0] == '_' or x.find("_") == -1 else x[:x.find("_")]]
        raise ValueError("Cannot handle %s!" % x)

    def intersection(self, a, b):
        # print("inter", a, b)
        ans = [1] * 4
        if a[2] < b[2]:  # a[2] b[2]
            ans[0] = b[0]
            ans[2] = b[2]
            if a[3] < b[2] or (a[3] == b[2] and a[1] & b[0] == 0):
                return None
            if b[3] < a[3]:
                ans[1] = b[1]
                ans[3] = b[3]
            elif a[3] < b[3]:
                ans[1] = a[1]
                ans[3] = a[3]
            else:
                ans[1] = a[1] & b[1]
                ans[3] = a[3]
        elif a[2] > b[2]:  # b[2] a[2]
            ans[0] = a[0]
            ans[2] = a[2]
            if b[3] < a[2] or (b[3] == a[2] and b[1] & a[0] == 0):
                return None
            if a[3] < b[3]:
                ans[1] = a[1]
                ans[3] = a[3]
            elif b[3] < a[3]:
                ans[1] = b[1]
                ans[3] = b[3]
            else:
                ans[1] = a[1] & b[1]
                ans[3] = a[3]
        else:
            ans[0] = a[0] & b[0]
            ans[2] = a[2]
            if a[3] < b[3]:
                ans[3] = a[3]
                ans[1] = a[1]
            elif a[3] > b[3]:
                ans[3] = b[3]
                ans[1] = b[1]
            else:
                ans[3] = a[3]
                ans[1] = a[1] & b[1]
        # print("inter_ans",a,b,tuple(ans))
        return tuple(ans)

    def cast_float_to_int(self, ran):
        if ran is None:
            return None
        ans = [1] * 4
        ran = list(ran)
        if ran[2] != float('inf') and ran[2] != float('-inf') and ran[3] != float('inf') and ran[3] != float('-inf'):
            candi_min = [math.floor(ran[2]),math.ceil(ran[2])]
            candi_max = [math.floor(ran[3]),math.ceil(ran[3])]
            for i in range(2):
                if 0.0000000000001< math.fabs(ran[2]-candi_min[i]) < 0.0001:
                    ran[2] = candi_min[i]
                if 0.0000000000001<math.fabs(ran[3]-candi_max[i]) < 0.0001:
                    ran[3] = candi_max[i]
        if ran[0] == 0:
            if math.isinf(ran[2]):
                ans[2] = ran[2]
            else:
                ans[2] = int(ran[2]) + 1
        else:
            if math.isinf(ran[2]):
                ans[2] = ran[2]
            else:
                ans[2] = math.ceil(ran[2])
        if ran[1] == 0:
            if math.isinf(ran[3]):
                ans[3] = ran[3]
            else:
                ans[3] = math.ceil(ran[3]) - 1
        else:
            if math.isinf(ran[3]):
                ans[3] = ran[3]
            else:
                ans[3] = math.floor(ran[3])
        return tuple(ans)

    def merge_in(self, pred_out, type):
        print(self.id, self.IN, pred_out)
        # merge self.IN and pred_out
        flag = False
        for x in self.IN:
            if x in pred_out:
                # tmp = pred_out[x]
                # if x not in self.live_OUT:
                #     tmp = self.union(self.IN[x], pred_out[x])
                if type == "W":
                    tmp = self.union(self.IN[x], pred_out[x])
                else:
                    tmp = pred_out[x]
                if tmp != self.IN[x]:
                    if tmp[2] < self.IN[x][2]:
                        self.less.add(x)
                    if tmp[3] > self.IN[x][3]:
                        self.greater.add(x)
                    flag = True
                    print("change ", x)
                    self.IN[x] = tmp
        for x in pred_out:
            if x not in self.IN:
                flag = True
                self.IN[x] = pred_out[x]
                print("change ", x)
        return flag

    def union(self, y_value, z_value):
        if y_value is None and z_value is None:
            raise ValueError("two Nones in union!")
        if y_value is None:
            return z_value
        if z_value is None:
            return y_value
        ans = [1] * 4
        # print(y_value,z_value)
        if y_value[2] < z_value[2]:
            ans[0] = y_value[0]
            ans[2] = y_value[2]
        elif y_value[2] == z_value[2]:
            ans[0] = y_value[0] | z_value[0]
            ans[2] = y_value[2]
        else:
            ans[0] = z_value[0]
            ans[2] = z_value[2]
        if y_value[3] > z_value[3]:
            ans[1] = y_value[1]
            ans[3] = y_value[3]
        elif y_value[3] == z_value[3]:
            ans[1] = y_value[1] | z_value[1]
            ans[3] = y_value[3]
        else:
            ans[1] = z_value[1]
            ans[3] = z_value[3]
        return tuple(ans)

    def try_to_add(self, next_block, OUT, type):
        if OUT is None:
            return
        next_block.TYPE = self.TYPE
        if next_block.merge_in(OUT, type) == True or not next_block.is_visited:
            if next_block.id not in self.func_ref.in_queue:
                print("Add ", next_block.id)
                self.func_ref.queue.put(next_block.id)
                self.func_ref.in_queue.add(next_block.id)

    def in_to_out(self, type):
        print("Processing: ", self.id)
        self.OUT = copy.copy(self.IN)
        self.is_visited = True
        self.greater = set()
        self.less = set()
        for line in self.stat:
            line = line.split()
            if len(line) == 0:
                continue
            if 'return' in line:
                self.func_ref.returnname = line[1]
                print('\n')
                print('finish analysing, the answer is: ')
                print('return range = [',self.OUT[line[1]][2],',',self.OUT[line[1]][3],']')
            if len(line) == 11 and line[0] == 'if':
                op = line[2]
                x = line[1][1:]
                y = line[3][:-1]
                x_value = self.valueof(x)
                y_value = self.valueof(y)
                true_label = line[5] + ' ' + line[6][:-1]
                false_label = line[9] + ' ' + line[10][:-1]

                def cal_out(op, OUT, x, y, x_value, y_value):
                    if op == '<':
                        OUT[x] = self.intersection(x_value, (1, 0, float("-inf"), y_value[3]))
                        OUT[y] = self.intersection(y_value, (0, 1, x_value[2], float("inf")))
                    elif op == '>=':
                        OUT[x] = self.intersection(x_value, (y_value[0], 1, y_value[2], float('inf')))
                        OUT[y] = self.intersection(y_value, (1, x_value[1], float('-inf'), x_value[3]))
                    elif op == '==':
                        OUT[x] = self.intersection(x_value, y_value)
                        OUT[y] = self.intersection(y_value, x_value)
                    elif op == '!=':
                        OUT[x] = x_value
                        OUT[y] = y_value
                    if OUT[x] is None or OUT[y] is None:
                        return None
                    if self.typeof(x) == "int":
                        OUT[x] = self.cast_float_to_int(OUT[x])
                    if self.typeof(y) == "int":
                        OUT[y] = self.cast_float_to_int(OUT[y])
                    return OUT

                if re_float.search(x) is None and re_float.search(y) is None and type == "W":
                    true_OUT = copy.copy(self.OUT)
                    false_OUT = copy.copy(self.OUT)
                else:
                    if op == '<':
                        true_OUT = cal_out("<", copy.copy(self.OUT), x, y, x_value, y_value)
                        false_OUT = cal_out(">=", copy.copy(self.OUT), x, y, x_value, y_value)
                    elif op == '<=':
                        true_OUT = cal_out('>=', copy.copy(self.OUT), y, x, y_value, x_value)
                        false_OUT = cal_out('<', copy.copy(self.OUT), y, x, y_value, x_value)
                    elif op == '>':
                        true_OUT = cal_out("<", copy.copy(self.OUT), y, x, y_value, x_value)
                        false_OUT = cal_out(">=", copy.copy(self.OUT), y, x, y_value, x_value)
                    elif op == '>=':
                        true_OUT = cal_out(">=", copy.copy(self.OUT), x, y, x_value, y_value)
                        false_OUT = cal_out("<", copy.copy(self.OUT), x, y, x_value, y_value)
                    elif op == '==':
                        true_OUT = cal_out("==", copy.copy(self.OUT), x, y, x_value, y_value)
                        false_OUT = cal_out("!=", copy.copy(self.OUT), x, y, x_value, y_value)
                    elif op == '!=':
                        true_OUT = cal_out("!=", copy.copy(self.OUT), x, y, x_value, y_value)
                        false_OUT = cal_out("==", copy.copy(self.OUT), x, y, x_value, y_value)
                self.try_to_add(self.func_ref.blocklist[true_label], true_OUT, type)
                self.try_to_add(self.func_ref.blocklist[false_label], false_OUT, type)
                return
            if line[0] == '#' and line[2] == '=':  # PHI
                x = line[1]
                y = line[4][1:line[4].find('(')]
                # y_from = '<bb ' + line[4][line[4].find('(') + 1: line[4].find(')')] + '>'
                z = line[5][0:line[5].find('(')]
                # z_from = '<bb ' + line[5][line[5].find('(') + 1: line[5].find(')')] + '>'
                # if y_from == pred_id:
                #     new_tuple = self.valueof(y)
                # elif z_from == pred_id:
                #     new_tuple = self.valueof(z)
                # else:
                #     new_tuple = self.func_ref.inputs[x if x[0] == '_' or x.find("_") == -1 else x[:x.find("_")]]
                #     # raise ValueError("Cannot determine y: %s, z: %s, pred_id: %s" % (y_from, z_from, pred_id))
                if line[4][line[4].find('(') + 1] == 'D':
                    y += "(D)"
                if line[5][line[5].find('(') + 1] == 'D':
                    z += "(D)"
                y_value = self.valueof(y)
                z_value = self.valueof(z)
                new_tuple = self.union(y_value, z_value)

                if self.TYPE[x if x[0] == '_' or x.find("_") == -1 else x[:x.find("_")]] == 'int':
                    self.OUT[x] = self.cast_float_to_int(new_tuple)
                else:
                    self.OUT[x] = new_tuple
                continue

            if len(line) == 2:  # int i
                if line[0] == 'int' or line[0] == 'float':
                    self.TYPE[line[1]] = line[0]
                continue
            if len(line) == 3:
                if line[0] == 'goto':
                    self.try_to_add(self.func_ref.blocklist[line[1] + ' ' + line[2]], self.OUT, type)
                    return
            if line[1] == '=':
                if len(line) == 4:  # x = (float) y
                    x = line[0]
                    y = line[3]
                    y_value = self.valueof(y)
                    if line[2] == '(float)':
                        self.OUT[x] = y_value
                    elif line[2] == '(int)':
                        self.OUT[x] = self.cast_float_to_int(y_value)
                    else:
                        raise TypeError('cannot do force convert %s', line[2])
                if len(line) == 3:  # x = y
                    x = line[0]
                    y = line[2]
                    y_value = self.valueof(y)
                    y_type = self.typeof(y)
                    if self.TYPE[x if x[0] == '_' or x.find("_") == -1 else x[:x.find("_")]] == 'int':
                        self.OUT[x] = self.cast_float_to_int(y_value)
                    else:
                        self.OUT[x] = y_value
                    continue

                if len(line) == 5:  # x = y op z
                    x = line[0]
                    y = line[2]
                    op = line[3]
                    z = line[4]
                    y_value = self.valueof(y)
                    z_value = self.valueof(z)
                    new_par_left = ''
                    new_par_right = ''
                    new_min = ''
                    new_max = ''
                    if op == '+':
                        # print("op+",y_value,z_value)
                        new_par_left = y_value[0] & z_value[0]
                        new_par_right = y_value[1] & z_value[1]
                        new_min = y_value[2] + z_value[2]
                        new_max = y_value[3] + z_value[3]

                    elif op == '-':
                        if y_value[0] == 0 and z_value[0] == 1:
                            new_par_left = 0
                        else:
                            new_par_left = 1
                        if y_value[1] == 0 and z_value[1] == 1:
                            new_par_right = 0
                        else:
                            new_par_right = 1
                        new_min = y_value[2] - z_value[3]
                        new_max = y_value[3] - z_value[2]

                    elif op == '*':
                        new_max = y_value[2] * z_value[2]
                        new_min = new_max
                        max_pos = (0, 0)
                        min_pos = (0, 0)
                        for i in range(2, 4):
                            for j in range(2, 4):
                                tmp = y_value[i] * z_value[j]
                                if tmp > new_max:
                                    new_max = tmp
                                    max_pos = (i - 2, j - 2)
                                if tmp < new_min:
                                    new_min = tmp
                                    min_pos = (i - 2, j - 2)
                        new_par_left = y_value[min_pos[0]] & z_value[min_pos[1]]
                        new_par_right = y_value[max_pos[0]] & z_value[max_pos[1]]

                    elif op == '/':
                        if (z_value[2] < 0 or (z_value[2] == 0 and z_value[0] == 1)) and (
                                z_value[3] > 0 or (z_value[2] == 0 and z_value == 1)):
                            raise (ValueError("divided by zero"))
                        else:
                            new_max = y_value[2] / z_value[2]
                            new_min = new_max
                            max_pos = (0, 0)
                            min_pos = (0, 0)
                            for i in range(2, 4):
                                for j in range(2, 4):
                                    if z_value[j] == 0:
                                        tmp = y_value * float('inf')
                                    else:
                                        tmp = y_value[i] / z_value[j]
                                    if tmp > new_max:
                                        new_max = tmp
                                        max_pos = (i - 2, j - 2)
                                    if tmp < new_min:
                                        new_min = tmp
                                        min_pos = (i - 2, j - 2)
                            new_par_left = y_value[min_pos[0]] & z_value[min_pos[1]]
                            new_par_right = y_value[max_pos[0]] & z_value[max_pos[1]]

                    new_tuple = (new_par_left, new_par_right, new_min, new_max)
                    if self.TYPE[x if x[0] == '_' or x.find("_") == -1 else x[:x.find("_")]] == 'int':
                        self.OUT[x] = self.cast_float_to_int(new_tuple)
                    else:
                        self.OUT[x] = new_tuple
                    continue
        if len(self.succ) != 0:
            self.try_to_add(self.func_ref.blocklist[self.succ[0]], self.OUT, type)

    def live_try_to_add(self, pred_block, live_OUT):
        flag = False
        for x in live_OUT:
            if x not in pred_block.live_IN:
                pred_block.live_IN.add(x)
                flag = True
        if (flag or not pred_block.live_is_visited) and pred_block.id not in self.func_ref.in_queue:
            self.func_ref.queue.put(pred_block.id)
            self.func_ref.in_queue.add(pred_block.id)

    def live_in_to_out(self):
        print("Processing: ", self.id)
        self.live_OUT = copy.copy(self.live_IN)
        self.live_is_visited = True
        for line in reversed(self.stat):
            line = line.split()
            if len(line) == 0:
                continue
            if len(line) == 11 and line[0] == 'if':
                x = line[1][1:]
                y = line[3][:-1]
                if re_float.search(x) is None:
                    self.live_OUT.add(x)
                if re_float.search(y) is None:
                    self.live_OUT.add(x)
                continue
            if line[0] == '#' and line[2] == '=':  # PHI
                x = line[1]
                y = line[4][1:line[4].find('(')]
                y_from = '<bb ' + line[4][line[4].find('(') + 1: line[4].find(')')] + '>'
                z = line[5][0:line[5].find('(')]
                z_from = '<bb ' + line[5][line[5].find('(') + 1: line[5].find(')')] + '>'
                if y_from != '<bb D>' and re_float.search(y) is None:
                    self.live_OUT.add(y)
                if z_from != '<bb D>' and re_float.search(z) is None:
                    self.live_OUT.add(z)
                if x in self.live_OUT:
                    self.live_OUT.remove(x)
                continue

            if len(line) == 2:  # int i
                if line[0] == "return":
                    # self.live_OUT.add(line[1])
                    pass
                continue
            if len(line) == 3:
                if line[0] == 'goto':
                    continue
            if line[1] == '=':
                if len(line) == 4:  # x = (float) y
                    x = line[0]
                    y = line[3]
                    if re_float.search(y) is None:
                        self.live_OUT.add(y)
                    if x in self.live_OUT:
                        self.live_OUT.remove(x)
                    continue
                if len(line) == 3:  # x = y
                    x = line[0]
                    y = line[2]
                    if re_float.search(y) is None:
                        self.live_OUT.add(y)
                    if x in self.live_OUT:
                        self.live_OUT.remove(x)
                    continue

                if len(line) == 5:  # x = y op z
                    x = line[0]
                    y = line[2]
                    z = line[4]
                    if re_float.search(y) is None:
                        self.live_OUT.add(y)
                    if re_float.search(z) is None:
                        self.live_OUT.add(z)
                    if x in self.live_OUT:
                        self.live_OUT.remove(x)
                    continue
        for x in self.pred:
            self.live_try_to_add(self.func_ref.blocklist[x], self.live_OUT)
