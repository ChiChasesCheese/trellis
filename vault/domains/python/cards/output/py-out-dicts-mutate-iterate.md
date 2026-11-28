---
id: py-out-dicts-mutate-iterate
node: output.dicts
type: qa
step: 2
---
## Q
**遍历时改字典**｜读代码说输出

```python
d = {"a": 1, "b": 2, "c": 3}
try:
    for k in d:
        if d[k] == 1: del d[k]
except RuntimeError as e:
    print(e)
for k in d:
    d[k] += 10
print(d)
for k in list(d):
    if d[k] == 12: del d[k]
print(d)
```

输出什么？

## A
**输出。**
```
dictionary changed size during iteration
{'b': 12, 'c': 13}
{'c': 13}
```

**为什么。**
- 迭代器记着开始时字典的大小；每走一步检查，发现大小变了就抛 RuntimeError。注意 `"a"` 已经被删掉，错误是下一步才抛出的。
- 只改值（`d[k] += 10`）不改键的个数，遍历时是安全的。
- `list(d)` 先复制出键的快照，再遍历快照去删，安全。

**语言为什么这样设计。**
- 哈希表增删键可能触发扩容、重排，迭代器的位置会失效；与其默默跳过或重复元素，不如立刻报错。
- Java 的 `HashMap` 抛 `ConcurrentModificationException`（fail-fast），同样的取舍；Go 的 `map` 允许遍历时删除，但新增的元素是否被遍历到没有保证。

**怎么写才对。**
```python
d = {k: v for k, v in d.items() if v != 1}   # 过滤：生成新字典
```

**面试里一句话。**
Changing a dict's size while iterating raises RuntimeError because the iterator can no longer trust its position; iterate over a copy or build a new dict.
