# od07 Throne Inheritance without an initial king — report

## Summary
fastprep 电面题（"Source Match: 86%"，LC 1600 "Throne Inheritance" 改编），MED 难度。与原题唯一
的结构性区别："没有初始国王"——家谱从空开始，第一次 `birth()` 里的 parent 成为奠基者。3-part：
Part 1 建树 + 死亡标记 + 先序继承顺序 → Part 2 把遍历改成显式栈迭代（禁止递归，扛 10 万级深链）
→ Part 3 `succession_after` 死后继位查询 **(reconstructed)**。

## Sources & confidence
MED：fastprep 一手骨架与题面措辞（"Source Match: 86% (adapted from original problem)"）。校验
分类（自己当父母、重名）、死亡的幂等/无操作语义、死人可再生子女、`succession_after` 的具体行为
均为重建，problem.md 逐条标注 **(reconstructed)**。

## Approach by part
1. `ThroneInheritance` 内部只有三样状态：`_founder`、`_children`（name → 子女列表，出生序）、
   `_dead`（集合）。`birth` 先挡自己当父母，再挡重名，再决定"建立奠基者"还是"校验 parent 已知"。
   `get_inheritance_order` = `_full_order()` 过滤掉 `_dead`。
2. `_full_order()` 是本题唯一的遍历实现：显式栈迭代先序 DFS（`stack.pop()` + 逆序 push 子女保证
   出生序），Part 1/2/3 共用同一份代码，天然满足"无递归、O(n)"的要求，不需要为 Part 2 单独写一
   份迭代版本。
3. `succession_after` 复用 `_full_order()`（不过滤死人），定位 `name` 后向后线性扫描找第一个
   活人；这样即使 `name` 已死也能正确回答"他死后谁继位"。

## Pitfalls hidden tests target
- 空家谱：`get_inheritance_order() == []`，`succession_after` 恒为 `""`
- 自己当自己父母 → 不建立奠基者、家谱仍为空
- 重名（曾当过 parent 或 child 都算）→ `ValueError`
- 未知 parent（奠基者已存在后）→ `ValueError`
- 出生序 ≠ 字母序（用刻意反字母序的名字验证）
- `death` 三种输入（活人/死人/未知名字）都不报错、不改变结构
- 死人分支保留、死人还能生新孩子
- 死掉的奠基者依然是遍历起点
- `succession_after` 用在死人身上、用在最后一位、用在从未出生的名字上
- 10 万级深单链：临时调低 `sys.setrecursionlimit()` 后仍不报 `RecursionError`（证明确实迭代）
  + 端到端脚本 3 秒预算
- 随机交叉验证：30 组随机 birth/death/order 脚本，逐步比对朴素递归 oracle 的输出

## Complexity & measured cost
`birth` / `death` O(1)；`get_inheritance_order()` / `succession_after()` O(n)（n = 家谱总人数，
活人 + 死人），迭代实现、无递归。10 万级深链的 `get_inheritance_order()` 实测 <0.01s；端到端脚本
（10 万次 BIRTH + 1 次 ORDER）3 秒预算内完成。

## Test inventory
24 tests — part1 14（含 1 命令流错误聚合、1 io）· part2 3（2 perf：递归深度陷阱 + 端到端计时，
1 随机交叉验证）· part3 7（含 1 io）；edge 17 · perf 2 · io 2。

## Skills exercised
S09 契约先行（"没有初始国王"这个边界必须先想清楚）· 树遍历迭代化应对深链输入 · 幂等操作的防御
性设计 · 用一份底层遍历同时服务"全量顺序"与"某人之后是谁"两种查询形状。
