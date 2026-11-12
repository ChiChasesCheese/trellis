---
slug: number-of-atoms
---
## Q
**LC 726 原子的数量**｜Hard

解析化学式 `formula`（原子名、数量、括号及括号后的倍数），按原子名字典序输出每种原子及其数量，数量为 `1` 省略。

## A
**一句话。** 栈里放计数器：`(` 压入新计数器，`)` 弹出并乘倍数并入上一层，用正则一次切出 token。

```python
def count_of_atoms(formula):
    tok = re.compile(r"([A-Z][a-z]*)(\d*)|(\()|\)(\d*)")
    st = [Counter()]
    for name, num, lp, mul in tok.findall(formula):
        if name:
            st[-1][name] += int(num or 1)
        elif lp:
            st.append(Counter())
        else:                     # ')'：乘倍数后并回上一层
            top = st.pop()
            for a, c in top.items():
                st[-1][a] += c * int(mul or 1)
    return "".join(a + str(c if c > 1 else "")
                   for a, c in sorted(st[0].items()))
```

**复杂度。** 时间 `O(n·k)`，空间 `O(n)`，`k` 是原子种类数。

**易错点。**
- 原子名只取一个大写字母：`Mg` 丢掉 `g`，`"Mg(OH)2"` 得 `"H2MO2"`，应为 `"H2MgO2"`。
- 忽略 `)` 后的倍数：`"Mg(OH)2"` 得 `"HMgO"`。
- 排序按原子名字典序，不是按数量或出现顺序；数量为 `1` 不写。

**追问。**
- 数量非常大？：Python 整数不会溢出；Java / C++ 要用 `BigInteger` 或按题意取模。
- 支持 `[]`、`{}`？：token 正则加上这两类，栈的压入弹出对应各类括号。

**同模式。** LC 394 字符串解码、LC 224 基本计算器、LC 772 基本计算器 III、LC 20 有效的括号
