---
id: distributed-collab-editing-replication
node: distributed.replication.multi-leader
type: qa
---
## Q
Why is real-time collaborative editing (Google-Docs-style) formally a multi-leader replication problem, and what dial does the size of the editing unit control?

## A
- Each user's device holds a **local replica it writes to immediately** (no round-trip per keystroke, works offline) and syncs asynchronously — that *is* multi-leader replication: multiple nodes accept writes independently, conflicts resolved after the fact.
- The **unit of change is the dial**. Lock the whole document while someone edits and you've collapsed back to single-leader: no conflicts, no real-time collaboration. Shrink the unit to a keystroke/character and concurrent edits become constant — so the merge logic (OT or CRDTs) must be automatic, deterministic, and run on every replica.
- Small units make conflicts **frequent but individually trivial** (two inserts at nearby positions), which is a better trade than rare-but-unmergeable conflicts on whole-document writes.

Takeaway: "how much do I lock / how small is a write" places any collaborative system on the spectrum between single-leader (serialize everything) and fine-grained multi-leader (merge everything).

## Q zh
为什么实时协作编辑（Google Docs 这类）在形式上就是一个多主复制（multi-leader replication）问题？编辑单元的大小控制着哪个"旋钮"？

## A zh
- 每个用户的设备都持有一个**可立即写入的本地副本**（每次按键无需网络往返，也能离线用），再异步同步——这*就是*多主复制：多个节点独立接受写入，冲突事后解决。
- **变更单元就是那个旋钮**。编辑时锁整篇文档，就退化回单 leader：没有冲突，也没有实时协作。把单元缩小到按键/字符级，并发编辑就无处不在——因此合并逻辑（OT 或 CRDT）必须是自动的、确定性的，并且在每个副本上都能独立得出相同结果。
- 小单元让冲突**频繁但个个都很小**（两个在相邻位置的插入），这比"整篇文档写入、冲突罕见但没法合并"是更好的交换。

要点："锁多大范围 / 一次写多小"决定了任何协作系统落在光谱的哪个位置——一端是单 leader（一切串行化），另一端是细粒度多主（一切靠合并）。
