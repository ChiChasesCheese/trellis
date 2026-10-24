---
id: tlc-compare-version-numbers-4-followup
node: a.compare-version-numbers
type: qa
step: 4
---
## Q
**LC 165 比较版本号**｜追问

面试官接着问：（1）不想用 `split` 产生额外的列表，能不能 `O(1)` 额外空间？（2）如果修订号可能超过 64 位，其他语言没有大整数怎么办？（3）版本号里带 `-beta`、`rc1` 这类预发布标记呢？

## A
1. **双指针原地解析**：两个下标 `i`、`j` 分别指向两个字符串。每轮从当前位置读到下一个 `.` 或末尾，边读边累加成整数 `x`、`y`，比较后两个下标各跳过 `.`。某个字符串读完后，`x` 保持 `0`，相当于补 `0`。空间 `O(1)`。

```python
def compare_version_o1(version1: str, version2: str) -> int:
    i = j = 0
    n, m = len(version1), len(version2)
    while i < n or j < m:
        x = 0
        while i < n and version1[i] != ".":
            x = x * 10 + int(version1[i])
            i += 1
        y = 0
        while j < m and version2[j] != ".":
            y = y * 10 + int(version2[j])
            j += 1
        if x != y:
            return -1 if x < y else 1
        i, j = i + 1, j + 1
    return 0
```

2. **超长修订号**：不转成整数，先去掉前导零，再比较**长度**（位数多的更大），长度相同再比较字符串（此时字典序等于数值序）。Python 的 `int` 是任意精度，不需要这样做。
3. **预发布标记**：规则变成语义化版本（SemVer）：主、次、补丁三段按数值比较，预发布标记再按标识符比较，没有标记的版本比有标记的更大。应当使用成熟的库实现，面试里说明规则即可。

**Python 提醒**：`"1..2".split(".")` 会得到 `['1', '', '2']`，`int('')` 抛 `ValueError`；输入保证是有效版本号，不会出现，但处理用户输入时要先校验。`str.split(".")` 不带 `maxsplit` 时返回所有段。
