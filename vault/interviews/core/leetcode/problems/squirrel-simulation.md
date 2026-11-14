---
slug: squirrel-simulation
---
## Q
**LC 573 松鼠模拟**｜Medium

网格上有一棵树、一只松鼠和若干坚果；松鼠每次只能带一颗坚果回树。求收完所有坚果的最小曼哈顿总距离。

## A
**一句话。** 除第一颗外每颗都是「树 → 坚果 → 树」，基准是 `Σ 2·d(树, 坚果)`；第一颗把一段 `d(树, 坚果)` 换成 `d(松鼠, 坚果)`，选节省最多的那颗。

```python
def min_distance(height, width, tree, squirrel, nuts):
    def d(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    total = sum(2 * d(tree, n) for n in nuts)
    save = max(d(tree, n) - d(squirrel, n) for n in nuts)
    return total - save          # 第一颗从松鼠出发
```

**复杂度。** 时间 `O(k)`，空间 `O(1)`，`k` 为坚果数。

**易错点。**
- 选离松鼠最近的坚果先拿：要比较的是「省下多少」，`d(树) - d(松鼠)` 最大才对。
- `save` 初值设 `0`：节省可能是负数（每颗都离松鼠更远），也必须先拿一颗。

**追问。**
- 为什么只有第一颗特殊？：拿完第一颗后松鼠就在树下，之后每颗都是来回。
- 松鼠一次能带两颗？：变成配对问题，要考虑「树 → a → b → 树」的组合，复杂得多。

**同模式。** LC 1266 访问所有点的最小时间
