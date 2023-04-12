class Solution:
    def mySqrt(self, x: int) -> int:
        l, r, ans = 0, x, -1
        print(l, r, ans)
        while l <= r:
            mid = (l + r) // 2
            if mid * mid <= x:
                ans = mid
                l = mid + 1
                print(l, r, ans)
            else:
                r = mid - 1
                print(l, r, ans)
        return ans


if __name__ == "__main__":
    x = Solution()
    print(x.mySqrt(9))
