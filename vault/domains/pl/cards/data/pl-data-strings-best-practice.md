---
id: pl-data-strings-best-practice
node: data.strings-text
type: qa
step: 10
---
## Q
资深工程师在处理文本时遵守哪些规则？Java、Go、Rust、Python 里分别怎样落实，何时可以破例？

## A
**通用规则**：
1. **边界处明确编码，内部统一为一种**。读入时解码、写出时编码，中间不做隐式转换；几乎总是选 UTF-8。
2. **先问「我要的是字节、码点还是用户看到的字符」**，再选 API。长度限制通常要按字节（数据库列、协议），显示截断要按字形簇。
3. **比较前规范化**：用户名、文件名、搜索关键字在比较或去重前统一成 NFC。
4. **累积用构建器，不用循环 `+=`。**

按语言：
- **Java**：不要用 `charAt`/`substring` 处理用户文本；需要码点用 `codePoints()`；显示截断用 `java.text.BreakIterator`。读写文件始终显式指定 `StandardCharsets.UTF_8`，不依赖平台默认（JDK 18 起默认才变成 UTF-8）。
- **Go**：边界处用 `utf8.ValidString` 检查来自外部的数据；遍历字符用 `range`；不要写 `s[:n]` 截断用户文本，先按 `rune` 或字形簇找位置。
- **Rust**：入口处 `String::from_utf8` 处理错误；`from_utf8_lossy` 仅用于日志；路径和系统字符串用 `Path`/`OsStr`，不要强转成 `String`。
- **Python**：显式 `open(..., encoding="utf-8")`；用 `unicodedata.normalize("NFC", s)`；`str` 和 `bytes` 不混用。

**何时破例**：纯 ASCII 的协议（HTTP 方法名、十六进制）直接用字节，更快；明确只处理英文标识符的内部工具可以不管字形簇。
