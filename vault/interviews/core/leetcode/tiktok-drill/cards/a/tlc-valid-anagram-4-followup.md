---
id: tlc-valid-anagram-4-followup
node: a.valid-anagram
type: qa
step: 4
---
## Q
**LC 242 有效的字母异位词**｜追问

面试官接着问：（1）输入含 Unicode 字符时怎么调整？（2）给一组单词，把互为异位词的分到一组（LC 49）？（3）在长串 `s` 里找出 `p` 的所有异位词子串的起点（LC 438）？

## A
1. **Unicode**：`Counter` 版不用改，字典的键可以是任何字符；26 格数组版不能用。另外同一个字形可能有不同的码点序列：`"café"` 里的 `é` 写成 U+00E9（长度 4）或 `e` + U+0301 组合重音符（长度 5）时，`is_anagram("café", "face" + "́")` 是 `False`；先用 `unicodedata.normalize("NFC", ...)` 把两边规范化，结果变成 `True`。
2. **分组（LC 49）**：异位词的「规范形式」相同，用它作字典的键：`groups = defaultdict(list)`，`groups[tuple(sorted(w))].append(w)`，`O(n · L log L)`；单词很长时用 26 格计数的元组作键，`O(n · L)`。
3. **找所有异位词子串（LC 438）**：长度固定为 `len(p)` 的滑动窗口。右端进一个字符就加计数，窗口超长就把左端字符减掉；用一个变量记「计数已经对上的字符种数」，每次移动 `O(1)` 更新，整体 `O(n)`。

**Python 提醒**：字典的键必须可哈希，`sorted(w)` 返回列表，要转成 `tuple` 或 `"".join(sorted(w))` 才能当键。
