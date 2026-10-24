---
id: pl-rt-compiler-found-ast-ir
node: runtime.compiler-pipeline
type: qa
step: 2
---
## Q
AST（抽象语法树）、IR（中间表示）和 SSA 形式分别是什么？请用 `a * 2 + b` 走一遍从源码到 IR 的变化。

## A
**AST**（Abstract Syntax Tree）：把源码的**结构**表示成树。词法分析先把字符切成记号（`a`、`*`、`2`、`+`、`b`），语法分析再按运算符优先级组织成树，丢掉无关的括号和空白。`a * 2 + b` 的树是“加法节点，左子树是乘法（`a`、`2`），右子树是 `b`”。Python 可以直接看到：
```python
ast.dump(ast.parse("def f(a, b):\n    return a * 2 + b\n").body[0].body[0])
```
输出（节选）：`Return(value=BinOp(left=BinOp(left=Name(id='a'), op=Mult(), right=Constant(value=2)), op=Add(), right=Name(id='b')))`。

类型检查、名字解析等语义分析都在树上做：给每个节点标上类型，检查 `a` 是否已定义、能不能和 `2` 相乘。

**IR**（Intermediate Representation，中间表示）：编译器内部使用的、介于源码和机器码之间的形式。它比 AST 更规整、更接近机器，但不依赖具体 CPU。优化都在 IR 上做。常见的 IR 是**三地址码**：每条指令最多一个运算符，用临时变量保存中间结果。

**SSA**（Static Single Assignment，静态单赋值）：IR 的一种形式，要求**每个变量只被赋值一次**。同一变量被多次赋值时，改写成新的名字（`x1`、`x2`），分支汇合处用 `phi` 函数选择。好处：每个值只有一个定义点，“这个值从哪来”一目了然，常量传播、死代码删除、公共子表达式消除都变得简单。

`a * 2 + b` 的 LLVM IR（Rust，`-O3`，节选）：
```
%_3 = shl i32 %a, 1
%_0 = add i32 %_3, %b
```
每个 `%` 名字只定义一次（SSA）；优化器已经把“乘 2”换成了“左移 1 位”。Go 编译器的后端同样基于 SSA。

流水线的意义就是：**在最适合的抽象层次上做最适合的事**——AST 上检查类型，SSA 上做优化，最后一层才考虑寄存器与指令。
