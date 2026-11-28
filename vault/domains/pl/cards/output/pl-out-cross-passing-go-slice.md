---
id: pl-out-cross-passing-go-slice
node: output.cross-passing
type: qa
step: 2
---
## Q
**Go 切片传参**｜读代码说输出

**Go**
```go
func f(s []int) {
	s[0] = 99
	s = append(s, 4)
	s[1] = 77
}
func main() {
	a := []int{1, 2, 3}
	f(a)
	fmt.Println(a)
	b := make([]int, 3, 4)
	copy(b, []int{1, 2, 3})
	f(b)
	fmt.Println(b, b[:4])
}
```
**Python**
```python
def f(s, grow):
    s[0] = 99
    if grow == "new":
        s = s + [4]
    else:
        s += [4]
    s[1] = 77
a = [1, 2, 3]
f(a, "new")
print(a)
b = [1, 2, 3]
f(b, "inplace")
print(b)
```

输出什么？

## A
**输出。**
**Go**
```
[99 2 3]
[99 77 3] [99 77 3 4]
```
**Python**
```
[99, 2, 3]
[99, 77, 3, 4]
```

**为什么。**
- Go 的切片是个小结构：指针、长度、容量，按值传递；`f` 拿到副本，但指针指向同一个底层数组，所以 `s[0] = 99` 调用者看得到。
- 第一次调用容量为 3，`append` 装不下，分配新数组并拷贝，之后 `s[1] = 77` 改的是新数组，`a` 只有 99 的改动。
- 第二次容量为 4，`append` 原地写进共享数组，随后 `s[1] = 77` 也写进共享数组：`b` 的长度仍是 3，只打印前三个，`b[:4]` 才看到追加的 4。
- Python 里 `s = s + [4]` 造新列表，对应「扩容」；`s += [4]` 原地扩展，对应「容量够」。

**语言为什么这样设计。**
- Go 想要数组的性能又要动态长度：切片是数组的视图，传参只拷贝 24 字节。代价是别名是否可见取决于容量，从代码里看不出来。
- Rust 用所有权避免：`&mut Vec` 独占借用，别处不能同时改；Java 的 `ArrayList` 是对象引用，扩容在内部发生，调用者始终通过同一个对象看到最新状态。

**怎么写才对。**
```go
func add(s []int) []int { return append(s, 4) }   // append 的结果必须返回
s = add(s)
slices.Clone(s)       // 需要隔离时先复制
```

**面试里一句话。**
A Go slice is passed by value but shares its backing array, so whether an append is visible to the caller depends on capacity.
