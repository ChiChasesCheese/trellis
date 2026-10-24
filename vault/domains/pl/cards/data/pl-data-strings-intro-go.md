---
id: pl-data-strings-intro-go
node: data.strings-text
type: qa
step: 4
---
## Q
Go 的 `string` 在内存里是什么？字节、`rune` 和 `range` 遍历分别给出什么，一个例子里发生了什么？

## A
**是什么**：Go 的 `string` 是一个不可变的字节序列，在内存里就是一个（指向字节的指针，长度）二元组。语言**约定**源码和多数字符串是 UTF-8，但类型本身不强制合法性：任意字节都能放进 `string`。

**三个视角**：
- `len(s)` 与 `s[i]`：按**字节**。
- `rune`：`int32` 的别名，代表一个码点。`[]rune(s)` 把字符串解码成码点数组。
- `for i, r := range s`：按**码点**遍历，`i` 是该码点起始的字节偏移，`r` 是码点。

```go
s := "a😀é"
len(s)               // 7 bytes
utf8.RuneCountInString(s)   // 3
for i, r := range s { ... } // 0:a 1:😀 5:é
s[1]                 // 0xf0, the first byte of the emoji
```

真实输出：7 字节、3 个码点；遍历给出偏移 0、1、5，说明 emoji 占了偏移 1 到 4。`s[1]` 是 `f0`，一个单独看没有意义的字节。

**非法字节**：`"\xff\xfe"` 是合法的 Go 字符串，`utf8.ValidString` 返回 `false`，`[]rune` 转换时把每个坏字节变成替换字符 `U+FFFD`（十进制 65533）。

**要记住的一点**：Go 把字符串当作「带 UTF-8 约定的字节包」，切片、拼接、写文件都零成本，没有任何隐式转换。需要按字符处理时自己选择 `range` 或 `[]rune`。切片 `s[a:b]` 是 O(1)，共享底层字节，不复制。
