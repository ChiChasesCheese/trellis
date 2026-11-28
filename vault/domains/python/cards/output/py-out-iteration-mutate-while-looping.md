---
id: py-out-iteration-mutate-while-looping
node: output.iteration
type: qa
step: 3
---
## Q
**遍历时删除**｜读代码说输出

```python
a = [2, 4, 6, 1]
for x in a:
    if x % 2 == 0:
        a.remove(x)
print(a)
b = [2, 4, 6, 1]
for x in b[:]:
    if x % 2 == 0:
        b.remove(x)
print(b)
```

输出什么？

## A
**输出。**

```
[4, 1]
[1]
```

**为什么。**

- 列表的迭代器只记一个下标，每轮取 `a[下标]` 再加 1。
- 删掉 `2` 后，后面的元素整体前移，`4` 落到下标 0，而迭代器已经指向下标 1，所以 `4` 被跳过；接着删掉 `6`，下标 2 超出长度，循环结束。
- 遍历副本 `b[:]` 时，被遍历的列表不变，每个元素都被检查到。

**语言为什么这样设计。**

- 列表迭代器只存下标、不检查修改，是为了让迭代是 O(1) 且没有额外状态；字典和集合则会检测大小变化并抛 `RuntimeError`。
- Java 的 `ArrayList` 迭代器是 fail-fast，抛 `ConcurrentModificationException`；Python 的列表选择了不管，所以悄悄出错。

**怎么写才对。**

```python
a = [x for x in a if x % 2]   # 重新生成，不要边遍历边改
```

**面试里一句话。**

Removing items from a list while iterating shifts the remaining elements under the iterator's index, so some are skipped; build a new list instead.
