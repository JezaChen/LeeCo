# -*- encoding:utf-8 -*-

class _Trie:
    def __init__(self):
        self.children = {}
        self.prefixSum = 0
        # 以该节点结尾的单词val(因为会存在重复insert的情况, 需要覆盖掉之前的val以及更新前缀和)
        # 如果该值不为0, 则意味着到该节点是有一个完整的单词的
        self.finishedVal = 0


class MapSum:

    def __init__(self):
        self._root = _Trie()

    def insert(self, key: str, val: int) -> None:
        visited_nodes = [self._root]
        cur_node = self._root

        for i, ch in enumerate(key):
            if ch not in cur_node.children:
                cur_node.children[ch] = _Trie()
            cur_node = cur_node.children[ch]
            visited_nodes.append(cur_node)

        old_val = visited_nodes[-1].finishedVal
        if old_val != 0:  # 先前存在相同的单词
            for node in visited_nodes:
                node.prefixSum += (val - old_val)
        else:
            for node in visited_nodes:
                node.prefixSum += val

        visited_nodes[-1].finishedVal = val

    def sum(self, prefix: str) -> int:
        cur_node = self._root
        for ch in prefix:
            if ch not in cur_node.children:
                return 0  # 没有该前缀
            cur_node = cur_node.children[ch]
        return cur_node.prefixSum


if __name__ == '__main__':
    import leeco

    leeco.test("""
["MapSum", "insert", "sum", "insert", "sum"]
[[], ["apple", 3], ["ap"], ["app", 2], ["ap"]]
    """)
