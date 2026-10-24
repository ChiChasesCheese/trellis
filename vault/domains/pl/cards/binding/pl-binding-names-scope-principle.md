---
id: pl-binding-names-scope-principle
node: binding.names-scope
type: qa
step: 1
---
## Q
代码里写下一个名字 `x`，语言怎样决定它指向哪个变量？词法作用域（lexical scope）和动态作用域（dynamic scope）的区别是什么，为什么现代语言几乎都选了前者？

## A
**作用域**（scope）是一个名字在程序里有效的范围，**名字解析**（name resolution）是在这个范围里找到名字所指变量的规则。两种基本答案：

- **词法作用域**：只看代码**写在哪里**，从当前块一层层向外找最近的声明。读源码就能确定 `x` 是谁。
- **动态作用域**：看**运行时谁调用了谁**，沿调用链向上找最近一个定义了 `x` 的调用者。

同一段代码在两种规则下结果不同。下面的 shell 脚本（bash 的 `local` 是动态作用域）里 `f` 写在外面，却看到了 `g` 的局部变量：

```bash
f() { echo "x is $x"; }
g() { local x=inner; f; }
x=outer; g          # prints: x is inner
```

词法规则下它会打印 `outer`。

现代语言选词法作用域，理由有三：读代码不必推演调用链；编译器能提前把名字解析成固定位置，不用运行时查表；闭包（closure，带着定义处环境的函数）只有在词法规则下才有明确含义。

动态作用域的唯一好处是**隐式传递上下文**（语言环境、日志器、事务）。现代语言把这个需求交给显式机制：Go 的 `context.Context` 参数、Java 的 `ThreadLocal`、Python 的 `contextvars`。

第二个设计维度是作用域的**粒度**：块级（C++、Java、Go、Rust：一对花括号一层）、函数级（Python：整个函数体一层，没有块作用域）、模块级。粒度决定了循环变量、临时变量会不会泄漏到外面，也决定了闭包能捕获什么。
