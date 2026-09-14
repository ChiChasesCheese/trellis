---
id: cc-python-io-read-all-stdin
node: python.io
type: qa
---
## Q
Read up to 10^6 lines from stdin as fast as possible, tolerating blank lines and a trailing newline. Write it — and say when the streaming form is the right call instead.

## A
```python
import sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
```

- One read, one pass. `input()` in a loop is several times slower and raises `EOFError` at the end.
- `splitlines()` drops the line terminators and does **not** produce a spurious empty last element for a trailing `\n`; `split("\n")` does.
- When memory is the binding constraint, stream instead: `for line in sys.stdin:` — each line still arrives with its `\n`, so `strip()` still matters ([[cc-performance-memory-input-is-resident]]).
- `sys.stdin.buffer.read()` returns bytes and is faster again if you can parse bytes directly.

## Q zh
尽可能快地从 stdin 读入至多 10^6 行，并容忍空行和结尾换行。写出来 —— 并说明什么时候该改用流式读法。

## A zh
```python
import sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
```

- 一次读取，一次遍历。循环里用 `input()` 要慢好几倍，并在末尾抛 `EOFError`。
- `splitlines()` 会去掉行终止符，且**不会**因为结尾的 `\n` 多出一个空元素；`split("\n")` 会。
- 当内存是硬约束时改用流式：`for line in sys.stdin:` —— 每行仍带着 `\n`，所以 `strip()` 依然重要（[[cc-performance-memory-input-is-resident]]）。
- `sys.stdin.buffer.read()` 返回 bytes，若能直接解析字节会更快。
