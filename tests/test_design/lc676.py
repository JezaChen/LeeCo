# -*- encoding:utf-8 -*-

from typing import List
from collections import defaultdict


class _Trie:
    def __init__(self):
        self.children = {}
        self.is_finished = False  # 该节点是否对应一个完整的单词


class MagicDictionary:

    def __init__(self):
        self._root = _Trie()

    def buildDict(self, dictionary: List[str]) -> None:
        # 构建trie
        for word in dictionary:
            cur_node = self._root
            for ch in word:
                if ch not in cur_node.children:
                    cur_node.children[ch] = _Trie()
                cur_node = cur_node.children[ch]
            cur_node.is_finished = True

    def search(self, searchWord: str) -> bool:
        def dfs(cur_node: _Trie, pos: int, modified: bool):
            nonlocal searchWord
            if pos == len(searchWord):
                # 单词已经遍历完毕, 判断最后遍历的节点是否对应一个完整的单词, 且有发生过更改
                return cur_node.is_finished and modified
            # 当前位置能匹配上, 继续递归
            if searchWord[pos] in cur_node.children:
                if dfs(cur_node.children[searchWord[pos]], pos + 1, modified):
                    return True
            # 否则, 如果搜索过程没有发生过修改, 则对此位置进行单词变换, 换兄弟节点继续下去
            if not modified:
                for ch, child in cur_node.children.items():
                    if ch != searchWord[pos] and dfs(child, pos + 1, True):
                        return True
            # 已经发生过修改 or 换了兄弟节点也不行, 搜索失败
            return False

        return dfs(self._root, 0, False)


if __name__ == '__main__':
    import leeco
    leeco.test("""
["MagicDictionary", "buildDict", "search", "search", "search", "search"]
[[], [["hello", "leetcode"]], ["hello"], ["hhllo"], ["hell"], ["leetcoded"]]
    """)
