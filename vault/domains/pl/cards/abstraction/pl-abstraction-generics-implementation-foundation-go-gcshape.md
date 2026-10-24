---
id: pl-abstraction-generics-implementation-foundation-go-gcshape
node: abstraction.generics-implementation
type: qa
step: 4
---
## Q
Go 的 GC shape stenciling 加字典是什么意思？为什么 Go 不选择完全单态化？

## A
Go 编译器把所有类型按「GC 看到的内存形状」分组：**底层类型相同**的算同一个 shape，**所有指针类型**也算同一个 shape（`*int`、`*string` 在 GC 眼里都只是「一个指针」）。每个 shape 生成一份实例化代码（stenciling）。

同一个 shape 里的不同类型，代码是共享的，但它们的类型相关操作（调用方法、转成接口、比较）怎么办？编译器给每个泛型函数额外传一个隐含参数——**字典**（dictionary），里面是该类型的类型描述符和方法地址，函数体通过字典查表完成操作。

在一个小程序里调用 `Show(1)`、`Show(int64(2))`、`Show(&n)`、`Show(&s)`、`Show(A{})`、`Show(B{})`，`go tool nm` 看到的实例化符号是：

```text
main.Show[go.shape.int]
main.Show[go.shape.int64]
main.Show[go.shape.*uint8]       // *int 和 *string 共用这一份
main.Show[go.shape.struct { main.p *int }]
main.Show[go.shape.struct { main.q *string }]
```

六次调用只有五份代码，两个指针类型共用一份。

为什么不全部单态化：Go 把**编译速度和二进制大小**当作一等目标。完全单态化会让标准库里的泛型代码膨胀；完全擦除又要为基本类型装箱。GC shape 是折中：值类型保持专用（不装箱），指针类型共享。代价是共享路径上通过字典的间接调用，可能比 Rust 的内联慢。
