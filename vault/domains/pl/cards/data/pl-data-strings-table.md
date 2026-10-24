---
id: pl-data-strings-table
node: data.strings-text
type: qa
step: 8
---
## Q
比较 Go、Java、Rust、Python、C++ 的字符串模型：各选了哪个计数单位，买到什么，付出什么？

## A
| 语言 | 模型 | 买到 | 付出 |
|---|---|---|---|
| Go | 不可变字节序列，UTF-8 是约定 | 切片 O(1)、零拷贝、和 I/O 天然一致 | 可能含非法 UTF-8，按字符处理要自己解码 |
| Java | 不可变 UTF-16 单元序列，Latin-1 紧凑存储 | 历史兼容；英文字符串省内存 | `length()` 不是字符数，emoji 占两个单元 |
| Rust | 保证合法 UTF-8 的 `String`/`&str`，不可按下标取字符 | 正确性由类型保证，没有隐藏的 O(n) | 要显式选 `chars()`/`bytes()`，切到字符中间会 panic |
| Python | 不可变码点序列，宽度灵活 | `len`、下标直观，文本与字节严格分离 | 一个 emoji 让整串膨胀到 4 字节，仍不是字形簇 |
| C++ | 可变的字节序列 `std::string`（`char` 数组，编码靠约定，通常 UTF-8）；`std::string_view` 是非拥有的视图；`wchar_t` 宽度因平台而异 | 与 C 字符串和系统接口直接互通，切片零复制，小字符串不上堆（SSO，小字符串优化） | 标准库不懂 Unicode：`size()` 是字节数，没有规范化、字形簇；`string_view` 可悬空；`wchar_t` 在 Windows 是 2 字节、Linux/macOS 是 4 字节 |

**逻辑**：这五个选择是语言诞生时代与核心目标的化石。Java 1995 年出生，Unicode 当时以为 16 位够用，于是固定 16 位单元，后来 emoji 出现，只能用代理对修补。Go 的作者（也是 UTF-8 的发明者之一）直接让字符串就是 UTF-8 字节，把解码留给程序员。Rust 追求「无法构造出错误状态」，所以把合法性写进类型，并让含糊的下标变成编译错误。Python 3 追求对用户直观，付出内存灵活性来保证 O(1) 的码点下标。C++ 的字符串是 C 的遗产：`char` 数组加后来包装出来的 `std::string`，诞生在编码还不统一的年代，所以标准库至今不规定编码，`"a😀é"` 的 `size()` 实测是 7（UTF-8 字节数），和 Go 一样；与 Go 的区别是它可变，也没有 `range` 按字符遍历。这是 C 兼容与“标准库不替你决定”的结果，处理文本几乎都要借助 ICU 之类的库。

没有一个模型回答了「用户看到的字符」（字形簇）：这需要 Unicode 数据表，要靠库（Rust 的 `unicode-segmentation`、Java 的 `BreakIterator`、Python 的 `regex` 库 `\X`）。
