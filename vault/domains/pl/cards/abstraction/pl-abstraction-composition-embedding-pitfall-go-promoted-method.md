---
id: pl-abstraction-composition-embedding-pitfall-go-promoted-method
node: abstraction.composition-embedding
type: qa
step: 9
---
## Q
Go 里嵌入一个带有方法的类型，为什么可能悄悄改变外层类型的行为？以 `time.Time` 和 JSON 为例。

## A
嵌入会把内层的**所有**公开方法提升到外层，包括满足某个标准接口的方法。标准库的 `encoding/json` 会检查一个值有没有 `MarshalJSON` 方法；`time.Time` 恰好有。外层结构体嵌入它时，也就「继承」了这个方法，序列化时 `json` 调用的是它，而不是按字段展开外层。

```go
type Event struct {
    time.Time          // 嵌入
    Name string
}
b, _ := json.Marshal(Event{time.Date(2026, 10, 23, 0, 0, 0, 0, time.UTC), "deploy"})
fmt.Println(string(b))
// 输出："2026-10-23T00:00:00Z"   —— Name 字段不见了
```

`Name` 没有出现，编译器和 `json` 都没有报错。同样的原理还会影响 `String()`（`fmt` 打印）、`Error()`、`UnmarshalJSON` 等。

另一类相关的坑：嵌入 `sync.Mutex` 后，`c.Lock()` 成了 `Counter` 的公开 API，外部包可以直接给你的对象加锁，也可以不小心复制带锁的结构体。

修法：想要字段展开就不要嵌入 `time.Time`，改用具名字段 `At time.Time`；确实要嵌入时，为外层自己实现 `MarshalJSON`，明确序列化的内容。审查规则：每嵌入一个类型，都要检查它的方法集是否碰巧满足了 `fmt.Stringer`、`json.Marshaler`、`error` 这类被标准库自动识别的接口。
