---
slug: array-wrapper
---
## Q
**LC 2695 包装数组**｜Easy

（原题为 JavaScript，这里用 Python。）实现类 `ArrayWrapper`，构造时传入整数数组。两个实例相加（`+`）得到两个数组所有元素之和；转成字符串（`str`）得到形如 `"[1,2,3]"` 的结果（逗号后无空格）。

## A
**一句话。** 重载运算符：`__add__` 返回两个数组和的和，`__str__` 把元素用逗号连接后加方括号。

```python
class ArrayWrapper:
    def __init__(self, nums):
        self.nums = nums

    def __add__(self, other):
        return sum(self.nums) + sum(other.nums)

    def __str__(self):
        return '[' + ','.join(map(str, self.nums)) + ']'
```

**复杂度。** `__add__` 与 `__str__` 均 `O(n)`。

**易错点。**
- 用 `str(list)`：它在逗号后带空格，`"[1, 2, 3]"` 与要求不符。
- `__add__` 返回实例：题目要求加出来的是数字。

**追问。**
- 要支持 `sum(wrappers)` 吗？：再加一个 `__radd__`，处理 `0 + wrapper`。

**同模式。** LC 2694 事件发射器、LC 2627 函数防抖、LC 2636 Promise 对象池、LC 1472 设计浏览器历史记录
