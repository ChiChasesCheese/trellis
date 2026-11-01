---
id: tlc-tops-using-a-robot-to-print-the-lexicographically-smallest-string-0-whole
node: stack.using-a-robot-to-print-the-lexicographically-smallest-string
type: qa
---
## Q
**LC 2434 使用机器人打印字典序最小的字符串（Using a Robot to Print the Lexicographically Smallest String）**｜Medium · 全公司热度第 187 名

给你一个字符串 `s` 和一个机器人，机器人当前有一个空字符串 `t`。执行以下操作之一，直到 `s` 和 `t` 都变成空字符串：(1) 删除 `s` 的第一个字符，机器人把它添加到 `t` 的尾部；(2) 删除 `t` 的最后一个字符，机器人把它写到纸上。返回纸上能写出的字典序最小的字符串。`1 <= s.length <= 10^5`，`s` 只包含小写英文字母。例：`s = "zza"` → `"azz"`；`s = "bac"` → `"abc"`；`s = "bdda"` → `"addb"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 栈（`t` 就是一个栈）+ 后缀最小值（suffix minimum）的贪心。

**一句话。** `s` 的字符依次入栈；每次入栈后，只要栈顶字符不大于 `s` 剩余部分的最小字符，就把它写到纸上，否则继续入栈。

**识别。** 「只能从一端放入、同一端取出」就是栈，输出序列是入栈序列经过栈的重排。「字典序最小」说明每一步都要写当前能写的最小字符。`n = 10^5`，要 `O(n)` 或 `O(n log n)`。

**推导。** 枚举所有入栈出栈顺序指数级。贪心：栈顶字符 `c` 能不能现在写？如果 `s` 里还有比 `c` 更小的字符，写 `c` 会让更小的字符排到后面，不划算，应继续入栈直到小字符进入栈再写；如果 `c` 不大于 `s` 剩余所有字符，现在写它不会吃亏（栈里更深的字符都在它前面入栈，已经被它压住，要先写它）。「`s` 剩余部分的最小字符」预处理成后缀最小值数组。

```python
def robot_with_string(s: str) -> str:
    n = len(s)
    suffix_min = ["{"] * (n + 1)              # suffix_min[i] = min(s[i:])；'{' 比 'z' 大，当哨兵
    for i in range(n - 1, -1, -1):
        suffix_min[i] = min(s[i], suffix_min[i + 1])
    paper: list[str] = []
    t: list[str] = []                         # 栈 t：只能从栈顶写出
    for i, ch in enumerate(s):
        t.append(ch)                          # 操作一：s 的首字符入栈
        while t and t[-1] <= suffix_min[i + 1]:    # 栈顶不比 s 剩余部分的任何字符大：现在写它不亏
            paper.append(t.pop())             # 操作二
    return "".join(paper)
```

运行：`"zza"` → `"azz"`，`"bac"` → `"abc"`，`"bdda"` → `"addb"`，`"a"` → `"a"`，`"cba"` → `"abc"`。

**复杂度。** 时间 `O(n)`：每个字符入栈出栈各一次；空间 `O(n)`。

**易错点。**
- 只和下一个字符 `s[i + 1]` 比较，而不是和整个后缀的最小值比：`"bdda"` 会输出 `"bdad"`，正确 `"addb"`。
- 哨兵必须比所有小写字母都大：最后一个字符入栈时，靠它把整个栈弹空。把哨兵换成 `"a"`，`"zza"` 只输出 `"a"`，栈里剩下的两个 `z` 没有写出，正确 `"azz"`。

**同模式。** LC 402 移掉 K 位数字、LC 316 去除重复字母、LC 155 最小栈、LC 946 验证栈序列。
