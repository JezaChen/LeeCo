# -*- encoding:utf-8 -*-
# Test 2-dimensional list

from typing import List


# leetcode submit region begin(Prohibit modification and deletion)
class Solution:
    moves = [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1)
    ]

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])
        visited = [[False] * n for _ in range(m)]

        def dfs(x: int, y: int) -> int:
            nonlocal visited

            if grid[y][x] == 0:
                return 0
            result = 1
            for move in self.moves:
                nx = x + move[0]
                ny = y + move[1]
                if 0 <= nx < n and 0 <= ny < m and not visited[ny][nx]:
                    visited[ny][nx] = True
                    result += dfs(nx, ny)
            return result

        r = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] and not visited[i][j]:
                    visited[i][j] = True
                    r = max(r, dfs(j, i))
        return r


if __name__ == '__main__':
    import leeco

    leeco.test("""
[[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
[[0,0,0,0,0,0,0,0]]
    """)
