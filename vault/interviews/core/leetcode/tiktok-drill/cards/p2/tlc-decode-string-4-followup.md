---
id: tlc-decode-string-4-followup
node: p2.decode-string
type: qa
step: 4
---
## Q
**LC 394 字符串解码**｜追问

面试官接着问：（1）用递归写一遍？（2）只要解码后的**长度**，而且输出可能大到存不下？（3）输入很长、嵌套很深时，两种写法的风险各是什么？

## A
1. **递归下降**：用全局下标 `i` 逐字符前进；遇到 `[` 递归解析内层并乘以刚读到的次数；遇到 `]` 返回上一层。
```python
def decode_recursive(s: str) -> str:
    i = 0
    def parse() -> str:
        nonlocal i
        out: list[str] = []
        num = 0
        while i < len(s):
            ch = s[i]
            i += 1
            if ch.isdigit():
                num = num * 10 + int(ch)
            elif ch == "[":
                out.append(parse() * num)
                num = 0
            elif ch == "]":
                break
            else:
                out.append(ch)
        return "".join(out)
    return parse()
```
   `"3[a2[c]]"` → `"accaccacc"`。
2. **只要长度**：栈里存的不再是字符串而是整数长度，`cur * times` 变成整数乘法，不分配内存。`"3[a2[c]]"` 得 `9`，`"300[300[300[a]]]"` 得 `27000000`。
```python
def decode_length(s: str) -> int:
    stack: list[tuple[int, int]] = []
    cur = num = 0
    for ch in s:
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, num))
            cur = num = 0
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times
        else:
            cur += 1
    return cur
```
3. **风险**：递归版的深度等于嵌套层数，Python 默认递归上限约 `1000`，嵌套 2000 层就会 `RecursionError`；栈版没有这个问题。两者的时间都由输出长度主导，嵌套的乘法会让输出指数膨胀，所以长度检查要放在构造之前。

**Python 提醒**：`str * int` 对负数或 `0` 返回空串，不会报错，所以 `times` 异常时静默得到空串；这里 `k` 保证为正整数。`nonlocal` 只用于修改外层的不可变变量（如下标 `i`），列表这类可变对象直接调用方法即可。
