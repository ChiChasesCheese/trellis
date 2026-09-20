---
id: problems-deck-of-cards-shoe-lock-and-immutable-cards
node: problems.games.deck-of-cards
type: qa
step: 9
tags: [grown]
---
## Q
一只赌场牌鞋（shoe）被多张桌子同时用时，哪里需要加锁？为什么 `Card` 本身完全不需要？GIL 在这里保证了什么？

## A
需要加锁的是 `Shoe.deal`：「检查够不够 → 切出来 → 从内部列表删掉」是典型的 check-then-act，中间被切走会让两张桌子拿到**重叠的牌**。锁的粒度是**一只牌鞋一把**，不是全局一把。

`Card` 不需要任何同步，因为它是 `frozen=True` 的不可变值对象——不可变的东西天生线程安全，可以随便跨线程共享；六副牌的牌鞋里放的其实可以是同一批 52 个对象的引用。游戏的取值表用 `MappingProxyType` 包成只读，也是同一个思路：不可变的东西不需要保护。

GIL 帮的忙很有限：它只保证单条字节码不被切开，而 `deal` 是好几步的复合操作。还有一条容易忽略的：订阅者回调是在 `deal` 的调用线程里**同步**执行的，所以回调里不许做慢事情——真要做，把事件丢进队列。
