---
id: tlc-group-anagrams-4-followup
node: b.group-anagrams
type: qa
step: 4
---
## Q
**LC 49 字母异位词分组**｜追问

面试官接着问：（1）字符不止小写字母，含 Unicode，键怎么做？（2）排序键和计数键各自适合什么场景？（3）数据量大到放不进内存怎么办？

## A
1. **任意字符集**：计数数组放不下，改成按需计数。
```python
from collections import Counter

def key_of(s: str) -> frozenset[tuple[str, int]]:
    return frozenset(Counter(s).items())
```
   `Counter(s).items()` 里是 `(字符, 次数)` 对，转 `frozenset` 后与顺序无关、可哈希。
2. **排序键 vs 计数键**：`"".join(sorted(s))` 一行写完，`O(L log L)`，字符集不限，面试里先写它最稳；计数键 `O(L + Σ)`，`Σ` 是字符集大小，`L` 远大于 `Σ`（这里 `L = 100`、`Σ = 26`）时更优，但字符集大时每个键要存 `Σ` 个数，反而更费空间。
3. **放不进内存**：键的哈希值取模分桶，把同一个桶的串写到同一个文件；桶内再用内存哈希分组。同组的串一定落在同一个桶，不会跨桶漏掉。

**Python 提醒**：不要用「字母的 ASCII 值求和」或「素数乘积」当键：和相同的不同字母组合（`"ad"` 与 `"bc"` 的和都是 `197`）会碰撞，素数乘积在长串上会变成大整数，慢且容易写错。
