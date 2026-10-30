---
id: tlc-letter-combinations-of-a-phone-number-3-why
node: p4.letter-combinations-of-a-phone-number
type: qa
step: 3
---
## Q
**LC 17 电话号码的字母组合**｜正确性

回溯解法里 `path.pop()` 维护的不变量是什么？去掉它，或者收集答案时不 `join`，分别会得到什么错误输出？

## A
**不变量。** 进入 `dfs(i)` 时，`path` 恰好是前 `i` 个数字各选了一个字母的结果，长度等于 `i`。每个分支结束返回上一层之前，`path` 必须恢复到进入时的样子，这样同一层的下一个字母才能在相同的前缀上继续。

**反例 1：漏掉 `path.pop()`。** `digits = "2"`：
- 选 `a`，`i == 1`，收集 `"a"`；不弹出，`path = ['a']`；
- 选 `b`，`path = ['a', 'b']`，收集 `"ab"`；选 `c`，收集 `"abc"`；
- 输出 `['a', 'ab', 'abc']`，正确答案是 `['a', 'b', 'c']`。

**反例 2：`ans.append(path)`，不 `join`。** 收集的是同一个列表对象的引用，而这个列表在回溯结束时被弹空。`digits = "23"` 的前三个结果都显示为 `[]`，而不是 `"ad"`、`"ae"`、`"af"`。如果必须收集列表形式，要写 `ans.append(path[:])` 或 `ans.append(list(path))` 复制一份。

**为什么叶子条件是 `i == len(digits)`。** 每个数字恰好选一个字母，所以路径长度达到数字个数时才是完整组合；中途收集会得到更短的前缀，不是合法答案。
