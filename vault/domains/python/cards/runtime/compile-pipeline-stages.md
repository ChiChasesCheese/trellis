---
id: compile-pipeline-stages
node: runtime.compile-bytecode
type: qa
source: cpython-internals
---
## Q
CPython 把一段 Python 源码变成可执行字节码要经过哪几个阶段？

## A
依次是：①词法分析（tokenize）产出 token 流；②用 PEG 解析器把 token 流转成抽象语法树（AST，abstract syntax tree）；③遍历 AST 构建符号表（symbol table），确定每个名字的作用域；④把 AST 转成一串「伪指令」（pseudo instruction）；⑤据此构建控制流图（CFG，control flow graph）并做窥孔优化（peephole optimization）；⑥把优化后的 CFG 汇编（assemble）成真正的字节码，连同常量表、名字表等元数据打包进一个 `PyCodeObject`。
