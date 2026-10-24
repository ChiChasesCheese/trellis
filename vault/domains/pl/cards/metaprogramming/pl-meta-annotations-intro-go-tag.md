---
id: pl-meta-annotations-intro-go-tag
node: metaprogramming.annotations-decorators
type: qa
step: 4
---
## Q
Go 的 struct tag 是什么？它存放在哪里，谁来读它，一个小场景里它怎样改变序列化结果？

## A
**是什么**：struct tag 是结构体字段声明后面的一个原始字符串字面量（用反引号包起来），Go 编译器不关心里面写什么，只把它原样保存在类型描述里。社区约定它的内部格式是 `key:"value" key2:"value2"`。

**心智模型**：每个字段挂一张纸条，纸条上可以有多个「收件人」。`json:"..."` 是写给 `encoding/json` 看的，`db:"..."` 是写给数据库库看的，互不干扰。读取方通过反射（`reflect.StructTag.Get("json")`）拿到自己那一段。

**场景**：

```go
type U struct {
    ID    int    `json:"id"`
    Email string `json:"email,omitempty"`
    Pass  string `json:"-"`
}
json.Marshal(U{1, "", "secret"})
```

真实输出：`{"id":1}`。三条规则都生效了：`ID` 被改名为小写的 `id`；`Email` 为空值，`omitempty` 让它被省略；`Pass` 的 `-` 让它永远不输出，避免密码泄漏到响应里。

**要记住的一点**：tag 的格式和含义纯属约定，编译器不验证，写错了只会静默失效。它的价值在于零新语法：Go 把「给字段附带元数据」的需求用字符串加反射解决，而没有引入注解语言。`encoding/json`、`encoding/xml`、各种 ORM 与校验库都靠这一个约定。
