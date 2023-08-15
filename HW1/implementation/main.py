import numpy as np
import copy


class PCN_cube:
    def __init__(self, vars_num, line):
        self.vars_num = vars_num
        line_arr_strs = line.split()
        line_arr = list(map(lambda a: int(a), line_arr_strs))
        # first one is dummy ( numbers start with 1)
        self.slots = [11] * (vars_num + 1)

        # first element is number of slots
        for i in range(0, len(line_arr)):
            if line_arr[i] > 0:
                self.slots[line_arr[i]] = 1
            else:
                self.slots[-line_arr[i]] = 10

    def is_all_dont_care(self):
        for i in range(1, self.vars_num + 1):
            if self.slots[i] != 11:
                return False
        return True

    def complement_cube(self):
        res_cubs_list = []
        for i in range(1, self.vars_num + 1):
            print('29')
            if self.slots[i] != 11:
                print('31')
                new_cube = PCN_cube.create_dont_care(self.vars_num)
                if self.slots[i] == 10:
                    print('34')
                    new_cube.slots[i] = 1
                else:
                    print('37')
                    new_cube.slots[i] = 10
                res_cubs_list.append(new_cube)
        return res_cubs_list

    def get_cofactor(self, var_idx, pos_cof):
        if self.slots[var_idx] == 11:
            return copy.deepcopy(self)
        if pos_cof and self.slots[var_idx] == 10:
            return None
        if not pos_cof and self.slots[var_idx] == 1:
            return None
        new_cube = copy.deepcopy(self)
        new_cube.slots[var_idx] = 11
        return new_cube

    def create_dont_care(vars_num):
        return PCN_cube(vars_num, '')


class cubes_list:

    def __init__(self, input_file):
        if input_file == '':
            return
        f = open(input_file, "r")
        file_cont = f.read().split('\n')
        file_cont = list(filter(lambda x: x != '', file_cont))
        self.vars_num = int(file_cont[0])
        self.cubes = list(map(lambda a: PCN_cube(self.vars_num, a), file_cont[2:]))

    def crete_dont_care(vars_num):
        new_list = cubes_list('')
        new_list.vars_num = vars_num
        new_list.cubes = [PCN_cube.create_dont_care(vars_num)]
        return new_list

    def create_empty(vars_num):
        new_list = cubes_list('')
        new_list.vars_num = vars_num
        new_list.cubes = []
        return new_list

    def get_most_binate(self):
        # collect scores to choose the most binate
        # for each binate variable 1000000
        # for each appearance is 1000 point
        # for diff between pos and negative -1

        ture_state = [0] * (self.vars_num + 1)
        false_state = [0] * (self.vars_num + 1)
        scores = [0] * (self.vars_num + 1)
        for i in range(len(self.cubes)):
            for j in range(self.vars_num + 1):
                if self.cubes[i].slots[j] == 1:
                    ture_state[j] += 1
                if self.cubes[i].slots[j] == 10:
                    false_state[j] += 1

        for i in range(self.vars_num + 1):
            # binate
            if ture_state[i] != 0 and false_state[i] != 0 and ture_state[i] != false_state[i]:
                scores[i] += 1000000
            # each appearance
            scores[i] += 1000 * (ture_state[i] + false_state[i])
            # minimal diff
            scores[i] += -1 * abs(ture_state[i] - false_state[i])

        max_score = np.max(scores)
        for i in range(1, self.vars_num + 1):
            if scores[i] == max_score:
                return i

    def get_cofactor(self, var_idx, pos_cof):
        new_list = cubes_list.create_empty(self.vars_num)
        for i in range(len(self.cubes)):
            new_cof = self.cubes[i].get_cofactor(var_idx, pos_cof)
            if new_cof is not None:
                new_list.cubes.append(new_cof)
        return new_list

    def complement(self):
        if len(self.cubes) == 0:
            return cubes_list.crete_dont_care(self.vars_num)

        if len(self.cubes) == 1:
            res = cubes_list.create_empty(self.vars_num)
            res.cubes = self.cubes[0].complement_cube()
            return res
        is_all_dont_care = True
        for i in range(len(self.cubes)):
            if not self.cubes[i].is_all_dont_care():
                is_all_dont_care = False
                break
        if is_all_dont_care:
            return cubes_list.create_empty(self.vars_num)

        most_binate_idx = self.get_most_binate()
        p = self.get_cofactor(most_binate_idx, True).complement()
        n = self.get_cofactor(most_binate_idx, False).complement()

        # p AND x
        for i in range(len(p.cubes)):
            p.cubes[i].slots[most_binate_idx] = 1
        # p AND not(x)
        for i in range(len(n.cubes)):
            n.cubes[i].slots[most_binate_idx] = 10
        # n OR p
        res = cubes_list.create_empty(self.vars_num)
        res.cubes = n.cubes + p.cubes
        return res


input_list = cubes_list('../input_data/part5.pcn')
output_cubs_list = input_list.complement()
of = open('../output_data/part5.pcn', 'w')
of.write(str(input_list.vars_num) + '\n')
of.write(str(len(output_cubs_list.cubes)) + '\n')
for i in range(len(output_cubs_list.cubes)):
    line_vars_num = 0
    cube_str = ''
    for j in range(1, input_list.vars_num + 1):
        if output_cubs_list.cubes[i].slots[j] == 1:
            cube_str += str(j) + ' '
            line_vars_num +=1
        if output_cubs_list.cubes[i].slots[j] == 10:
            cube_str += str(-j) + ' '
            line_vars_num += 1
    if cube_str != '':
        of.write(str(line_vars_num) + ' ' + cube_str + '\n')
