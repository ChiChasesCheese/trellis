---
id: robust-suppress-vs-bare-except-pass
node: engineering.robustness
type: qa
source: python-docs
---
## Q
`with contextlib.suppress(FileNotFoundError): os.remove('tmp')` 和写一个 `try: ... except FileNotFoundError: pass` 效果一样，为什么前者更值得提倡？这种「吞掉异常」的写法什么时候才合适？

## A
两者语义等价，`contextlib.suppress` 只是把「已知会发生、明确要忽略」的这一种异常类型写成声明式的一行，可读性更好且不易在改代码时不小心扩大 `try` 块范围。但无论哪种写法，都只应该用来覆盖「明确知道会发生、且已确认可以安全忽略」的具体异常类型（例如文件本就可能不存在），绝不能用一个宽泛类型（如 `Exception`）去静默吞掉所有错误，否则会掩盖真正的 bug。
