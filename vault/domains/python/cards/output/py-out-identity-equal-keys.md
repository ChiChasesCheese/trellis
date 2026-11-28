---
id: py-out-identity-equal-keys
node: output.identity
type: qa
step: 2
---
## Q
**True、1 与 1.0 当键**｜读代码说输出

```python
d = {1: "a"}
d[True] = "b"
d[1.0] = "c"
print(d, len(d))
print(hash(1) == hash(True) == hash(1.0))
print(len({0, False, 0.0, ""}))
```

输出什么？

## A
**输出。**

```
{1: 'c'} 1
True
2
```

**为什么。**

- 字典判断两个键是不是同一个，看哈希值（hash）相同并且 `==` 为 True。
- `True` 是 `int` 的子类，`True == 1`，`1.0 == 1`，三者哈希也相同，所以是同一个键。
- 键保留最先插入的 `1`，值被后来的覆盖成 `'c'`。集合里 `0`、`False`、`0.0` 是同一个元素，加上 `""` 一共 2 个。

**语言为什么这样设计。**

- 数据模型规定 `a == b` 则 `hash(a) == hash(b)`；数值类型的哈希统一设计，让 `1` 和 `1.0` 可以互相查到，这样混用整数和浮点做键不会出错。
- Java 里 `Integer(1)` 和 `Double(1.0)` 不 `equals`，是两个键；JavaScript 的 `Map` 用 SameValueZero，`true` 和 `1` 是不同的键。

**怎么写才对。**

```python
d[(type(k), k)] = v   # 需要区分类型时把类型放进键
```

**面试里一句话。**

Dictionary keys match by hash and equality, and True, 1 and 1.0 are equal with the same hash, so they collapse into one key.
