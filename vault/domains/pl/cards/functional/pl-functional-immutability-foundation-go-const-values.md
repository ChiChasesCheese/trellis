---
id: pl-functional-immutability-foundation-go-const-values
node: functional.immutability
type: qa
step: 4
---
## Q
Go 里有什么不可变的机制？`const` 能做什么，值语义怎样间接提供隔离？

## A
Go 的 `const` 只用于**编译期常量**：数字、字符串、布尔值（以及它们的无类型常量表达式），没有不可变的结构体、切片、map。

```go
const Limit = 10
p := &Limit
// error: cannot take address of Limit (untyped int constant 10)
```

常量不占内存地址，不是变量，是编译器内联的字面量。想要「不可变的配置对象」，Go 没有语言机制，靠约定：字段不导出，只提供读取方法，不提供修改方法。

Go 的真正机制是**值语义**：赋值和传参都是复制。

```go
type Cfg struct{ Tags [2]string }
func set(c Cfg) { c.Tags[0] = "changed" }
c := Cfg{[2]string{"a", "b"}}
set(c)
fmt.Println(c)   // {[a b]}：函数改的是副本
```

数组和结构体按值传递，接收方改的是副本，调用者的数据不受影响，等于在拷贝成本内获得了隔离。但这个保护是**浅的**：结构体里的切片、map、指针被复制的只是头部，它们指向的底层数据仍然共享。

所以 Go 的不可变性是「小而按值」的惯用法：小结构体按值传递（隔离便宜）；大的、需要共享的用指针，并靠文档和约定说明是否会被修改；并发共享则靠锁、通道，或者发布后不再修改的约定。Go 不提供类型层面的保证。
