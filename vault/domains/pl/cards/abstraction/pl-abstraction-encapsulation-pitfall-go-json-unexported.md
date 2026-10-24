---
id: pl-abstraction-encapsulation-pitfall-go-json-unexported
node: abstraction.encapsulation
type: qa
step: 10
---
## Q
Go 里一个结构体字段首字母写成了小写，为什么序列化时数据会无声丢失？

## A
`encoding/json` 通过反射读取字段，而反射**遵守可见性**：它看不到小写（未导出）的字段，所以直接跳过，既不报错也不警告。

```go
type User struct {
    Name  string
    email string      // 小写
}
b, _ := json.Marshal(User{"ann", "a@x.com"})
fmt.Println(string(b))
// {"Name":"ann"}      —— email 不见了
```

典型事故：给结构体新增字段时顺手写了小写，单元测试里只比较了内存里的对象，没有走一遍序列化，直到线上发现另一个服务收到的数据缺字段。反序列化方向同理：`json.Unmarshal` 不会填未导出字段，它们保持零值，没有任何提示。

同一类问题出现在所有靠反射读字段的库：`encoding/xml`、`gob`、ORM、模板引擎（`text/template` 对小写字段会报错但消息不直观）。

防御：
- 序列化的 DTO 类型里所有字段都导出，用 struct tag 控制 JSON 的键名（`json:"email"`），不要依赖大小写；
- 写一个往返测试（序列化再反序列化，断言相等）覆盖每个对外结构；
- 用 `go vet`：它会报告「带 `json` tag 的未导出字段」，这个 tag 永远不会生效。
