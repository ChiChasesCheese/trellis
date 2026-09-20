---
id: patterns-memento-vs-command-undo
node: patterns.behavioral
type: qa
---
## Q
Memento vs Command 来实现 undo——都能做到，选择的张力是什么？

## A
- **Command**：存储**调用**（`cmd.execute()` 加 `cmd.undo()`）。优点：紧凑、单一职责。缺点：undo 逻辑分散在每个命令中；复杂操作中容易出错。
- **Memento**：存储**完整对象状态**的快照。优点：undo 是通用的（`restore(snapshot)`）；与命令无关。缺点：内存开销大；状态可能深而慢。

选择：
- 命令简单、undo 逻辑清晰？→ Command。
- 状态复杂、undo 必须是可靠的备份？→ Memento。
- 混合：Command 记录操作，Memento 作为检查点。
