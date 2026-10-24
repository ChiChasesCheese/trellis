---
id: pl-binding-evaluation-order-foundation-go
node: binding.evaluation-order
type: qa
step: 3
---
## Q
Go 规范对求值顺序规定了什么、没规定什么？为什么 `[]int{a, f()}` 的结果可能出乎意料？

## A
Go 规范规定：表达式里的**函数调用、方法调用、通道接收和逻辑运算**，按词法顺序从左到右执行。但它明确说**没有规定**这些操作与普通变量读取之间的先后。

```go
a := 1
f := func() int { a++; return a }
x := []int{a, f()}
fmt.Println(x)     // [2 2] with this toolchain; [1 2] would also be conforming
```

规范只保证 `f()` 会被调用，没保证变量 `a` 是在 `f()` 之前还是之后读取。官方编译器的实际行为是：先执行所有调用，再读取普通变量，因此得到 `[2 2]`。换一个实现或升级编译器，`[1 2]` 同样合法。

同样容易被忽视的几条：

- **`defer` 的参数在 `defer` 语句执行时求值**，不是在函数返回时：

```go
y := 1
defer fmt.Println("defer saw", y)   // y is evaluated now: 1
y = 2                                // output: defer saw 1
```

- **`map` 的遍历顺序故意随机化**：每次遍历起点不同，防止程序依赖它。需要稳定顺序要先排序键。
- **赋值的左右两边**：`m[len(m)] = len(m) + 5` 里下标与右边的 `len(m)` 都在赋值前算好，得到 `map[0:5]`。多重赋值 `a, b = b, a` 先算右边全部，再统一赋值，所以能交换。

Go 的立场是：给最容易出问题的东西（调用与通信）排好序，让并发代码可预测；对纯变量读取保留优化空间。因此实践规则非常简单：**一个表达式里不要让一个变量既被函数调用修改，又被别处读取。**
