---
id: cc-round-submit-no-half-refactor
node: round.submission
type: qa
---
## Q
At minute 56 you are halfway through renaming a structure to make the code read better. What do you do?

## A
**Revert to the last state you verified and submit that.** A half-applied rename is a syntax error or, worse, a silent partial change that still runs and now computes something else.

Two habits that make this recoverable: keep a copy of the last passing version (a comment block, a second file, a git commit if you have one) before starting any edit that touches more than one function, and never begin such an edit inside the last ten minutes. Legibility is worth zero tests; a running program is worth all of them.

## Q zh
第 56 分钟，你正把一个结构改名改到一半，为了代码更好读。怎么办？

## A zh
**回退到你上一次验证过的状态并提交那一版。** 改到一半的重命名要么是语法错误，要么更糟 —— 一次静默的部分改动，程序照跑，算的却是别的东西。

两个让这件事可恢复的习惯：在开始任何跨函数的编辑之前，先留一份上一个通过版本的副本（注释块、第二个文件，或有条件的话一次 git commit）；以及在最后十分钟绝不开始这类编辑。可读性值零个测试；能跑的程序值全部测试。
