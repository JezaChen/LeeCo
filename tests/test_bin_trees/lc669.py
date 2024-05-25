# -*- encoding:utf-8 -*-
from typing import Optional
from leeco.data_structures import TreeNode


class Solution:
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        if root is None:
            return root

        if low <= root.val <= high:
            root.left = self.trimBST(root.left, low, high)
            root.right = self.trimBST(root.right, low, high)
            return root
        elif root.val < low:
            return self.trimBST(root.right, low, high)
        else:
            return self.trimBST(root.left, low, high)


if __name__ == '__main__':
    import leeco

    leeco.test('''
[1,0,2]
1
2
[3,0,4,null,2,null,null,1]
1
3
    ''')
