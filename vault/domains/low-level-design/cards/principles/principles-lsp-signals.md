---
id: principles-lsp-signals
node: principles.solid
type: qa
---
## Q
什么时候你知道一个子类违反了 Liskov 替换原则？

## A
信号：
- 调用者必须检查运行时类型才能安全调用方法：`if (x instanceof Circle) ...`
- 子类抛出基类不抛出的异常
- 子类削弱前置条件或强化后置条件（相对于基类）
- 子类中的方法对调用者的期望没有满足（比如缓存的实现阻止重新计算，但调用者期望新值）
