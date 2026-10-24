---
nodes: [data.strings-text, data.arrays-slices, data.maps-collections]
tags: [drill]
---
# 练习：昵称限制「最多 6 个字符」，四个服务四种判断

用户昵称规则是「最多 6 个字符」。四个服务分别用 Go 的 `len(s)`、Java 的 `s.length()`、Python 的 `len(s)`、Rust 的 `s.len()` 来校验。昵称 `héllo👋` 在界面上看是 6 个字符，却有的服务放行、有的拒绝。另外，这四个服务还各自把用户标签放进映射里再遍历输出，导出的文件顺序在不同服务、甚至不同次运行之间都不一样。你要预测，并给出一套在四门语言里都正确的校验与导出做法。

**要你给出的**
- `héllo👋` 在四门语言里 `len` 一类调用的结果，以及它们各自数的是什么单位；按「用户看到的字符」应当怎么数。
- Go 里 `s[:2]` 与 `s[1:3]`、Rust 里 `&s[0..2]` 与 `s.get(0..2)` 的结果；Python 里 `"é"` 与 `"e\u0301"` 相等吗。
- 映射遍历顺序：Go、Python、Java、Rust 分别怎样；以及下面这段 Go 代码的输出。
- 校验与导出的跨语言规则各一条。

```go
a := make([]int, 3, 4)
b := append(a, 1)
c := append(a, 2)
fmt.Println(b[3], c[3])
```

**评分要点**
- `héllo👋` 的长度：Go 与 Rust 是 `10`（UTF-8 字节数），Java 是 `7`（UTF-16 码元，表情符号占两个），Python 是 `6`（码点）；Java 的 `codePointCount` 是 `6`，Go 用 `utf8.RuneCountInString`，Rust 用 `chars().count()`。用户看到的「字符」其实是字素簇（grapheme cluster），再往上要用专门的库 ([[pl-data-strings-pitfall-length]], [[pl-data-strings-intro-unicode]])。
- 四门语言的字符串模型：Go 是任意字节序列、约定为 UTF-8；Java 是 UTF-16 码元数组；Python 是码点序列；Rust 保证是合法 UTF-8。对「字符串里到底有什么」做的承诺不同，决定了切片、反转、截断是否安全 ([[pl-data-strings-intro-go]], [[pl-data-strings-intro-java]], [[pl-data-strings-intro-python]], [[pl-data-strings-intro-rust]])。
- 切片：Go 的 `s[:2]` 在 `%q` 下是 `"h\xc3"`，把 `é` 切成了半个字符，不报错；`s[1:3]` 是完整的 `"é"`。Rust 的 `&s[0..2]` 直接 panic（`end byte index 2 is not a char boundary`），而 `s.get(0..2)` 返回 `None`，`s.get(0..3)` 返回 `Some("hé")`。Python 的 `"é" == "e\u0301"` 是 `False`（长度 1 对 2），要先做规范化（`unicodedata.normalize("NFC", ...)`）才相等。Go 用 `range` 遍历字符串给出的是字节下标 `0:é 2:👋` ([[pl-data-strings-philosophy-trust-vs-guarantee]], [[pl-data-strings-best-practice]])。
- 映射顺序：Go 故意随机化迭代顺序（同一程序两次运行可得到 `1 2 3 4 5` 与 `5 1 2 3 4`）；Rust 的 `HashMap` 同样每次运行不同；Python 的 `dict` 保持插入顺序（`[3, 1, 2]`）；Java 的 `HashMap` 顺序由哈希桶决定，键 3、1、2、100、17 得到 `[1, 17, 2, 3, 100]`，看上去稳定但没有保证。依赖顺序的导出必须显式排序 ([[pl-data-maps-philosophy-order-promise]], [[pl-data-maps-table]])。
- Go 代码输出 `2 2`：`a` 长度 3、容量 4，两次 `append` 都写入同一个底层数组的第 4 个位置，后写的覆盖先写的，`b` 与 `c` 共享存储。需要独立副本时先 `slices.Clone` 或使用完整切片表达式限制容量 ([[pl-data-arrays-pitfall-go-alias]], [[pl-data-arrays-intro-go]])。
- 校验规则：先确定产品要的单位（字素簇、码点还是字节），在入口处做一次规范化，用能数出这个单位的函数，不要拿 `len` 默认值当业务规则；数据库列长度与协议字段长度另用字节数校验 ([[pl-data-strings-best-practice]])。
- 导出规则：需要稳定输出时对键排序，或使用有序结构；不要让下游依赖映射的遍历顺序；在测试里用多次运行或随机种子暴露这类依赖 ([[pl-data-maps-best-practice]], [[pl-data-maps-mechanism]])。

**练习记录**
- [ ] 第 1 次（日期、用时、自评）：
