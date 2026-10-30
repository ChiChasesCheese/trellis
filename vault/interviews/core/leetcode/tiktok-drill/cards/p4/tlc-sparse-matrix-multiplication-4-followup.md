---
id: tlc-sparse-matrix-multiplication-4-followup
node: p4.sparse-matrix-multiplication
type: qa
step: 4
---
## Q
**LC 311 稀疏矩阵的乘法**｜追问

面试官接着问：（1）如果矩阵很大（行列数上万），根本存不下稠密形式，输入直接是「位置 → 值」的字典呢？（2）两个矩阵一稀一稠，循环该怎么摆？（3）结果也很稀疏时怎么输出？

## A
1. **字典输入**：把 `B` 按行号分组成 `k -> [(j, 值)]`，再对 `A` 的每个非零项 `(i, k)` 走一遍对应列表，累加到字典里。`defaultdict(int)` 省去判键。
```python
from collections import defaultdict

def multiply_coo(a: dict[tuple[int, int], int], b: dict[tuple[int, int], int]) -> dict[tuple[int, int], int]:
    rows_b: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for (k, j), v in b.items():
        rows_b[k].append((j, v))                     # 按 B 的行号分组：k -> [(列号, 值)]
    res: defaultdict[tuple[int, int], int] = defaultdict(int)
    for (i, k), x in a.items():
        for j, y in rows_b.get(k, ()):
            res[i, j] += x * y
    return {pos: v for pos, v in res.items() if v}   # 相消成 0 的项不保留
```
`A = {(0,0):1, (1,0):-1, (1,2):3}`、`B = {(0,0):7, (2,2):1}` 得 `{(0, 0): 7, (1, 0): -7, (1, 2): 3}`；`{(0,0):1,(0,1):1}` 乘 `{(0,0):1,(1,0):-1}` 得 `{}`，两项相消。时间只和非零个数及匹配对数有关，与矩阵尺寸无关。
2. **一稀一稠**：外层遍历稀疏的那个矩阵的非零项，内层再去走另一个矩阵对应行；让「稀疏的一方」决定外层，工作量就由它的非零个数控制。
3. **结果稀疏**：用字典输出，并过滤掉累加后恰好为 0 的项（正负相消）；稠密输出会重新引入 `m*n` 的空间。

**Python 提醒**：用元组 `(i, j)` 当字典键是哈希安全的；用列表当键会抛 `TypeError: unhashable type`。`res[i, j]` 是 `res[(i, j)]` 的简写。
