---
id: pl-out-go-append-alias
node: output.go
type: qa
step: 2
---
## Q
**append 共享底层数组**｜读代码说输出

```go
func main() {
	a := []int{1, 2, 3, 4}
	b := a[:2]
	b = append(b, 99)
	fmt.Println(a, b, len(b), cap(b))
	c := a[:2:2]
	c = append(c, 77)
	fmt.Println(a, c)
}
```

输出什么？

## A
**输出。**
```
[1 2 99 4] [1 2 99] 3 4
[1 2 99 4] [1 2 77]
```

**为什么。**
- `a[:2]` 与 `a` 共享底层数组，`b` 的长度是 2，容量是 4（从切片起点到数组末尾）。
- 容量够，`append` 把 99 直接写进下标 2，覆盖了 `a` 的第三个元素：`a` 变成 `[1 2 99 4]`，`b` 长度 3、容量 4。
- 三下标切片 `a[:2:2]` 把容量也限制成 2，`append` 必须分配新数组，77 写在新数组里，`a` 不受影响。

**语言为什么这样设计。**
- 切片是（指针、长度、容量）三元组；规范规定容量够就原地追加，不够才分配新数组，目的是均摊 O(1) 的追加，又不必每次都拷贝。
- 代价是「是否共享」取决于容量，从代码里看不出来。Python 的 `a[:2]` 总是拷贝；Java 的 `subList` 是视图，但对原列表做结构修改后再用会抛 `ConcurrentModificationException`。

**怎么写才对。**
```go
b := slices.Clone(a[:2])      // 需要独立副本
b = append(b, 99)             // 始终接收 append 的返回值
```

**面试里一句话。**
A Go slice append writes into the shared backing array whenever the capacity allows, so a subslice can overwrite its parent's elements.
