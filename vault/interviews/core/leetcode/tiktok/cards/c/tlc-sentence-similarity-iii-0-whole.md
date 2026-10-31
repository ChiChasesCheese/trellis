---
id: tlc-sentence-similarity-iii-0-whole
node: c.sentence-similarity-iii
type: qa
---
## Q
**LC 1813 句子相似性 III**｜Medium · LC TikTok 全时段热度 41/100

句子是由单个空格分隔的单词序列，首尾没有多余空格，单词只含大小写英文字母。若能往其中一个句子里插入一个任意句子（可以为空）得到另一个句子，则两句相似；插入的句子必须与已有单词用空格隔开。给定 `sentence1`、`sentence2`，判断是否相似。`1 <= sentence1.length, sentence2.length <= 100`。例：`"My name is Haley"` 与 `"My Haley"` → `true`（在 `My` 和 `Haley` 之间插入 `name is`）；`"of"` 与 `"A lot of words"` → `false`；`"Eating right now"` 与 `"Eating"` → `true`（在结尾插入）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按单词切开，较短的句子必须是较长句子的「前缀 + 后缀」，双指针分别数出最长公共前缀和最长公共后缀，两者之和覆盖整个短句即可。

**识别。** 「只能在一处插入一段」等价于「短句 = 长句头部一截 + 长句尾部一截」。看到「插入 / 删除一段」想前缀后缀匹配，不要想编辑距离。

**推导。** 暴力：枚举短句从哪里断开，逐段比较，`O(m^2)`。浪费：前缀匹配得越长越好，后缀也是，二者互不干扰，只要不重叠。洞察：先尽量吃前缀，再在剩下的词里尽量吃后缀；`i + j == m` 说明短句被完全认领。

```python
def are_sentences_similar(sentence1: str, sentence2: str) -> bool:
    short, long = sorted((sentence1.split(), sentence2.split()), key=len)
    m = len(short)
    i = 0
    while i < m and short[i] == long[i]:         # 从头匹配的最长公共前缀
        i += 1
    j = 0
    while j < m - i and short[-1 - j] == long[-1 - j]:   # 从尾匹配，且不能和前缀重叠
        j += 1
    return i + j == m                            # 短句每个词都被前缀或后缀认领，中间缺的就是插入的句子
```

运行：`"My name is Haley"`, `"My Haley"` → `True`；`"of"`, `"A lot of words"` → `False`；`"Eating right now"`, `"Eating"` → `True`；`"Frog cool"`, `"Frogs are cool"` → `False`；`"a b a"`, `"a"` → `True`。

**复杂度。** 时间 `O(m + n)`（切词与扫描），空间 `O(m + n)`。

**拓展优化。**
- 不拆词、不排序，直接用 `collections.deque` 从两端同时弹出相同的词，写法等价，空间同样 `O(m + n)`。
- 允许在多处插入时问题变成「短句是否是长句的子序列」（`LC 392`）。

**易错点。**
- 按字符而不是按单词比较：`"Frog cool"` 与 `"Frogs are cool"` 按字符前缀会误判为 `true`，必须先 `split()`。
- 后缀指针不限制到 `m - i`：`"a b a"` 与 `"a"` 里前缀已吃掉 `a`，后缀再吃一次会重复计数；上限 `m - i` 防止前后缀重叠。
- 忘记交换长短：短句更长时下标 `long[i]` 越界。

**追问。**
- 返回被插入的那一段：`long[i : n - j]`。
- 同义词版本（`LC 737`）：把「词相等」换成并查集里的「同一集合」，其余不变。

**同模式。** LC 392 判断子序列、LC 14 最长公共前缀、LC 734 句子相似性、LC 737 句子相似性 II、LC 125 验证回文串。
