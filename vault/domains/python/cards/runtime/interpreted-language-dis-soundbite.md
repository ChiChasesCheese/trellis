---
id: interpreted-language-dis-soundbite
node: runtime.compile-bytecode
type: qa
source: cpython-internals
---
## Q
面试官追问「你说 Python 是解释型语言，具体解释一下，`dis` 模块能帮你验证什么」，60 秒内怎么答？

## A
三句话：①CPython 不是逐行解释源码，而是先编译成字节码这种中间表示（词法分析→语法树→控制流图优化→汇编），这一步类似编译器前端；②之后由 C 写的求值循环逐条解释执行字节码，这才是「解释型」的真正含义，也是比原生机器码慢的根源；③`dis` 模块能把函数反汇编成字节码指令，用来验证某种写法是否真的比另一种少几条指令，而不是凭感觉判断性能差异。
