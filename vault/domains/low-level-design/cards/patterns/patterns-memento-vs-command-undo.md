---
id: patterns-memento-vs-command-undo
node: patterns.behavioral
type: qa
---
## Q
You're asked to add undo. Memento and command both do it — how do the two approaches differ, and when do you pick each?

## A
- **Memento**: snapshot the originator's **state** before each change; undo = restore the snapshot. The memento is opaque to everyone but the originator, so encapsulation survives. Simple and bulletproof, but memory-heavy for large state (mitigate with diffs or copy-on-write).
- **Command with `undo()`**: store the **inverse operation** (`InsertText` undoes by deleting the range). Cheap per step and gives redo/replay for free, but every command must implement a correct inverse — and some operations aren't invertible (irreversible side effects, lossy edits).

Practical answer: commands for the history mechanism, carrying small mementos of just the affected fragment — the hybrid most editors use.

## Q zh
Memento vs Command 来实现 undo——都能做到，选择的张力是什么？

## A zh
- **Command**：存储**调用**（`cmd.execute()` 加 `cmd.undo()`）。优点：紧凑、单一职责。缺点：undo 逻辑分散在每个命令中；复杂操作中容易出错。
- **Memento**：存储**完整对象状态**的快照。优点：undo 是通用的（`restore(snapshot)`）；与命令无关。缺点：内存开销大；状态可能深而慢。

选择：
- 命令简单、undo 逻辑清晰？→ Command。
- 状态复杂、undo 必须是可靠的备份？→ Memento。
- 混合：Command 记录操作，Memento 作为检查点。
