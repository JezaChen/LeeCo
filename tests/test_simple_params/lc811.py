import typing
from typing import List
from collections import defaultdict


class Solution:
    def subdomainVisits(self, cpdomains: List[str]) -> List[typing.AnyStr]:
        cnt_map = defaultdict(int)
        for domain_info in cpdomains:
            cnt, domain = domain_info.split(' ')
            cnt = int(cnt)
            while True:
                cnt_map[domain] += cnt
                next_dot_pos = domain.find('.')
                if next_dot_pos == -1:
                    break
                domain = domain[next_dot_pos + 1:]
        return [
            f'{cnt} {domain}' for domain, cnt in cnt_map.items()
        ]


# leetcode submit region end(Prohibit modification and deletion)

if __name__ == '__main__':
    import leeco

    leeco.test("""
["9001 discuss.leetcode.com"]
["900 google.mail.com", "50 yahoo.com", "1 intel.mail.com", "5 wiki.org"]
    """)
