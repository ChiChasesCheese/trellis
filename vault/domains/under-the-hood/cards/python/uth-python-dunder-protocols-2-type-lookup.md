---
id: uth-python-dunder-protocols-2-type-lookup
node: python.dunder-protocols
type: qa
step: 2
---
## Q
**给对象单独挂 __len__ 为什么没用**｜Python · CPython 3.14

`c = C(); c.__len__ = lambda: 5` 之后，`len(c)` 会得到 5 吗？

## A
**背景。** 普通属性查找是先看对象自己的字典，再看它的类。照这个思路，往实例上挂一个同名函数，应该能盖过类里的才对。

**结构。** `len(c)` 这类隐式调用只在**类**上找特殊方法，完全不看实例字典。实现上，类里定义的 `__len__` 会被装进这个类型的「长度槽位」（`sq_length`），槽位里的转接函数用 `type(c)` 去查 `__len__`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="8" y="30" width="140" height="56" rx="3" stroke-dasharray="4,3"/>
<rect x="125" y="125" width="90" height="30" rx="3"/>
<line x1="150" y1="125" x2="95" y2="88" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="192" y="30" width="140" height="56" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="190" y1="125" x2="250" y2="88"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="95.0,88.0 101.7,88.9 98.3,93.8"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="250.0,88.0 246.5,93.7 243.3,88.6"/>
</g>
<g fill="currentColor">
<text x="262" y="50">type(c) = C (类)</text>
<text x="262" y="72" font-size="11">没有 __len__</text>
<text x="170" y="144">len(c)</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="78" y="50">c.__dict__ (实例)</text>
<text x="78" y="72" font-size="11">__len__ = lambda</text>
<text x="98" y="112" font-size="11">不看</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="170" y="180">结果: TypeError</text>
</g>
</g>
</svg>
```

```python
class C: pass
c = C()
c.__len__ = lambda: 5
len(c)        # TypeError: object of type 'C' has no len()
c.__len__()   # 5，显式写出来才会查实例字典
```

**为什么。** 如果隐式调用也先看实例字典，作用在类型对象自己身上的调用就会出错：`hash(int)` 会去 `int` 的字典里找 `__hash__`，把它当成一个缺少参数的实例方法。只认类，规则统一，也少一次字典查找。

**坑。** 想在测试里替换某个对象的 `len(obj)` 或 `str(obj)`，要改它的类，而不是实例。

**对应 LeetCode：** 无直接对应的题
