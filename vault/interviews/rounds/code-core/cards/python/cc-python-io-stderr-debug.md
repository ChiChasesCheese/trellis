---
id: cc-python-io-stderr-debug
node: python.io
type: qa
---
## Q
You cannot attach a debugger and stdout is compared byte for byte. How do you print debug output safely, and what must you know about ordering?

## A
**Everything you print for yourself goes to `sys.stderr`.**

```python
print(f"{event=} {state=}", file=sys.stderr)
```

- stdout is the contract: one stray line there fails *every* test at once, including the ones your logic gets right.
- stderr is normally shown in the run panel and ignored by the comparator.
- The two streams are buffered independently, so their interleaving in a terminal is **not** the true order — never infer sequence from it. Add a counter to the debug line if order matters.
- A debug line inside a hot loop is also real time; grep for `stderr` and `print(` before you submit and delete every one.

## Q zh
你没法挂调试器，而 stdout 是逐字节比对的。怎样安全地打印调试输出？关于顺序你必须知道什么？

## A zh
**所有给你自己看的打印都走 `sys.stderr`。**

```python
print(f"{event=} {state=}", file=sys.stderr)
```

- stdout 是契约：那里多出一行就会一次性挂掉*所有*测试，包括逻辑本来正确的那些。
- stderr 通常显示在运行面板里，比对器会忽略它。
- 两个流各自缓冲，所以它们在终端里的交错**不是**真实顺序 —— 绝不要据此推断先后。顺序重要时给调试行加一个计数器。
- 热点循环里的一行调试也是实打实的时间；提交前 grep 一遍 `stderr` 和 `print(`，把它们全删掉。
