# -*- encoding:utf-8 -*-
from typing import List


class Solution:
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        n = len(customers)
        orig_satisfied = sum(cnt * (1 - is_grumpy) for cnt, is_grumpy in zip(customers, grumpy))
        l, r = 0, minutes - 1
        satisfied_increment_in_cur_window = 0
        for i in range(minutes):
            satisfied_increment_in_cur_window += customers[i] * grumpy[i]
        max_increment = satisfied_increment_in_cur_window
        while r + 1 < n:
            if grumpy[l]:
                satisfied_increment_in_cur_window -= customers[l]
            l += 1
            r += 1
            if grumpy[r]:
                satisfied_increment_in_cur_window += customers[r]
            max_increment = max(max_increment, satisfied_increment_in_cur_window)
        return orig_satisfied + max_increment


if __name__ == '__main__':
    import leeco

    leeco.test('''
			[1,0,1,2,1,1,7,5]
			[1,1,1,1,1,1,1,1]
			1
        ''')
