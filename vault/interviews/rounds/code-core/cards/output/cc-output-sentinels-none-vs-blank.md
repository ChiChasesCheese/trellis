---
id: cc-output-sentinels-none-vs-blank
node: output.sentinels
type: qa
---
## Q
Part 2 flags nothing. Three candidate outputs: the literal `NONE`, an empty line, no line at all. How do you choose, and why does the choice carry so much weight?

## A
**The empty case is a specified output, not an absence.** All three are byte-different, and graders test the empty case in every part.

- Find the sentence or the sample that names it ("print `NONE` if no account is flagged"). If none exists, choose, state the choice in a comment, and keep the alternative one line away.
- An empty line is `print("")` — one `\n`. "No line at all" writes zero bytes. A grader comparing stripped output may accept both; one comparing exactly will not.
- The sentinel is often **per section**: `REJECTED: NONE` keeps the label and replaces only the list, so a bare `NONE` fails even though the idea is right.
- Sentinels are case-sensitive and exact: `NONE`, `None`, `N/A`, `-1` are four different contracts.

## Q zh
Part 2 一个都没标记。三种候选输出：字面量 `NONE`、一个空行、完全不输出。怎么选，为什么这个选择分量这么重？

## A zh
**空结果是被规定的输出，而不是「什么都没有」。** 这三者逐字节都不同，而 grader 在每个 part 都会测空的情形。

- 找到点名它的那句话或样例（「若没有账户被标记则打印 `NONE`」）。如果没有，就自己选定、在注释里写明，并让另一种方案只差一行。
- 空行是 `print("")` —— 一个 `\n`。「完全不输出」写 0 个字节。做 strip 后比较的 grader 可能两者都收；严格比较的不会。
- 哨兵常常是**分节的**：`REJECTED: NONE` 保留标签、只替换列表，所以只打印一个 `NONE` 即使思路对也会失败。
- 哨兵区分大小写且必须精确：`NONE`、`None`、`N/A`、`-1` 是四种不同的契约。
