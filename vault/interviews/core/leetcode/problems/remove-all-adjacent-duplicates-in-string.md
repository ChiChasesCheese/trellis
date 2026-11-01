---
slug: remove-all-adjacent-duplicates-in-string
---
## Q
**LC 1047 删除字符串中的所有相邻重复项**｜Easy

给出由小写字母组成的字符串 `s`，重复项删除操作会选择两个相邻且相同的字母并删除它们。在 `s` 上反复执行该操作，直到无法继续，返回最终的字符串（答案唯一）。`1 <= s.length <= 10^5`，`s` 仅由小写英文字母组成。例：`"abbaca"` → `"ca"`（先删 `bb` 得 `"aaca"`，再删 `aa`）；`"azxxzy"` → `"ay"`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 栈（stack）：删除会让左右两侧重新相邻，用栈顶维护"当前已处理部分的末尾"。

**一句话。** 逐字符入栈，当前字符与栈顶相同就弹栈（两个一起消掉），否则入栈，最后栈里的字符拼起来就是答案。

**识别。** 「反复删除相邻的成对项」「删除后左右合拢，可能产生新的相邻对」= 栈，类似括号匹配；`n = 10^5` 要求 `O(n)`，不能反复 `replace`。

**推导。** 暴力：循环地找相邻相同对并删除，直到找不到，每轮 `O(n)`，最多 `n/2` 轮，`O(n^2)`。删除只影响"已处理部分的末尾"和"下一个字符"的相邻关系，所以只要始终保留已处理部分化简后的结果，新来的字符只需和它的末尾比较，这个结构就是栈。

```python
def remove_duplicates(s: str) -> str:
    stack: list[str] = []  # 已处理部分化简后的结果，栈顶是它的最后一个字符
    for c in s:
        if stack and stack[-1] == c:
            stack.pop()  # 与栈顶相同：这一对相邻重复项一起删掉，栈顶之前的字符重新露出来
        else:
            stack.append(c)
    return ''.join(stack)
```

运行：`"abbaca"` → `"ca"`；`"azxxzy"` → `"ay"`；`"abccba"` → `""`；`"a"` → `"a"`。

**复杂度。** 时间 `O(n)`（每个字符最多入栈、出栈各一次），空间 `O(n)`。

**拓展优化。**
- 删除 `k` 个相邻相同字符（LC 1209，`k >= 2`）：栈里存 `(字符, 连续个数)`，个数达到 `k` 就整组弹出：

```python
def remove_duplicates_k(s: str, k: int) -> str:
    stack: list[tuple[str, int]] = []  # (字符, 栈顶这一段的连续个数)
    for c in s:
        if stack and stack[-1][0] == c:
            ch, cnt = stack.pop()
            if cnt + 1 < k:  # 还没凑够 k 个，放回去；凑够就整段不放回
                stack.append((ch, cnt + 1))
        else:
            stack.append((c, 1))
    return ''.join(ch * cnt for ch, cnt in stack)
```

**易错点。**
- 只扫一遍、遇到相邻相同就跳过两个：`"abbaca"` 得到 `"aaca"`，正确是 `"ca"`，删 `bb` 后产生的新相邻对 `aa` 被漏掉；`"azxxzy"` 得到 `"azzy"`，正确是 `"ay"`。
- 没判断栈是否为空就读 `stack[-1]`：第一个字符就 `IndexError`；条件必须是 `stack and stack[-1] == c`。
- 全部被删光（`"aa"`、`"abccba"`）时结果是 `""`，`''.join([])` 自然成立，不要特判成别的值。

**同模式。** LC 1209 删除字符串中的所有相邻重复项 II、LC 20 有效的括号、LC 844 比较含退格的字符串、LC 394 字符串解码。
