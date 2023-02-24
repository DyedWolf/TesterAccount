"""
给你一个数组 nums和一个值 val，你需要 原地 移除所有数值等于val的元素，并返回移除后数组的新长度。

不要使用额外的数组空间，你必须仅使用 O(1) 额外空间并 原地 修改输入数组。

元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。



说明:

为什么返回数值是整数，但输出的答案是数组呢?

请注意，输入数组是以「引用」方式传递的，这意味着在函数里修改输入数组对于调用者是可见的。

你可以想象内部操作如下:

// nums 是以“引用”方式传递的。也就是说，不对实参作任何拷贝
int len = removeElement(nums, val);

// 在函数里修改输入数组对于调用者是可见的。
// 根据你的函数返回的长度, 它会打印出数组中 该长度范围内 的所有元素。
for (int i = 0; i < len; i++) {
  print(nums[i]);
}


示例 1：

输入：nums = [3,2,2,3], val = 3
输出：2, nums = [2,2]
解释：函数应该返回新的长度 2, 并且 nums 中的前两个元素均为 2。你不需要考虑数组中超出新长度后面的元素。例如，函数返回的新长度为 2 ，而 nums = [2,2,3,3] 或 nums = [2,2,0,0]，也会被视作正确答案。



"""

from typing import List


# class Solution:
#     def removeElement(self, nums: List[int], val: int) -> int:
#         result = 0
#         for i in range(len(nums)):
#             if nums[i] != val:
#                 nums[result] = nums[i]
#                 result += 1
#         print(result)
#         return result

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:

        nums1 = [3, 2, 2, 3]
        nums1.remove(2)
        print(nums1)

        i = 0
        result = nums
        while i < len(nums):
            if nums[i] == val:
                result.remove(nums[i])
            i += 1
        print(result)
        return len(result)





if __name__ == "__main__":
    nums = [3, 2, 2, 3]
    val = 3
    solution = Solution()
    solution.removeElement(nums, val)
