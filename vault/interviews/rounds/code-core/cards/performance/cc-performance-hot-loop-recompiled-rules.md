---
id: cc-performance-hot-loop-recompiled-rules
node: performance.hot-loop
type: qa
---
## Q
A program evaluates 50 000 transactions against 21 rule strings and takes 4 seconds. One change brings it to 0.3 seconds. The rules are tokenized and parsed inside the per-transaction loop. Name the fix and the general shape.

## A
**Hoist the compilation out of the loop: parse once, evaluate many.** Tokenizing and building the rule's AST per transaction repeats identical work 50 000 times; caching the compiled form keyed by the rule source collapses it to 21 parses — a measured ~15× on a real problem.

Same shape, same fix:
- `re.compile(...)` at module level, not inside the loop.
- `datetime.strptime` format strings, `Decimal` contexts, constant `str.split` targets.
- Any expression whose value depends only on loop-invariant data.

Cue while reading your own code: "does this line's answer change with the loop variable?" If not, it belongs above the loop.

## Q zh
一个程序拿 50 000 笔交易去过 21 条规则字符串，跑了 4 秒。改一处后变成 0.3 秒。规则的分词和解析写在每笔交易的循环里。说出修法和它的一般形态。

## A zh
**把编译提到循环外：解析一次，求值多次。** 每笔交易都重新分词、重建规则的 AST，是把同样的工作重复了 50 000 遍；用规则源串作 key 缓存编译结果，就塌缩成 21 次解析 —— 在一道真实题上实测约 15×。

同一形态，同一修法：
- `re.compile(...)` 放模块级，不放循环里。
- `datetime.strptime` 的格式串、`Decimal` 的 context、常量的 `str.split` 目标。
- 任何取值只依赖循环不变量的表达式。

读自己代码时的提示语：「这一行的结果会随循环变量变吗？」不会，它就该待在循环上面。
