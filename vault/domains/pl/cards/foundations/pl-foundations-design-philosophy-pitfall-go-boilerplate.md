---
id: pl-foundations-design-philosophy-pitfall-go-boilerplate
node: foundations.design-philosophy
type: qa
step: 9
---
## Q
Go 追求「简单、显式」的代价在代码里是什么样子？这个代价说明了什么一般规律？

## A
Go 没有异常，错误是普通的返回值，每一步都要显式检查。一个读文件并解析整数的函数：

```go
func readNum(path string) (int, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return 0, err
	}
	n, err := strconv.Atoi(string(data))
	if err != nil {
		return 0, err
	}
	return n, nil
}
```

真正干活的只有两行，其余 6 行是错误检查和返回。这段代码实际编译通过。

好处是控制流完全可见：每个可能失败的位置都写在纸面上，读代码的人不会漏掉一条隐藏的异常路径。代价是样板代码多，业务逻辑被淹没。

一般规律：简单性不会凭空产生，它把复杂度从语言挪到了用户代码。Go 把「错误怎么传播」的复杂度挪给了每一个调用点；Java 的受检异常（checked exception）反过来，语言承担了更多机制，调用点代码少，但异常声明会沿着调用链向上扩散。评价一个设计，要同时看复杂度被放在了哪里，而不能只看语言本身看起来多简单。
