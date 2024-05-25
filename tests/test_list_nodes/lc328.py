# -*- encoding:utf-8 -*-
from typing import Optional
from leeco.data_structures import ListNode


class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head:
            return head

        dummy_head = ListNode(0, head)
        prev, curr = dummy_head, head
        index = 0
        dummy_even_head = ListNode(0, None)
        curr_even_node = dummy_even_head
        while True:
            index += 1
            if index % 2 == 0:  # even
                curr_even_node.next = curr
                curr_even_node = curr

                prev.next = curr.next  # 剥离偶数节点

            if curr.next is None:
                break
            prev = curr
            curr = curr.next

        curr_even_node.next = None
        last_odd_node = curr if index % 2 else prev
        last_odd_node.next = dummy_even_head.next
        return head


if __name__ == '__main__':
    import leeco

    leeco.test('''
[1,2,3,4,5]
[2,1,3,5,6,4,7]
[]
    ''')
