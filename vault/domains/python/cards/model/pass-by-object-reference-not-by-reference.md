---
id: pass-by-object-reference-not-by-reference
node: model.mutability
type: qa
source: python-docs
---
## Q
Python 的参数传递常被问「是传值还是传引用」，准确的说法是什么？为什么在函数体内对形参重新赋值不会影响调用者的变量？

## A
Python 的参数传递本质是「按对象引用传递的赋值（pass by assignment）」：形参是函数内的新名字，被绑定到调用者传入的同一个对象上。若在函数体内对形参重新赋值（如 `a = 'new-value'`），只是让形参这个名字改指向别的对象，调用者的原名字仍绑定原对象，不受影响；只有对形参引用的可变对象做就地修改（如 `a[0] = ...`、`a.append(...)`），调用者才能通过共享对象看到变化，这也是 Python 没有真正的按引用传递（call by reference）的原因。
