---
id: tlc-find-the-difference-4-followup
node: b.find-the-difference
type: qa
step: 4
---
## Q
**LC 389 找不同**｜追问

面试官接着问：（1）不用异或还有哪些解法？（2）`t` 里多了不止一个字符呢？（3）字符不限于小写字母（任意 Unicode）？（4）数据是流式的、放不进内存？

## A
1. **求和之差**：`sum(t) - sum(s)` 就是多出来字符的码点，一遍扫描，`O(1)` 空间；Java / C++ 里数值可能溢出，Python 不会。

```python
def find_by_sum(s: str, t: str) -> str:
    return chr(sum(map(ord, t)) - sum(map(ord, s)))
```

`find_by_sum("abcd", "abcde")` → `"e"`。
2. **多出多个字符**：求和 / 异或只能给出一个整数，不够了；改用计数差 `Counter(t) - Counter(s)`，得到每个多出字符及其次数。

```python
from collections import Counter


def extra_chars(s: str, t: str) -> Counter[str]:
    return Counter(t) - Counter(s)
```

`extra_chars("ab", "abbc")` → `Counter({'b': 1, 'c': 1})`。
3. **任意字符**：异或按码点计算，不依赖字符集大小，仍然正确；计数版也可以，只是字典代替长度 26 的数组。
4. **流式 / 大数据**：异或是在线的，一个整数边读边更新，可以同时流式读 `s` 和 `t`，不需要存下任何一个。

**Python 提醒**：`Counter` 相减只保留正数计数（负数和零被丢弃），所以 `Counter(t) - Counter(s)` 只给出 `t` 比 `s` 多出的部分；想看双向差异用 `Counter.subtract`（原地减，保留负数）；`str` 的 `+` 每次拷贝，大字符串用 `chain`。
