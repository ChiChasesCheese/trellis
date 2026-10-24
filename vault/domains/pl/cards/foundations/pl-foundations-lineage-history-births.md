---
id: pl-foundations-lineage-history-births
node: foundations.lineage
type: qa
step: 9
---
## Q
Python、Java、Go、Rust 各自诞生时面对的环境和痛点是什么？时间线是怎样的？

## A
- Python（1991）：Guido van Rossum 在荷兰 CWI 参与过教学语言 ABC，想做一门既能写脚本又能当真正语言的工具，在 Unix 系统管理和 C 之间补一块。2008 年的 Python 3 做了一次不兼容的清理。
- Java（1995）：Sun 起初为家电和交互电视设计，赶上互联网兴起，口号是「一次编写，到处运行」，并用垃圾回收和去掉指针运算回应 C++ 项目里的内存错误。
- Go（2009 公开，2012 年 1.0）：Google 内部的 Robert Griesemer、Rob Pike、Ken Thompson 因为用 C++ 编译一个大型服务要等很久、多核并发难写而设计，目标是大代码库和大团队下的开发效率。
- Rust（2010 公开，2015 年 1.0）：Graydon Hoare 的个人项目，后来由 Mozilla 资助，为的是写出更安全、可并行的浏览器引擎。

时间上看，四门语言恰好沿着一条主线排开：1990 年代解决「写得快、跑得到处都是」，2010 年前后解决「多核时代的并发与大规模工程」和「不要再出内存安全漏洞」。每一代都是对上一代痛点的回应。后面在讲每个具体特性时，如果觉得设计奇怪，先回到诞生背景看它是为了对付哪个痛点。
