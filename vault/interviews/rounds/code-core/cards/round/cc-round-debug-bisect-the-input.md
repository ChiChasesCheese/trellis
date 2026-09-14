---
id: cc-round-debug-bisect-the-input
node: round.debugging
type: qa
---
## Q
Your program produces the right answer on the ten-line sample and the wrong one on a thousand-line input you generated. No debugger. How do you find the offending record?

## A
**Bisect the input, not the code.** Run the first half; if it is wrong, the culprit is there — otherwise it is in the second half, or in an interaction the halves hide. Ten halvings isolate one line out of a thousand.

Cheaper first move when state is cumulative: print the running state to stderr after every record and scan for the first line where an invariant breaks (a count going negative, a balance drifting, a set growing when it should not). Bisection finds *which* record; the invariant trace finds *when* it went wrong, which is usually more useful.

## Q zh
你的程序在十行样例上答案正确，在你自己生成的一千行输入上错了。没有 debugger。怎么找出那条记录？

## A zh
**二分输入，而不是二分代码。** 跑前一半；错了说明问题在那里，否则在后一半，或者在被两半掩盖的交互里。十次对折就能从一千行里定位到一行。

当状态是累积的时，更省事的第一步：每处理一条记录就把运行中的状态打到 stderr，扫出第一处不变量被破坏的行（计数变负、余额漂移、集合本不该增长却增长了）。二分找出**哪一条**记录；不变量轨迹找出**何时**出错 —— 后者通常更有用。
