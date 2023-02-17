from typing import List

from django.test import TestCase


# Create your tests here.


class Solution:
    def giveGem(self, gem: List[int], operations: List[List[int]]) -> int:
        # for op in operations:
        #     send = gem[op[0]]//2
        #     gem[op[0]] -= send
        #     gem[op[1]] += send
        # gem.sort()
        # return gem[-1]-gem[0]

        for op in operations:
            num = gem[op[0]] // 2
            gem[op[0]] = gem[op[0]] - num
            gem[op[1]] = gem[op[1]] + num
        gem.sort()
        print(gem)
        return gem[-1] - gem[0]


if __name__ == '__main__':
    gem = [100, 0, 50, 100]
    operations = [[0, 2], [0, 1], [3, 0], [3, 0]]
    s = Solution()
    print(s.giveGem(gem, operations))
