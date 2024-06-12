# -*- encoding:utf-8 -*-
from leeco import TreeNode, List, Optional


class Solution:
    def findDuplicateSubtrees(self, root: TreeNode) -> List[Optional[TreeNode]]:
        tree_dict = dict()
        res = []

        def preorder(node):
            if not node:
                return '#'
            sub_tree = str(node.val) + ',' + preorder(node.left) + ',' + preorder(node.right)
            if sub_tree in tree_dict:
                tree_dict[sub_tree] += 1
            else:
                tree_dict[sub_tree] = 1
            if tree_dict[sub_tree] == 2:
                res.append(node)
            return sub_tree

        preorder(root)
        return res


if __name__ == '__main__':
    import leeco

    leeco.test("""
[1,2,3,4,null,2,4,null,null,4]
[2,1,1]
[2,2,2,3,null,3,null]
    """)
