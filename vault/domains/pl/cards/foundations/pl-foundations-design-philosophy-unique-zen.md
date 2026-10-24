---
id: pl-foundations-design-philosophy-unique-zen
node: foundations.design-philosophy
type: qa
step: 4
---
## Q
Python 在语言里怎样直接写下了它的设计哲学？哪几条原则最能解释 Python 的日常写法？

## A
Python 是唯一把设计哲学做成语言内置功能的：在解释器里执行 `import this`，会打印出 19 条格言，称为 Python 之禅（The Zen of Python）。节选：

```console
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Readability counts.
There should be one-- and preferably only one --obvious way to do it.
```

这些原则能解释具体写法：

- 「可读性很重要」解释了为什么 Python 用缩进而不是花括号表示块结构，布局和逻辑必须一致。
- 「明确胜于隐含」解释了为什么 `self` 必须显式写在方法参数里，为什么字符串和数字不会被隐式转换。
- 「最好只有一种明显的做法」是对 Perl「做法不止一种」的反动。

但最后一条在现实里也最常被打破：遍历有 `for`、推导式、`map`、生成器，格式化有 `%`、`str.format`、f-string。这说明哲学是倾向而不是法律，Go 把「只有一种做法」做成了编译器强制的规则（`gofmt`、无 `while`），Python 只把它留作口号。
