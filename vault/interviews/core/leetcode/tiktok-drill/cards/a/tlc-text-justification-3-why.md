---
id: tlc-text-justification-3-why
node: a.text-justification
type: qa
step: 3
---
## Q
**LC 68 文本左右对齐**｜正确性

断行条件 `used + 1 + len(words[j]) <= max_width` 为什么这样写？排版时 `(k < r)` 为什么能保证"左边的空档多"？最后一行和单词独占的行为什么要单独处理？各给一个出错的具体输出。

## A
**断行不变量。** `used` 等于当前行已放单词的总长加上它们之间各放一个空格的长度，也就是这一行**最紧凑**时的宽度。再放下一个单词需要多 `1 + len(word)`，不超过 `max_width` 才放。这和贪心"每行尽可能多放单词"的要求一致，排版阶段只会往空档里补空格，不会再改变断行。

**均分不变量。** 一行有 `gaps` 个空档、`spaces` 个空格。`q, r = divmod(spaces, gaps)` 后，每个空档放 `q` 个，剩下 `r` 个空格（`0 <= r < gaps`）分给前 `r` 个空档各一个。判断 `k < r`，`k` 是从 0 开始的空档序号，前 `r` 个为真，所以多出来的空格都落在左边。总数 `gaps * q + r = spaces`。

**特殊行。** 最后一行规定左对齐、单词间只有一个空格，如果也用均分，会被拉伸。单词独占的行没有空档，`gaps = 0`，`divmod` 会抛 `ZeroDivisionError`，规则本身也规定左对齐。

**反例一：最后一行也均分。** 示例二 `["What","must","be","acknowledgment","shall","be"]`，`16`：最后一行 `["shall","be"]` 被拉伸成 `"shall         be"`，正确是 `"shall be        "`。

**反例二：余数给右边。** 示例一第二行 `["example","of","text"]` 有 `3` 个空格、`2` 个空档，正确是 `"example  of text"`（左边 2 个，右边 1 个）；若让后面的空档多，得到 `"example of  text"`。
