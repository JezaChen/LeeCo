# -*- encoding:utf-8 -*-
from collections import defaultdict


class Solution:
    def countOfAtoms(self, formula: str) -> str:
        level_to_atom_cnt = [{}]

        i = 0
        while i < len(formula):
            ch = formula[i]
            if ch == '(':
                level_to_atom_cnt.append({})
                i += 1
            elif ch == ')':
                group_cnt = 1

                # 计数括号化学式的数量
                if i + 1 < len(formula) and formula[i + 1].isdigit():
                    group_cnt = 0
                    i += 1
                    while i < len(formula) and formula[i].isdigit():
                        group_cnt *= 10
                        group_cnt += int(formula[i])
                        i += 1
                else:
                    i += 1

                cur_level_atom_cnt_map = level_to_atom_cnt.pop()
                for atom in cur_level_atom_cnt_map:
                    cur_level_atom_cnt_map[atom] *= group_cnt
                # 更新上一层的原子数量
                for atom, cnt in cur_level_atom_cnt_map.items():
                    level_to_atom_cnt[-1][atom] = level_to_atom_cnt[-1].get(atom, 0) + cnt
            elif ch.isalpha():
                cur_atom_name_arr = [ch]
                i += 1
                # 扫描剩下的小写字母以获得完整的元素名
                while i < len(formula) and formula[i].isalpha() and formula[i].islower():
                    cur_atom_name_arr.append(formula[i])
                    i += 1
                cur_atom_name = ''.join(cur_atom_name_arr)
                # 扫描元素数量
                atom_cnt = 0
                while i < len(formula) and formula[i].isdigit():
                    atom_cnt *= 10
                    atom_cnt += int(formula[i])
                    i += 1
                if atom_cnt == 0:
                    atom_cnt = 1
                level_to_atom_cnt[-1][cur_atom_name] = level_to_atom_cnt[-1].get(cur_atom_name, 0) + atom_cnt
        ans_arr = []
        for atom, cnt in sorted(level_to_atom_cnt[-1].items()):
            s = f"{atom}{cnt}" if cnt > 1 else atom
            ans_arr.append(s)
        return ''.join(ans_arr)


if __name__ == '__main__':
    import LeetCodeTestcaseHelper

    LeetCodeTestcaseHelper.test('''
"H2O"
"Mg(OH)2"
"K4(ON(SO3)2)2"
"(H)"
    ''')
