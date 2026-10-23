---
id: hl-j07-string-methods
node: java21.j07-text-blocks
type: qa
step: 10
---
## Q
和文本块配合最常用的四个 `String` 方法是什么？各是哪个版本加入、做什么？

## A
- `.formatted(args...)`（Java 15）：`"""...%s...""".formatted(x)`，等价 `String.format(textBlock, x)`。
- `.lines()`（Java 11）：按行拆成 `Stream<String>`，与换行符种类无关；测试常用 `block.lines().toList()`。
- `.stripIndent()`（Java 15）：对任意字符串做与文本块相同的"去公共缩进 + 去行尾空白"。
- `.translateEscapes()`（Java 15）：把字符串**内容里**的反斜杠转义翻译成真实字符（用于从配置文件读出的文本）。
