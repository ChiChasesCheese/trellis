# q07 · 订阅通知调度（欢迎 / 到期预警 / 已过期 + 改套餐 + 续期）

> `problems/q07_subscription_notifications/` · 4 个 part · OA + VO 都出现（13 个来源）
> **主题：后来的事件会作废前面已经排好的计划，但已发出的不能撤回。**

## 一句话题意

每个订阅在三个时点发邮件（开始日、结束日前 15 天、结束日）。
`CHANGE` 改套餐名，`RENEW` 延长期限并**重算**尚未发出的邮件。
按时间序输出完整的邮件与事件序列。

## 时间模型（题面明确）

日期是**整数天偏移**，没有日历。`start=s`、`duration=d` 的订阅：
**活跃天是 `s .. s+d-1`，结束日 `end = s + d`（不活跃的第一天，"已过期"邮件发在这天）。**

## 输入 / 输出

```
PART n
name,plan,start_day,duration_days     用户记录；重名则替换且取后面的位置
CHANGE,name,new_plan,day              Part 2+
RENEW,name,extra_days,day             Part 3+
```

输出（Part 1–3）：`day: name - message`，事件是
`day: [Changed] name - old -> new` / `day: [Renewed] name - old_end -> new_end`。

**排序（三级 tie-break，必须背下来）**：
① 按天升序 → ② 同一天：**先按用户输入顺序** → ③ 同一天同用户：**事件在邮件之前**，
事件按输入序、邮件按日程序（welcome → warning → expired）。

## 核心考点

`S01` 长 spec · `S02` 混合记录类型 · `S03` 按 id 建记录 · **`S08` 多键 tie-break** ·
`S09` 带标签的格式 · **`S10` 会改变先前决定的事件流** · `S12` 天偏移算术 · `S19` 增量

## 解题思路

### Part 1 — 排期

```python
end = start + duration
schedule = [(start,      f"Welcome to {plan}"),
            (end - 15,   "Upcoming expiry"),
            (end,        "Subscription expired")]
emails = [(d, msg) for d, msg in schedule if d >= start]     # ★ 早于 start 的不发
```

- duration < 15 → **没有预警**。
- duration == 15 → 预警**就在 start 当天**，排在 welcome 之后。
- duration == 0 → welcome 和 expired **同一天**。

### Part 2 — 改套餐

`CHANGE` 在 `day` **当天开始时**生效（在当天的邮件之前）：
打印 `[Changed]` 行，且所有 `day >= 当天` 的邮件用新套餐名。
日期不变；同名套餐的 CHANGE **也要打印**。

### Part 3 — 续期（本题最难的一条规则）

```
new_end = old_end + extra_days           从**旧的结束日**延长，与续期发生在哪天无关
```

重算之后：

> **一封邮件会被发出，当且仅当 `email_day >= start_day` 且 `email_day >= 触发重算的事件日`。**

也就是说：
- 续期**之前**已经发出的邮件**永久保留**，不会被撤回。
- 尚未发出的（`day >= 事件日`）被重算后的替换。

推论（题面列出的）：
- 续期前已发的预警**留着**，同时会在新结束日前 15 天再发一封（如果那天 `>= 事件日`）。
- **在结束日当天续期 → 抑制"已过期"邮件**（因为 `new_end > day`）。
- **过期之后续期 → 旧的"已过期"邮件保留**，新结束日再发一封（若 `new_end >= day`）。

事件按天序处理，同天按输入序；`CHANGE` 和 `RENEW` 可以混着来。

### Part 4 — 规则驱动的单日变体

给一个 `current_day`，对每个账户跑每条规则：

```
on_create:               current_day == created_day + offset
days_before_expiration:  current_day == expires_day - offset
after_expiration:        current_day == expires_day + offset
```

输出 `account_id rule_name template`，账户按输入序、规则按配置序。要求近线性（≤ 2·10^5 行）。

## 坑

1. **`end = start + duration`，"已过期"发在 end 当天**（不是 `end - 1`）。
2. **早于 start 的邮件不发。** duration 15 的预警恰好落在 start，要发，且在 welcome 之后。
3. duration 0 → welcome 与 expired 同天。
4. **三级 tie-break**：天 → 用户输入序 → 事件先于邮件 → 事件输入序 / 邮件日程序。
5. `CHANGE` 在 start 当天 → welcome 用**新**套餐名。
6. **续期从旧 end 延长**，不是从续期日。
7. **已发出的邮件永不撤回**；`day >= 事件日` 的才被替换。
8. 在 end 当天续期 → 抑制 expired；过期后续期 → 旧 expired 保留。
9. 同一用户同一天两个事件 → 按输入序；事件可能**乱序**给出 → 先按天排。
10. **未知用户的事件忽略**；`extra_days = 0` **仍要打印** `[Renewed] 30 -> 30`。
11. 格式：`[Changed]`/`[Renewed]` 后有一个空格，`->` 两边有空格，**无尾随空格**。
12. **重名的用户记录**：替换先前的，且**取后面的位置**（影响 tie-break）。

## 变体

- 日历日期（`YYYY-MM-DD`）+ `timedelta(days=15)`（VO 形式）。
- tie-break 按 subscription id（这里就是输入位置）。
- 第 4 个 part：取消事件 → 之后不再发邮件（等价于 `end = day` 且丢弃待发）。
- 自定义日程偏移（`-7`、`-1`）。

## Code Core 节点

**`model.event-stream`** · **`model.reversal`**（重算 = 作废待发） · `chrono.arithmetic` ·
**`output.ordering`**（三级 tie-break） · `output.formatting` · `round.reading`

## 自测清单

- [ ] duration 14 / 15 / 16 三种（无预警 / 预警在 start / 正常）
- [ ] duration 0
- [ ] 同一天多个用户 / 同一天事件与邮件
- [ ] CHANGE 在 start 之前 / 当天 / 之后
- [ ] RENEW 在预警日之前 / 当天 / 之后
- [ ] RENEW 在 end 当天（抑制 expired）
- [ ] RENEW 在过期之后（旧 expired 保留 + 新的一封）
- [ ] 同用户同天两个事件、事件乱序给出
- [ ] 未知用户的事件、`extra_days = 0`
