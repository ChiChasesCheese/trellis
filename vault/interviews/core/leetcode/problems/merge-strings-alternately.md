---
slug: merge-strings-alternately
---
## Q
**LC 1768 交替合并字符串**｜Easy

给你两个字符串 `word1` 和 `word2`。从 `word1` 开始，通过交替添加字母来合并字符串；如果一个字符串比另一个长，就把多出来的字母追加到合并结果的末尾。返回合并后的字符串。`1 <= word1.length, word2.length <= 100`，只含小写英文字母。例：`"abc"`, `"pqr"` → `"apbqcr"`；`"ab"`, `"pqrs"` → `"apbqrs"`；`"abcd"`, `"pq"` → `"apbqcd"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 两个序列同步前进的双指针（`zip` 惯用法）+ 处理长度不等的尾巴。

**一句话。** 两个下标一起走，到较短者的长度为止交替取字符，然后把较长者剩下的部分整体接上。

**识别。** 「交替 / 逐位合并两个序列」= 两个指针同步前进；`n <= 100`，任何线性写法都够。

**推导。** 直接写 `while i < len(a) or j < len(b)`，里面再各判一次越界，容易漏。把问题拆开：公共长度 `n = min(len(a), len(b))` 内严格交替，之后只有一个串有剩余，切片 `a[n:]`、`b[n:]` 里必有一个是空串，直接都接上，不需要判断谁更长。

```python
def merge_alternately(word1: str, word2: str) -> str:
    n = min(len(word1), len(word2))
    head = "".join(a + b for a, b in zip(word1, word2))  # 两个指针同步前进，交替各取一个；zip 到较短者结束
    return head + word1[n:] + word2[n:]  # 较长者剩下的尾巴原样接上（另一个切片是空串）
```

运行：`("abc", "pqr")` → `"apbqcr"`；`("ab", "pqrs")` → `"apbqrs"`；`("abcd", "pq")` → `"apbqcd"`。

**复杂度。** 时间 `O(n + m)`，空间 `O(n + m)`（结果串）。

**拓展优化。**
- 更短的写法：`"".join(x + y for x, y in zip_longest(a, b, fillvalue=""))`（`itertools.zip_longest`），长度不等的尾巴由 `fillvalue` 补空串；本质一样，面试里先写上面的版本更容易讲清楚。

**易错点。**
- 忘记追加尾巴：`("ab", "pqrs")` 只得到 `"apbq"`，正确是 `"apbqrs"`。
- 用 `+=` 在循环里反复拼接字符串，在长输入下是 `O(n^2)` 的隐患，应该 `"".join(...)`。

**追问。**
- 交替合并 `k` 个字符串：`"".join(c for tup in zip_longest(*words, fillvalue="") for c in tup)`，按「列」轮流取，`O(总长)`。
- 输入是很长的流或迭代器：写成生成器，逐字符产出，不必把结果整个放进内存。

**同模式。** LC 392 判断子序列、LC 88 合并两个有序数组、LC 21 合并两个有序链表、LC 2 两数相加。
