---
id: pl-rt-opt-mechanism-bce
node: runtime.optimizations
type: qa
step: 6
---
## Q
数组下标越界检查（bounds check）是怎么被编译器消除的？Go 的 `-d=ssa/check_bce` 能看出什么，写代码时怎样帮优化器一把？

## A
Go、Java、Rust、Python 访问数组/切片都要检查下标是否合法，越界就报错而不是读到脏内存。每次检查是一次比较加一个分支，很便宜，但在热循环里会阻碍向量化，并占用指令。优化器的办法是**证明某次检查必然通过**，然后删掉它，这叫边界检查消除（BCE）。

证明依赖循环结构。Go 里可以让编译器报告还剩哪些检查：
```go
func sumPlain(s []int, n int) int {     // n has no known relation to len(s)
	for i := 0; i < n; i++ { t += s[i] }  // Found IsInBounds
}
func sumRange(s []int) int {
	for i := range s { t += s[i] }        // no report: i < len(s) is proven
}
func four(s []int) int {
	_ = s[3]                              // Found IsInBounds (the single hint)
	return s[0] + s[1] + s[2] + s[3]      // all four are now proven
}
```
`go build -gcflags=-d=ssa/check_bce/debug=1` 的实测输出只有两行：`sumPlain` 里的 `s[i]` 和 `four` 里的 `_ = s[3]`。`range` 遍历天然被证明，不报告；`four` 里先写一次 `_ = s[3]`，后面三个下标都能由“长度至少为 4”推出，只剩这一次检查。

**各语言**：
- **Rust**：迭代器 `for x in &v` 根本没有下标，没有检查；写 `v[i]` 才有，LLVM 同样做证明。
- **Java**：HotSpot C2 对计数循环做 range-check elimination，把循环里的检查提到循环外一次完成。
- **Python**：每次下标访问都是解释器里的一次检查，没有消除。

做法：**能用 `range`/迭代器就不要手写下标**；必须手写时，在循环前写一句断言或 `_ = s[n-1]` 这样的提示。这是对性能敏感代码里最便宜的优化，但先测量热点再做，不要给冷代码加这种怪写法。
