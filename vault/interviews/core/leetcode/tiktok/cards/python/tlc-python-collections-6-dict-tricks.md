---
id: tlc-python-collections-6-dict-tricks
node: python.collections
type: qa
step: 6
---
## Q
**Python 工具箱｜`dict` 的几个省代码写法**

「去重但保持原顺序」「没有就建一个列表」「读不到就给默认值」分别怎么写最地道？它们的复杂度和陷阱是什么？

## A
```python
print(list(dict.fromkeys([3, 1, 3, 2, 1])))  # [3, 1, 2]：去重且保持首次出现顺序
e: dict[str, list[int]] = {}
e.setdefault("k", []).append(1)              # 没有就建空列表再追加
print(e)                                     # {'k': [1]}
seen: dict[str, int] = {}
print(seen.get("x", -1))                     # -1：读不到给默认值，且不插入
```

- `dict.fromkeys(iterable)` 利用「字典键唯一且有序」去重，`O(n)`，比 `set` 去重多保留顺序（输出要保持输入顺序的题常用，例如按首次出现顺序列出元素）。
- `setdefault(k, v)`：键不在则插入 `v` 并返回；注意 `v` 每次都会被**先求值**（`[]` 每次新建一个），热路径上改用 `defaultdict`。
- `get(k, default)` 一次完成「是否存在 + 取值」。LC 3 里的 `last.get(ch, -1) >= left` 就是这种写法。
- `d1 | d2`（3.9+）合并成新字典，`d1 |= d2` 原地合并，同键后者覆盖。
- **坑**：遍历字典时增删键会抛 `RuntimeError: dictionary changed size during iteration`；需要边遍历边改，就遍历 `list(d)` 的拷贝。
