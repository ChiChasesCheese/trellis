---
id: cc-output-sentinels-error-contract
node: output.sentinels
type: qa
---
## Q
A command arrives with the wrong number of arguments, then one names an unknown region, then one carries `1.5` where an integer is required. What does a well-behaved program print, and what does it change?

## A
**The error token is part of the output contract, and the state must be untouched.**

- Validate **fully before mutating**. A half-applied command — source debited, destination invalid — is exactly what graders probe, and it corrupts every later part.
- Never let an exception escape: a traceback replaces the rest of stdout and loses the points for parts that were already correct. Catch at the dispatch loop and emit the declared token.
- One validator per command shape returning either a parsed record or an error, rather than `try` blocks scattered around the mutations.
- Use the spec's token exactly, including case and any suffix: `ERROR`, `-1`, `N/A`, `NONE 0`, `false` are five different contracts, and an unknown command word usually maps to the same one as a bad argument.
- "Ignored" is a third behaviour: some specs want no output *and* no state change ([[cc-output-sentinels-none-vs-blank]]).

## Q zh
先来一条参数个数不对的命令，再来一条指向未知 region 的，再来一条在要求整数处给了 `1.5`。一个行为良好的程序打印什么、改变什么？

## A zh
**错误标记是输出契约的一部分，而状态必须保持不变。**

- **先完整校验再修改状态。** 只执行了一半的命令 —— 源已扣款、目标却非法 —— 正是 grader 要探的，而且会污染后面每一个 part。
- 绝不让异常逃逸：traceback 会替换掉 stdout 的剩余部分，把已经做对的 part 的分也弄丢。在分发循环处捕获，并输出约定的标记。
- 每种命令形态一个校验器，返回解析好的记录或一个错误，而不是把 `try` 散落在各处的状态修改旁边。
- 精确使用 spec 的标记，包括大小写和后缀：`ERROR`、`-1`、`N/A`、`NONE 0`、`false` 是五种不同契约，而未知命令词通常与非法参数映射到同一种。
- 「忽略」是第三种行为：有些 spec 要求既不输出*也*不改状态（[[cc-output-sentinels-none-vs-blank]]）。
