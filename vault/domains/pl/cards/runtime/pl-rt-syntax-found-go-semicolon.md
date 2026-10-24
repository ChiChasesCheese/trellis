---
id: pl-rt-syntax-found-go-semicolon
node: runtime.syntax-parsing
type: qa
step: 3
---
## Q
Go 为什么不写分号却能解析，自动分号插入（automatic semicolon insertion）的规则是什么？它为什么逼着 `{` 必须和 `func` 写在同一行？

## A
Go 的文法在形式上要求语句以分号结束，但源码里几乎不写。做法在**词法分析**阶段：词法分析器在每一行末尾，如果最后一个记号是标识符、数字/字符串字面量、`return`/`break`/`continue`、`++`/`--`、`)`、`]`、`}` 之一，就自动补一个分号。解析器因此不需要“语句在哪里结束”的猜测，仍然是简单的单记号前瞻。

后果是两条硬规则：
```go
func main()
{                      // go build:
	fmt.Println("hi")  // syntax error: unexpected semicolon or newline before {
}
```
`func main()` 以 `)` 结尾，行末被补上分号，`{` 成了孤儿。另一条：多行的字面量里，最后一个元素后面必须有逗号：
```go
s := []int{
	1,
	2     // syntax error: unexpected newline in composite literal; possibly missing comma or }
}
```
`2` 是字面量，行末被补分号，所以必须写成 `2,`。多行表达式则要把运算符留在行尾（`total := 1 +` 换行 `2`），因为 `+` 不在补分号的名单里。

**这是设计取舍**：语言用“行尾补分号”换来了不用写分号的观感，也换来了一个副作用——**代码风格被语法固定**（大括号不能另起一行）。Go 团队顺势把格式也收归工具：`gofmt` 只有一种输出，团队不再争论风格。JavaScript 同样有自动分号插入，但规则是“出错再补”，而 Go 的规则是“词法上确定地补”，所以没有那些诡异的歧义。
