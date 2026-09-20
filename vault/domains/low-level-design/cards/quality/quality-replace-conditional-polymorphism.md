---
id: quality-replace-conditional-polymorphism
node: quality.refactoring
type: qa
---
## Q
"用多态替换条件" —— 触发条件是什么，什么时候 switch 反而是更好的设计？

## A
触发条件：**同一个**基于类型的 `switch`/`if` 出现在**多个地方** —— 每加一个类型都要在所有这些地方做散弹式修改。把每个分支的主体搬进子类/策略的覆盖方法里，用分派取代这些条件判断。

```java
switch (emp.type) { ENGINEER -> base*1.1; MANAGER -> base+bonus; }  // pay() 里有、inBonus() 里有、inReport() 里还有…
// 变成：emp.pay() —— 每个类型一个类，自己拥有自己的全部分支
```

该保留 switch 的情况：

- 它只出现**一次** —— 多态是拿一段可读的代码块，换来散落在多个文件里的类。
- 新增**操作**比新增**类型**更频繁 —— 多态为"加类型"优化，switch（或 visitor）为"加操作"优化。这就是 expression problem：选那个真正在变的轴。
