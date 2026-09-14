# od07 · Throne Inheritance without an initial king — 空族谱起步的 LC 1600 变体

> fastprep 电面题（"Source Match: 86% (adapted from original problem)"，即 LC 1600 "Throne
> Inheritance" 的改编），MED 难度。原题给的是完整规则骨架，本题的具体边界（自己当自己父母、
> 复活语义、死人能否再生子女、Part 3 的"死后继位查询"）大部分为 **(reconstructed)**，逐条标注。

## 背景

fastprep 原题描述（一手改写）：

> "Design a class that models throne inheritance, but unlike the classic version there is no
> king at construction time — the family starts completely empty. Support recording births,
> recording deaths, and querying the current inheritance order."

和 LC 1600 的关键区别只有一处：**LC 1600 在构造函数里给一个 `kingName`；这里没有**——第一次
`birth()` 调用里的 *parent* 就是奠基者（founder），此后永远不变（即使他后来死了）。

## API 契约（英文签名）

```python
class ThroneInheritance:
    def birth(self, parent_name: str, child_name: str) -> None
    def death(self, name: str) -> None
    def get_inheritance_order(self) -> list[str]
    def succession_after(self, name: str) -> str        # Part 3
```

## 规则

### Part 1 — 建树、死亡标记、继承顺序

- **奠基者**：第一次 `birth(parent, child)` 调用里的 `parent` 成为奠基者（founder），此后所有
  查询都从他开始；`parent_name == child_name`（自己当自己父母）→ `ValueError`。**(reconstructed)**
- 此后每次 `birth(parent, child)`：`parent` 必须已经在家谱里（曾作为某次 `birth` 的 parent 或
  child 出现过，或就是奠基者），否则 → `ValueError`（"unknown parent"）；`child` 不能是家谱里
  已出现过的名字（无论之前是当过 parent 还是 child）→ 否则 `ValueError`（"duplicate child"）。
- 同一 parent 的多个孩子按 **出生顺序** 排列（不是字母序）。
- `death(name)` **幂等**：调用在世的人、已死的人、甚至从未出生过的名字都不报错，只是把这个
  名字标记为"死"；**死人不会被移出家谱**——他们的分支结构原样保留，他们**活着的后代**照样出
  现在继承顺序里，而且死人自己后续还能作为 parent 生育新的孩子（家谱按调用顺序，不按真实时间）。
  **(reconstructed)**
- `get_inheritance_order()`：从奠基者开始的**先序遍历**，同一层孩子按出生顺序访问；结果里
  **跳过死人**（但仍然遍历他们的子树）；家谱为空（还没有任何 `birth` 调用）→ `[]`。

### Part 2 — 无递归、O(living + dead)

`get_inheritance_order()` 的先序遍历**禁止使用 Python 递归**（`def dfs(node): ... dfs(child)`
这种写法在一条 10 万级深的单链家谱上会撞上默认递归深度上限而 `RecursionError`）——必须用显式
栈做迭代 DFS，时间与空间都是 O(家谱总人数)（活人 + 死人）。**(reconstructed)**

### Part 3 — 继位查询 `succession_after` **(reconstructed)**

`succession_after(name)`：沿着**完整先序**（死人也算在内，这样才能问"某个国王刚驾崩，谁是他
后面第一个还活着的继承人"）找到 `name` 的位置，返回**严格在它之后**第一个**还活着**的名字；
`name` 从未出生过，或它之后已经没有活人了 → `""`。

### 命令流

```
BIRTH <parent> <child>     成功不输出；自己当父母 / 重名 / 未知 parent → ERROR
DEATH <name>               永远不输出（幂等，未知名字也不报错）
ORDER                      空格分隔的继承顺序；空 → -
SUCCESSOR <name>           下一个活着的继承人；没有/未知 → -
```

## Worked examples（全部由 `solution.py` 实际运行得出）

```
PART 1
BIRTH rhea zoe
BIRTH rhea amy
BIRTH zoe leo
ORDER            → rhea zoe leo amy
DEATH zoe
ORDER            → rhea leo amy
```

```
空家谱：
ORDER            → -
```

```
错误与边界：
BIRTH rhea zoe
BIRTH amy zoe    → ERROR          （zoe 已经出生过，重名）

BIRTH rhea zoe
BIRTH ghost leo  → ERROR          （ghost 不在家谱里，未知 parent）

BIRTH rhea rhea  → ERROR          （自己当自己父母；奠基者未建立，家谱仍为空）
ORDER            → -

BIRTH rhea zoe
DEATH zoe
BIRTH zoe leo    → 不报错（死人也能再生孩子）
ORDER            → rhea leo       （zoe 死了被跳过，leo 是她活着的孩子照样出现）

BIRTH rhea zoe
DEATH zoe
DEATH zoe        → 不报错（幂等）
ORDER            → rhea

BIRTH rhea zoe
DEATH ghost      → 不报错（从未出生过的名字也能 DEATH，是空操作）
ORDER            → rhea zoe
```

```
PART 3
BIRTH rhea zoe
BIRTH rhea amy
BIRTH zoe leo
SUCCESSOR rhea   → zoe
SUCCESSOR zoe    → leo
DEATH zoe
SUCCESSOR rhea   → leo            （zoe 死了被跳过，下一个活人是 leo）
SUCCESSOR zoe    → leo            （查询"zoe 死后谁继位"依然可用，答案不变）
SUCCESSOR amy    → -              （amy 之后没人了）
SUCCESSOR ghost  → -              （从未出生过）
```

## 边界清单

- 空家谱：`get_inheritance_order() == []`；对任何名字 `succession_after(...) == ""`
- 第一次 `birth` 建立奠基者；奠基者死后仍是遍历起点、仍在家谱结构里
- 自己当自己父母（parent == child）→ `ValueError`，且不建立奠基者
- 重名孩子（曾当过 parent 或 child 都算）→ `ValueError`
- 未知 parent（奠基者已存在之后）→ `ValueError`
- 同一 parent 的多个孩子按出生顺序，不按字母序（用刻意乱序的名字验证）
- `death` 三种输入都不报错：活人、已死的人、从未出生的名字（幂等 + 空操作）
- 死人的分支结构不消失：他们活着的后代照样出现在 `get_inheritance_order()`
- 死人还能作为 parent 生新孩子
- `succession_after` 用在死人身上依然有效（"他死后谁继位"）；用在最后一位、或从未出生的名字
  上返回 `""`
- 性能与实现约束：10 万级深的单链家谱，`get_inheritance_order()` 与 `succession_after()` 在
  `sys.setrecursionlimit()` 调得很低时依然不抛 `RecursionError`（证明是迭代不是递归），且在
  3 秒预算内完成

## 追问

1. **为什么"没有初始国王"是这题真正的坑？** LC 1600 原题构造函数直接给 `kingName`，遍历起点
   永远存在；这里必须处理"家谱还没有任何人"的状态——`get_inheritance_order()` 在此时必须返回
   `[]` 而不是抛异常，且第一次 `birth` 调用要把 parent（不是 child）种成根节点。
2. **为什么 `death` 要设计成幂等、对未知名字也不报错？** 继承系统的调用方（前端/其它服务）可
   能重放事件或乱序到达；把 `death` 设计成"总是安全"的操作，比每次都校验存在性再决定报不报错
   更健壮，也符合"幂等操作"是分布式系统里常见的防御性设计这一点。
3. **为什么迭代 DFS 而不是递归？** 面试里会直接给"10 万级深"的场景逼你意识到 Python 默认递归
   深度上限（约 1000）；用显式栈做先序遍历是标准手法，也是"树/图遍历不要用语言默认递归"这条
   通用经验在这里的具体体现。
4. **`succession_after` 为什么要在"包含死人的完整顺序"上定位，而不是在 `get_inheritance_order()`
   的结果上定位？** 因为真实场景就是"国王刚死，问谁继位"——如果只能在已经过滤掉死人的列表里
   查找，你就没法以"刚死的这个人"为锚点去问下一个继承人是谁；这也是为什么本题把这个 API 命名
   为 `succession_after` 而不是简单的"下一个下标"。

## 来源与置信度

- **MED**：fastprep "Snowflake Throne Inheritance without initial king"，Medium，Phone Screen，
  "Source Match: 86% (adapted from original problem)"（即改编自 LC 1600 "Throne Inheritance"）：
  https://www.fastprep.io/problems/snowflake-throne-inheritance-without-initial-king ；全文见
  `../../../../catalog/raw/ood.md` #8。
- 具体的错误分类（自己当父母、死人再生子女、`succession_after` 的语义）为重建，见各条标注。

## 考什么

S09 类设计先定契约（"没有初始国王"这个边界必须在写代码前想清楚）· 树遍历用迭代而非递归应对
深链输入 · 幂等操作的防御性设计 · 用同一份底层遍历同时服务"给我完整顺序"和"给我某人之后是谁"
两种查询形状。
