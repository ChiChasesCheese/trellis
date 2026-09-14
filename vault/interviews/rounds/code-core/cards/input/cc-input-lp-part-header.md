---
id: cc-input-lp-part-header
node: input.line-protocols
type: qa
---
## Q
The input may begin with a `PART n` line that changes what the program prints — and may equally well be absent. How do you handle it?

## A
**Peek and pop, then pass `part` as a parameter to one shared code path.**

```python
lines = [l.strip() for l in sys.stdin if l.strip()]
part = DEFAULT_PART
if lines and lines[0].startswith("PART"):
    part = int(lines.pop(0).split()[1])
```

Two decisions worth stating: the default when the header is absent (usually the **highest** part, because the parts accumulate into one program), and that `part` gates only the output and the rules that differ — never a second copy of the pipeline. Graders do run the no-header case, so the default is a tested behaviour, not a convenience.

## Q zh
输入可能以一行 `PART n` 开头来改变程序的打印内容 —— 也可能根本没有这一行。怎么处理？

## A zh
**先窥探再弹出，然后把 `part` 作为参数传给同一条代码路径。**

```python
lines = [l.strip() for l in sys.stdin if l.strip()]
part = DEFAULT_PART
if lines and lines[0].startswith("PART"):
    part = int(lines.pop(0).split()[1])
```

有两个决定值得明说：没有这一行时的默认值（通常是**最高**的那一部分，因为各部分是累加进同一个程序的）；以及 `part` 只控制输出和真正不同的规则，绝不派生出第二份流水线。评测机确实会跑没有 header 的情形，所以默认值是被测试的行为，不是图方便。
