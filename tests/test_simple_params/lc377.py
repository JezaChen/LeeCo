# -*- encoding:utf-8 -*-
from typing import List


class Solution:
    def combinationSum4(self, nums: List[int], target: int) -> int:
        dp = [0] * (target + 1)
        dp[0] = 1
        for sum_ in range(1, target + 1):
            for num in nums:
                if sum_ - num >= 0:
                    dp[sum_] += dp[sum_ - num]
        return dp[target]

    def _utilFunc(self):
        ...


if __name__ == '__main__':
    import leeco
    leeco.inject(Solution.combinationSum4)
    leeco.test('''
    [1,2,3]
    4
    [9]
    3
    ''')

