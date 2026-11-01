---
slug: isomorphic-strings
---
## Q
**LC 205 同构字符串（Isomorphic Strings）**｜Easy

给定两个字符串 `s` 和 `t`，判断它们是否同构。如果 `s` 中的字符可以按某种映射关系替换得到 `t`，那么这两个字符串是同构的。每个出现的字符都应当映射到另一个字符，同时不改变字符的顺序；不同字符不能映射到同一个字符上，相同字符只能映射到同一个字符上，字符可以映射到自己本身。`1 <= s.length <= 5 * 10^4`，`t.length == s.length`，`s` 和 `t` 由任意有效的 ASCII 字符组成。例：`s = "egg"`，`t = "add"` → `true`；`s = "f11"`，`t = "b23"` → `false`；`s = "paper"`，`t = "title"` → `true`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 双向映射（bijection）：两张哈希表分别保证「一对一」的两个方向。

**一句话。** 逐位建立 `s -> t` 和 `t -> s` 两张映射，任何一边出现冲突就不同构。

**识别。** 「字符一一对应替换」要求映射是双射：既不能一个字符对应两个目标，也不能两个字符共用一个目标。长度 `5 * 10^4`，一遍扫 `O(n)`。

**推导。** 只建 `s -> t`：`s = "ab"`，`t = "aa"` 时 `a -> a`、`b -> a` 都不冲突，却违反「不同字符不能映射到同一个字符」。所以反方向 `t -> s` 也要建，两张表同时检查。

```python
def is_isomorphic(s: str, t: str) -> bool:
    s2t: dict[str, str] = {}     # s 的字符 -> 它必须映射成的 t 的字符
    t2s: dict[str, str] = {}     # 反向：保证不同字符不会映射到同一个字符
    for a, b in zip(s, t):
        if s2t.setdefault(a, b) != b or t2s.setdefault(b, a) != a:
            return False         # a 已经映射到别的字符，或 b 已经被别的字符占用
    return True
```

运行：`("egg", "add")` → `True`，`("f11", "b23")` → `False`，`("paper", "title")` → `True`，`("badc", "baba")` → `False`，`("a", "a")` → `True`。

**复杂度。** 时间 `O(n)`；空间 `O(Σ)`，`Σ` 是字符集大小（ASCII 至多 128）。

**拓展优化。**
- 合法映射等价于：不同的 `(a, b)` 配对数 == `s` 中不同字符数 == `t` 中不同字符数。

```python
def is_isomorphic_zip(s: str, t: str) -> bool:
    pairs = set(zip(s, t))       # 合法映射 <=> 不同的 (a, b) 对数 == 不同 a 数 == 不同 b 数
    return len(pairs) == len(set(s)) == len(set(t))
```

**易错点。**
- 只检查一个方向：`("badc", "baba")` 只用 `s -> t` 会得到 `True`（`b -> b`、`a -> a`、`d -> b`、`c -> a` 没有冲突），正确是 `False`（`b` 和 `d` 同时映射到 `b`）。
- 用 `s.index(c)` 比较首次出现位置的做法每次是 `O(n)`，整体 `O(n^2)`，`n = 5 * 10^4` 偏慢。

**同模式。** LC 290 单词规律、LC 242 有效的字母异位词、LC 383 赎金信、LC 49 字母异位词分组。
