---
id: craft-make-unmake-undo-log-5-across-problems-and-scales
node: craft.patterns.make-unmake-undo-log
type: qa
step: 5
---
## Q
**做/撤销与撤销日志 · N 皇后、键值库、编辑器、四子棋、国际象棋里的同一个动作**｜模式

这五个问题都有「改一下再撤回」。撤销信息分别存在哪里？放大到数据库，同一个想法叫什么？

## A
**要点。** 撤销信息的位置有三种：藏在**调用栈**里（递归回溯的局部变量）；放在**动作对象**里（`Move.prev_halfmove`、`Edit.removed`）；放进**日志**里（闭包列表）。选择由撤销的时机决定：只在递归返回时撤，用调用栈；需要用户随时撤任意步，用动作对象或日志；需要多层嵌套、随时回滚一整批，用分层日志。

```python
# N-Queens：撤销信息在调用栈上（递归返回时撤）
cols.add(c); d1.add(row - c); d2.add(row + c)
total += go(row + 1)
cols.remove(c); d1.remove(row - c); d2.remove(row + c)
# kv-store：撤销信息在日志里（闭包），逆序重放
for undo in reversed(self._frames.pop()): undo()
# chess：撤销信息在 Move 里（被吃的子、旧计数）
self._en_passant, self._rights, self._halfmove = (move.prev_en_passant, move.prev_rights, move.prev_halfmove)
```

**见于。** n-queens、kv-store、text-editor、connect-four（`drop` 的逆操作是 `undo`，搜索里用它）、chess。

**不变的。** 逆操作必须精确；撤销信息 = 正向会丢掉的东西；多步撤销按逆序；撤销后与派生结构（局面计数、孤立的过期表）一起恢复。**变化的。** 撤销信息的存放位置，以及撤销的粒度（一步、一层事务）。

**信号。** 需求里出现「悔棋」「回滚」「撤销」「试探一下再退回」「嵌套事务」；或者一个搜索里每个节点都在复制大对象。

**尺度对照。** 力扣：回溯题的做/撤销（N 皇后、全排列、子集）。低层设计：着法对象、分层撤销日志。数据库：事务回滚靠撤销日志（例如 InnoDB 的 undo log 保存修改前的旧值，同时也支撑一致性读）；写前日志（WAL）则是相反方向，记下"要做什么"以便崩溃后重做。变化：内存里撤销是一次函数调用，数据库里撤销信息本身要持久化，并且要和其他并发事务可见的数据版本协调，所以"撤销日志"在那里同时承担回滚和多版本读取两件事。
