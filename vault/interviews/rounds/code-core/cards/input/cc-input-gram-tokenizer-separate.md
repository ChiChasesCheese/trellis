---
id: cc-input-gram-tokenizer-separate
node: input.grammar
type: qa
---
## Q
A later part replaces `field == value` rules with a real expression language: quoted constants that may contain spaces, boolean attributes, `AND`/`OR`, parentheses. What is the first structural decision?

## A
**Three separate stages: tokenize → parse to a tree → evaluate against a record.**

The tokenizer alone handles quoting and whitespace, so the parser never looks at characters; the parser alone handles precedence and nesting, so the evaluator never re-reads text; the evaluator alone knows what a missing field means.

Doing it in one pass with `split()` and string searching works for `a = "b"` and collapses at the first constant containing a space or the first nested parenthesis. Three stages is also what lets you parse each rule **once** and evaluate it against every record.

## Q zh
后面的部分把 `field == value` 规则换成真正的表达式语言：可能含空格的带引号常量、布尔属性、`AND`/`OR`、括号。第一个结构性决定是什么？

## A zh
**分成三个阶段：分词 → 解析成树 → 对记录求值。**

分词器独自处理引号和空白，于是解析器永远不看字符；解析器独自处理优先级和嵌套，于是求值器永远不重读文本；求值器独自知道字段缺失意味着什么。

用 `split()` 加字符串查找一趟做完，对 `a = "b"` 有效，但遇到第一个含空格的常量或第一层嵌套括号就崩。三阶段也正是让你把每条规则只解析**一次**、再对每条记录求值的前提。
