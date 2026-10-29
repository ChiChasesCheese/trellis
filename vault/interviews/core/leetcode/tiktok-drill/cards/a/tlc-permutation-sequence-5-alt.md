---
id: tlc-permutation-sequence-5-alt
node: a.permutation-sequence
type: qa
step: 5
---
## Q
**LC 60 排列序列**｜另一种解法

`1 <= n <= 9`，`1 <= k <= n!`，有没有不推公式、几行就能写完的解法？什么时候可以用，什么时候不行？

## A
**`itertools.permutations` 跳过前 `k - 1` 个。** 对升序的输入，`permutations` 按字典序逐个产出；用 `islice` 跳过前 `k - 1` 个，取下一个即可。

```python
from itertools import islice, permutations


def get_permutation(n: int, k: int) -> str:
    perms = permutations("123456789"[:n])     # 输入升序，permutations 就按字典序产出
    return "".join(next(islice(perms, k - 1, None)))   # 跳过前 k-1 个，取第 k 个
```

`(3, 3)` → `"213"`，`(4, 9)` → `"2314"`，`(9, 362880)` → `"987654321"`（最坏情形约几毫秒）。

**怎么选。**
- `n <= 9` 时最坏要生成 `9! = 362880` 个排列，在 C 层完成，足够快；代码 3 行，几乎不会写错，适合先给出可用答案。
- 它的时间是 `O(k * n)`：`k` 随 `n!` 增长，`n = 12` 已是 `4.8 * 10^8` 级，`n = 20` 完全不可行；面试官通常正是要看你有没有阶乘进制这一步。
- 阶乘进制解法是 `O(n^2)`（甚至 `O(n log n)`），与 `k` 的大小无关，是标准答案；写出它之后再提 `islice` 做对照也可以。
