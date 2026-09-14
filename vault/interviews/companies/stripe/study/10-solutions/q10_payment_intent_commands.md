# q10 · PaymentIntent 命令流（INIT / CREATE / ATTEMPT / SUCCEED / FAIL / REFUND）

> `problems/q10_payment_intent_commands/` · 4 个 part
> **主题：显式状态机 + "非法命令静默忽略"—— 几乎所有隐藏测试都在这句话里。**

## 一句话题意

按行重放一串 API 命令，维护每个 payment 的状态机和每个商户的余额，输出最终余额。
**任何不适用的命令（未知 id、状态不对、参数个数不对、数字解析失败）都静默忽略，不输出、不崩溃。**

## 输入 / 输出

```
PART n                      可选，缺省视为 PART 3
INIT    <merchant> <balance>
CREATE  <payment> <merchant> <amount>
ATTEMPT <payment>
SUCCEED <payment>
UPDATE  <payment> <amount>     Part 2+
FAIL    <payment>              Part 3+
REFUND  <payment>              Part 3+
```
Part 4：每行前面多一个整数时间戳，`INIT` 多一个可选的 `refund_limit`。金额是整数分，最多 2·10^5 行。

输出：每个被 `INIT` 过的商户一行 `merchant balance`，按**普通字符串序**。余额 0 也打印。

## 状态机

```
REQUIRES_ACTION --ATTEMPT--> PROCESSING --SUCCEED--> COMPLETED
       ^                          |
       +---------FAIL-------------+
```
`SUCCEED` 时才 `balance[m] += amount`。`REFUND` 只对 `COMPLETED` 且未退过的生效，`balance[m] -= amount`，
状态**仍是 COMPLETED**，第二次 REFUND 忽略。

## 核心考点

`S02` 解析 · `S03` 记录 + 按 id 的字典 · **`S10` 带反向的状态机** · **`S11` 幂等（重复 INIT/CREATE/REFUND）** ·
`S12` 时间窗口（Part 4） · **`S18` 校验与错误路径** · `S19` 增量

## 解题思路

```python
TRANSITIONS = {                    # (命令, 当前状态) → 新状态
    ("ATTEMPT", "REQUIRES_ACTION"): "PROCESSING",
    ("SUCCEED", "PROCESSING"):      "COMPLETED",
    ("FAIL",    "PROCESSING"):      "REQUIRES_ACTION",
}
```

把转移写成表，比一堆 `if` 少写一半代码且不会漏。**表里没有的组合 = 忽略。**

各命令的忽略条件（逐条对照题面）：

| 命令 | 忽略当 |
|---|---|
| `INIT m b` | `m` **已存在**（余额不重置） |
| `CREATE p m a` | `p` 已存在 / `m` 不存在 / `a < 0`（`a == 0` 合法） |
| `ATTEMPT p` | `p` 不存在 / 不在 `REQUIRES_ACTION` |
| `SUCCEED p` | `p` 不存在 / 不在 `PROCESSING` |
| `UPDATE p a` | `p` 不存在 / **不在 `REQUIRES_ACTION`** / `a < 0` |
| `FAIL p` | 不在 `PROCESSING` |
| `REFUND p` | 不在 `COMPLETED` / **已退过** |

**参数个数与整数解析**统一在 dispatch 之前挡掉：

```python
tok = line.split()
if not tok: continue
spec = ARITY.get(tok[0])
if spec is None or len(tok) != spec: continue      # 未知命令 / 参数个数不对 → 忽略
```

### Part 4（version C 语义）

- `t INIT m balance [refund_limit]`：缺省 → **永远可退**；`0` → **永不可退**；
  否则 `t_refund - t_create <= refund_limit`（**闭区间**）才可退。
- `t CREATE p m amount`：**立刻完成并立刻入账**（不需要 SUCCEED）。
- 被拒绝的 REFUND **不标记**该 payment，可以之后再试。
- 命令按**输入顺序**处理，`t` 只用于退款窗口判断。

## 坑

1. **第二次 `INIT` 同一商户不重置余额。**
2. `CREATE` 的三种忽略；`amount == 0` **合法**。
3. `SUCCEED` 没有先 `ATTEMPT` / `SUCCEED` 两次 / 对 `COMPLETED` 再 `ATTEMPT` → 全忽略。
4. **`UPDATE` 在 `ATTEMPT` 之后被忽略，但 `FAIL` 之后又可以了**；`SUCCEED` 入账的是**更新后**的金额。
5. `REFUND` 两次 / 对非 `COMPLETED` 的退 → 忽略；退的是**当初入账的那个金额**。
6. 余额 0 的商户也打印；排序是字符串序（`m10 < m2`）。余额可以为负。
7. Part 4：`t_refund - t_create == refund_limit` **允许**，`+1` 拒绝；`refund_limit 0` 永不退；
   缺省永远退；被拒的退款可重试。
8. Part 4：`CREATE` 立刻入账，**不需要 SUCCEED**。
9. 未知命令词 / 参数个数不对 / 非整数 → 忽略，**绝不崩溃**。
   （仓库的 adversarial review 在这里发现过一个真 bug：`INIT` 的参数个数判断。）

## 变体

- **Version B**（"Transaction Intent Management System"）：状态改名 PENDING/IN_PROGRESS/DONE，
  命令改名 START/NEW/PROCESS/COMPLETE/MODIFY/CANCEL/RETURN，全部带时间戳。
  → `part4(lines, immediate_credit=False)` + 换命令表。
- **Version C**：P1 只有 INIT/CREATE（立刻入账），P2 REFUND，P4 时间戳 + 窗口。就是上面的 Part 4。
- 输出成 `list[str]` 或 `{"m1": 1500}`。

## Code Core 节点

**`model.state-machine`** · **`model.idempotency`** · **`input.malformed`** ·
`model.entity-state` · `chrono.windows`（退款窗口） · `output.ordering` · `round.hidden-tests`

## 自测清单

- [ ] 重复 INIT 不重置
- [ ] CREATE 的三种忽略 + `amount == 0`
- [ ] 每个非法转移各来一次
- [ ] UPDATE → ATTEMPT（忽略）→ FAIL → UPDATE（生效）→ ATTEMPT → SUCCEED（入更新后的额）
- [ ] REFUND 两次 / 非 COMPLETED
- [ ] 余额 0 / 负余额 / `m10` vs `m2`
- [ ] Part 4 窗口的 `==` / `+1` / `0` / 缺省
- [ ] 参数个数错、非整数、未知命令词
