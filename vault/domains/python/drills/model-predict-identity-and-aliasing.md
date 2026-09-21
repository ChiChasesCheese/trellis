---
nodes: [model.names-objects, model.mutability, model.copy, model.hash-eq, model.dict-set-internals, classes.operator-overloading]
tags: [drill, interview]
---
# Drill：六段代码，逐段预测输出并解释机制

依次给出六段独立的小代码。每段先自己在纸上写出预测输出，再运行验证，说不出「为什么」不算过关。

**限制与要求**
- 不许在读题时先跑代码；先写出预测输出，再解释机制，最后才验证。
- 每段限时 2 分钟想清楚机制，想不出来就承认卡住、进入下一段，面试官不会给你无限时间。
- 解释里必须用对术语：identity vs value、就地修改 vs 重新绑定、可哈希（hashable）。
- 不能只说「这是 Python 的坑」——要说出具体是哪个机制导致的。

**分关要求**（六段各自独立，逐段做完再看下一段）
- 第 1 段（`is` vs `==`）：
  ```python
  x = [1, 2, 3]
  y = [1, 2, 3]
  print(x is y, x == y)
  ```
- 第 2 段（可变默认参数）：
  ```python
  def append_item(item, acc=[]):
      acc.append(item)
      return acc

  print(append_item(1))
  print(append_item(2))
  ```
- 第 3 段（`+=` 在 tuple 里的 list）：
  ```python
  t = ([1, 2], 3)
  try:
      t[0] += [4]
  except TypeError as e:
      print("caught:", type(e).__name__)
  print(t)
  ```
- 第 4 段（浅拷贝）：
  ```python
  matrix = [[1, 2], [3, 4]]
  shallow = matrix.copy()
  shallow[0].append(99)
  print(matrix)
  ```
- 第 5 段（`__eq__` 无 `__hash__` 做键）：
  ```python
  class Point:
      def __init__(self, x, y):
          self.x, self.y = x, y
      def __eq__(self, other):
          return (self.x, self.y) == (other.x, other.y)

  p = Point(1, 2)
  s = {p}
  ```
- 第 6 段（dict 插入序）：
  ```python
  d = {}
  d["b"] = 1
  d["a"] = 2
  d["c"] = 3
  del d["a"]
  d["a"] = 4
  print(list(d.keys()))
  ```

**评分点（强答案会命中）**
- `is` 比较身份（identity）、`==` 调用 `__eq__` 比较值；两个字面量各自新建对象，身份必然不同 [[is-vs-eq-identity-value]] [[elevator-pitch-is-vs-eq]]
- 默认参数只在 `def` 执行时求值一次，`[]` 是可变对象，之后每次省略该参数都复用同一个对象 [[mutable-default-argument-trap]]
- `t[0] += [4]` 先算 `t[0].__iadd__([4])`——list 原地追加已经生效并返回自身，再把结果赋回 `t[0]` 才因为 tuple 不支持 `__setitem__` 抛 `TypeError`，呈现「报错但列表已经变了」 [[iadd-tuple-of-list-partial-mutation-trap]]
- `matrix.copy()` 只新建外层 list，内层两个子 list 仍是原对象的引用，`shallow[0].append(99)` 是就地修改，两边都能看到 [[shallow-copy-nested-list-pitfall]] [[shallow-vs-deep-copy-definition]]
- 重写 `__eq__` 而不重写 `__hash__` 会让解释器把该类的 `__hash__` 隐式设为 `None`，实例不可哈希，放进 `set` 直接抛 `TypeError` [[hash-eq-contract-basic]] [[override-eq-implicit-hash-none]]
- dict 拆分表由 key-table + 独立的 values 数组组成，删除只是用哨兵 `<dummy>` 占位维持探测链不断裂而不是立刻紧缩，所以先删后插的键会被追加到表尾而不是回到原来的位置 [[dict-three-part-data-layout]] [[split-table-key-null-vs-dummy-null]]

**参考答案**
1. `False True`——`x`、`y` 是两次独立的列表字面量，`id(x) != id(y)`，但内容相同故 `==` 为真。
2. `[1]` 然后 `[1, 2]`——第二次调用打印的是 `[1, 2]`，因为 `acc` 是模块加载时创建的同一个 list，两次调用都在往它上面追加。
3. 打印 `caught: TypeError`，随后 `t` 变成 `([1, 2, 4], 3)`——list 的 `__iadd__` 已经把 `4` 追加进去并返回自身，只是把这个结果重新绑定回 `t[0]` 这一步因为 tuple 不支持赋值才报错，副作用已经不可逆。
4. `[[1, 2, 99], [3, 4]]`——浅拷贝没有复制内层子 list。
5. 抛出 `TypeError: unhashable type: 'Point'`——`Point` 定义了 `__eq__` 却没定义 `__hash__`，`__hash__` 被隐式设为 `None`。
6. `['b', 'c', 'a']`——`'a'` 被删除时原槽位留下 dummy 占位，重新插入的 `'a'` 是一次新的插入，追加到 entries 表尾，不会跳回它原来的位置。

**尝试记录**
| 日期 | 用时 | 卡在哪 | 下次 |
|---|---|---|---|
