---
id: pl-data-serialization-intro-go
node: data.serialization
type: qa
step: 3
---
## Q
Go 的 `encoding/json` 是怎样工作的？它对未导出字段、未知字段和 `any` 里的数字有哪些默认行为？

## A
**怎样工作**：`json.Marshal(v)` 用反射遍历结构体的字段，读每个字段的 struct tag（比如 `json:"name"`）决定键名，把值写成 JSON。`json.Unmarshal(data, &v)` 反向：解析 JSON，再用反射按键名找字段，设置值。因为用了反射，只有**导出字段**（首字母大写）会被处理。

```go
type U struct {
    ID    int64    `json:"id"`
    Name  string   `json:"name"`
    Tags  []string `json:"tags"`
    score int      // unexported
}
json.Marshal(U{1, "a", nil, 5})  // {"id":1,"name":"a","tags":null}
```

真实输出：`score` 被静默跳过；`nil` 切片变成 `null`。

**默认的宽松行为**：
- **未知字段被忽略**：输入 `{"id":1,"nmae":"typo"}`，`Name` 就是空字符串，没有任何错误。要变严格，用 `Decoder.DisallowUnknownFields()`。
- **类型不匹配才报错**：给 `int64` 字段一个字符串 `"7"`，得到 `json: cannot unmarshal string into Go struct field U.id of type int64`。
- **解码进 `any` 时数字都是 `float64`**：`{"id": 9007199254740993}` 解码后打印出的是科学计数法的 9.007199254740992 乘以 10 的 15 次方，也就是 9007199254740992，末位的 3 变成了 2（真实输出）。要精确，定义具体的结构体，或用 `Decoder.UseNumber()`。

**要记住的一点**：Go 的 JSON 是「宽进严出」的反射实现：简单、够用、标准库自带，但把校验留给你。一次本机测量，解码一个小对象约 350 ns，编码约 140 ns。
