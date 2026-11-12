---
slug: contains-duplicate
---
## Q
**LC 217 存在重复元素（Contains Duplicate）**｜Easy

判断整数数组中是否有值出现至少两次。

## A
**一句话。** 边扫边放进集合，遇到已在集合里的就是重复。

```python
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先 `add` 再判断 `in`：第一个元素就被判成重复，`[1,2,3,4]` 错成 `True`。
- 排序后只比首尾：`[1,2,2,3]` 的重复在中间，要比每对相邻元素。

**追问。**
- 想要 `O(1)` 空间？：排序后比较相邻元素，时间 `O(n log n)`。
- 一行写法？：`len(set(nums)) < len(nums)`，但无法提前退出。

**同模式。** LC 1 两数之和、LC 242 有效的字母异位词、LC 219 存在重复元素 II、LC 220 存在重复元素 III
