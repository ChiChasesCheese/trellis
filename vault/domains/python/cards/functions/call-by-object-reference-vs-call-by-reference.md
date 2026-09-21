---
id: call-by-object-reference-vs-call-by-reference
node: functions.arguments
type: qa
source: python-docs
---
## Q
Python 的参数传递常被称为「按对象引用传递」（pass by object reference / call by assignment），这和 C++ 里的「传引用」（call by reference）有什么本质区别？

## A
调用函数时，形参名字被绑定到实参所指向的同一个对象上，相当于做了一次赋值；调用者的变量名和被调函数里的形参名之间没有「别名」（alias）关系。所以在函数内把形参重新赋值成一个新对象，不会影响调用者手里的变量；但如果这个对象本身是可变的（mutable），在函数内原地修改它（如 `list.append`）会让调用者也看到变化。要实现「输出参数」的效果，只能传一个可变对象进去原地修改，或者直接 `return` 一个新值。
