---
id: principles-temporal-coupling
node: principles.coupling
type: qa
---
## Q
```java
var svc = new ReportService();
svc.setStore(store);
svc.init();
svc.run();          // 少走一步就 NPE / IllegalStateException
```
说出这种耦合的名字、它的两个检测信号，以及修法。

## A
**Temporal coupling（时序耦合）** —— 正确性依赖于一个类型本身并未表达出来的调用顺序。信号：

- 方法开头是 `if (!initialized) throw new IllegalStateException(...)`。
- 为对象"没它就不能工作"的东西提供 setter（`setStore`），也就是说构造函数留下了一个非法的对象。

修法：**让非法状态压根构造不出来** —— 所有必需的协作者都从构造函数进来（或者用一个校验后返回就绪对象的 builder），把 `init()` 的内容并进去。当阶段确实互相不同时，就把阶段编码进*类型*里：`Connection.open()` 返回一个 `OpenConnection`，而只有它才有 `query()`。

同一个坏味道的放大版：跨类的两次调用必须按顺序发生 —— 把它们合并成一个方法，由它拥有这个顺序。
