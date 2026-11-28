---
id: py-out-mutation-tuple-shallow
node: output.mutation
type: qa
step: 4
---
## Q
**元组里的列表与浅拷贝**｜读代码说输出

```python
t = ([1], 2)
try:
    t[0] += [9]
except TypeError as e:
    print(e)
print(t)
s = [[1, 2], [3]]
c = s[:]
c[0].append(99)
c.append([4])
print(s)
```

输出什么？

## A
**输出。**

```
'tuple' object does not support item assignment
([1, 9], 2)
[[1, 2, 99], [3]]
```

**为什么。**

- `t[0] += [9]` 分三步：取出 `t[0]`，对列表原地 `+=`（成功了，列表已变成 `[1, 9]`），再把结果赋回 `t[0]`——这一步元组不允许，抛 TypeError。
- 所以报了错，但列表已经被改了。
- `s[:]` 只复制外层列表，内层的 `[1, 2]` 仍是同一个对象：`append(99)` 两边都看见，而给 `c` 追加新元素 `[4]` 不影响 `s`。

**语言为什么这样设计。**

- 元组的不可变指「每个位置的引用不能换」，不是「引用的对象不能变」；增强赋值（augmented assignment）规定目标只求值一次，先运算后存回，所以「先改后报错」是语言定义的结果。
- 切片只做浅拷贝，因为深拷贝要处理循环引用和自定义对象，代价大、语义复杂，所以放进显式的 `copy.deepcopy`。

**怎么写才对。**

```python
t[0].extend([9])           # 不会报错
import copy; c = copy.deepcopy(s)
```

**面试里一句话。**

Tuples are immutable only in which objects they hold, so a list inside can still change, and a slice copy is shallow so nested lists stay shared.
