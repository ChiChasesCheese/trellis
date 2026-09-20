---
id: python-data-model-eq-hash-form
node: python.data-model
type: qa
step: 3
tags: [grown]
---
## Q
写一个正确的 `__eq__`/`__hash__` 实现时，为什么类型不匹配要返回 `NotImplemented` 而不是直接返回 `False`？

## A
返回 `NotImplemented` 会让解释器转去尝试对方对象的反射方法（`other.__eq__(self)`），给它一个说“我也不认识这个类型”的机会；直接返回 `False` 相当于武断宣称“不相等”，可能压制了对方类型本可以提供的正确比较。
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return (self.x, self.y) == (other.x, other.y)
    def __hash__(self):
        return hash((self.x, self.y))
```
