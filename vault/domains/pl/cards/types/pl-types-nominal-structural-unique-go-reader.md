---
id: pl-types-nominal-structural-unique-go-reader
node: types.nominal-structural
type: qa
step: 8
---
## Q
Go 的隐式接口为什么说「接口由使用方定义」？标准库的 `io.Reader` 怎样让从未听说过它的类型也能参与？

## A
Go 标准库的 `io.Reader` 只有一个方法：`Read(p []byte) (n int, err error)`。任何类型只要有这个方法签名，就是 `Reader`，函数 `io.ReadAll`、`bufio.NewReader`、`io.Copy` 都接受它。

```go
type Upper struct{ s string }

func (u *Upper) Read(p []byte) (int, error) {
	if u.s == "" { return 0, io.EOF }
	n := copy(p, strings.ToUpper(u.s))
	u.s = u.s[n:]
	return n, nil
}

b, _ := io.ReadAll(&Upper{"hello"})
fmt.Println(string(b))   // HELLO
```

实际输出 `HELLO`。`Upper` 的作者没有 import `io` 来声明什么，却可以被 `io.ReadAll` 使用。

这就是「接口由使用方定义」：你写一个函数，只需要对象会 `Read`，就在自己的包里定义一个只有 `Read` 的小接口，调用方的类型自动满足，不需要谁去修改谁。Go 社区的惯例是接口越小越好（`io.Reader`、`io.Writer` 都只有一个方法），在使用方定义，而不是在实现方定义。

这在 Java 和 Rust 里做不到同样的低耦合：Java 的类必须在定义时就知道有哪些接口；Rust 虽然能事后 `impl`，但要在代码里显式写出来，并受孤儿规则限制。代价是 Go 的满足关系不显眼：看一个类型的定义，找不到它实现了什么。
