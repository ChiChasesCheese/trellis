---
id: cc-python-portability-language-cost
node: python.portability
type: qa
---
## Q
Sixty minutes, a parsing-then-rules problem, language free. Give the honest verdict on Python, Go, Java and TypeScript.

## A
**Choose the language with the shortest path from "line of text" to "typed record".**

- **Python** — fastest to write: one-line parsing, tuples as composite keys, `defaultdict`/`Counter`, no build step, a `__repr__` for free. Cost: you must carry the runtime budget in your head, because it is roughly 30–50× slower per operation than Go or Java ([[cc-performance-budget-ops-per-second]]).
- **Go** — quick at runtime, but no tuple map keys, a five-method heap, and an error check on every `strconv.Atoi`. Expect 1.5–2× the lines.
- **Java** — the most typing per idea (`Map<String, List<Charge>>`, `computeIfAbsent`, boxing). Worth it only when the perf test is genuinely tight.
- **TypeScript** — good `Map`/`Set`, but no integer type, no tuple keys, no priority queue, and a lexicographic default sort.

Verdict: in a 60-minute round, minutes of *your* time are far scarcer than milliseconds of CPU. Take Python unless the constraint arithmetic says it will not fit.

## Q zh
60 分钟，一道「解析加规则」的题，语言不限。对 Python、Go、Java、TypeScript 给出老实的判断。

## A zh
**选那门从「一行文本」到「带类型的记录」路径最短的语言。**

- **Python** —— 写得最快：一行解析、元组当复合键、`defaultdict`/`Counter`、无构建步骤、白送 `__repr__`。代价：你必须把运行时预算记在脑子里，因为它每次操作比 Go 或 Java 慢约 30–50 倍（[[cc-performance-budget-ops-per-second]]）。
- **Go** —— 运行快，但没有元组 map 键、堆要实现五个方法、每个 `strconv.Atoi` 后面都跟一次错误检查。代码行数预计 1.5–2 倍。
- **Java** —— 每个想法要敲最多字（`Map<String, List<Charge>>`、`computeIfAbsent`、装箱）。只有性能测试真的紧时才值得。
- **TypeScript** —— `Map`/`Set` 不错，但没有整数类型、没有元组键、没有优先队列，默认排序还是字典序。

判断：在 60 分钟的一轮里，*你的*分钟数远比 CPU 的毫秒数稀缺。除非约束算术说塞不下，否则就用 Python。
