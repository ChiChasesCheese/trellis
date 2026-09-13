# q41 · 可观测性指标（事件流 → 时间窗聚合 → 带迟滞的告警）

> `problems/q41_observability_metrics/` · 4 个 part · **重建题（非真题），置信度极低**
>
> interviewdb.io 上确实有一道标题叫「Observability」的 Stripe OA 题（2026-08 被发现更新），但正文
> 区域全程是前端占位符，WebFetch 多次抓取拿不到任何规则、输入输出格式或样例；PracHub 上一道同主题的
> onsite 系统设计题只能当"这道题大概率是指标/告警方向"的旁证，不能当题面用。**题面、part 划分、输入
> 输出格式全部是本仓库自拟**，练的是 `study/00-essentials/02-core-topics.md` 里的
> **S02（行式解析）· S05（阈值语义）· S08（确定性排序）· S09（字节级输出）· S10（事件流/状态机）·
> S12（时间分桶）· S16（滑动窗口）** 这七个考点，**不要把这里的输出格式（`MALFORMED`/`DROPPED` 行、
> `.2f` 格式、`ALERT_ON/ALERT_OFF` 文案）当成真题格式去背**——换一家公司出的同类题，格式一定不一样，
> 考点才是能带走的东西。

---

## 一句话题意

解析一串 `timestamp,metric_name,labels,value` 指标事件，按时间窗聚合成 count/avg/百分位数，再用一套
"连续 N 个窗口满足条件才触发、连续 M 个窗口不满足才解除"的迟滞状态机跑告警规则，Part 4 再叠加"事件
按到达顺序处理、超过容忍窗口数的迟到事件要被丢弃"这个真实流式系统都要面对的问题。

---

## 输入 / 输出

```
PART n
WINDOW <size> <step>          Part 2/3/4 才有；size/step 单位秒，1<=step<=size
RULES                          Part 3/4 才有
<rule row>                    metric_name,labels,stat,op,threshold,trigger_n,clear_n[,value_threshold]
LATENESS <L>                   Part 4 才有
EVENTS
<event row>                   timestamp,metric_name,labels,value
```

- 小节按固定顺序累积出现（`PART n` 只包含它该有的那几节，见上）；标记行大小写敏感、逐字匹配。
- **`labels`**：`-`（无标签）或 `key1=val1;key2=val2`（分号分隔，键唯一）；**必须规范化**（按 key
  排序）后再参与分组——`b=2;a=1` 和 `a=1;b=2` 是**同一个 series**。
- **规则行是可信配置，不是数据流**：格式错就是致命 `ValueError`，不是"跳过计数"；`stat=rate` 时才
  多一个第 8 字段 `value_threshold`（否则不能有这个字段）。
- **事件行畸形就跳过并计数**（`MALFORMED`），4 种独立原因：字段数不对 / `timestamp` 不是非负整数 /
  `value` 不是合法浮点 / `labels` 格式不对。
- 输出：每个 part 自己的行 + 结尾 `MALFORMED <n>`；Part 4 在 `MALFORMED` **之前**多一行
  `DROPPED <n>`。所有聚合数值用 Python 的 `f"{x:.2f}"` 语义格式化，不自造舍入规则。

---

## 核心考点

`S02` 行式解析 + labels 规范化 · **`S12` 时间分桶（半开区间、整数除法）** ·
**`S05` 阈值语义（`gt/gte/lt/lte` 严格 vs 非严格；`count` 计数 vs `rate` 比率）** ·
`S10` 事件流 + 显式状态机（只在翻转时输出） · **`S16` 滑动窗口（重叠成员关系）** ·
`S08` 确定性排序（Part 1/2 排序 vs Part 3/4 刻意不排序） · `S09` 字节级输出（`.2f`、尾行永远存在）

---

## 解题思路

### 状态形状（从 Part 4 倒推）

```python
class Event(NamedTuple):
    timestamp: int; metric: str; labels: str; value: float   # labels 已规范化

class Rule(NamedTuple):
    metric: str; labels: str; stat: str; op: str
    threshold: float; trigger_n: int; clear_n: int
    value_threshold: float | None                              # 仅 stat=="rate" 时非空
```

**★ 按 series 存成排好序的 `(timestamps, values)` 对，而不是按窗口存**：窗口数量通常远小于事件数
量，每个窗口用 `bisect_left` 在时间线上做一次范围查询，比"对每个事件反推它属于哪些窗口"更高效也更
好写：

```python
def window_values(ts, vals, size, step, k):
    lo, hi = k * step, k * step + size
    i, j = bisect_left(ts, lo), bisect_left(ts, hi)
    return vals[i:j]
```

### Part 1 — 解析 + 按 (metric, 规范化 labels) 聚合

```python
def canonicalize_labels(raw):
    if raw == "-": return "-"
    pairs = [p.partition("=") for p in raw.split(";")]
    if any(not k or "=" not in p or not v for p, (k, _, v) in ...): return None   # 畸形
    return ";".join(f"{k}={v}" for k, v in sorted(pairs, key=lambda kv: kv[0]))
```

**★ 规范化必须在分组之前做**，不是"先按原始字符串分组，输出时再排序"——否则 `b=2;a=1` 和 `a=1;b=2`
会被当成两个不同的 series，题面 worked example 专门给了这个反例（`us=1;region=us` 排序后变成
`region=us;us=1`，和纯 `region=us` 是不同 series，即便后者是前者的子串）。

### Part 2 — 时间窗 + 百分位数

- `window k` 覆盖 `[k*step, k*step+size)` 半开区间；`step==size` 是不重叠的滚动窗口，`step<size`
  是重叠的滑动窗口——**一个事件同时落进多个窗口是设计好的行为，不是需要去重的 bug**，这正是 `S16`
  要考的滑动窗口语义。
- 百分位数用 **nearest-rank**，不是插值：`rank = ceil(P/100 * n)`（1-indexed），`p50` 在偶数长度
  窗口上取的是"中点靠后"的那个元素，不是两者平均——这是本题自拟的定义，题面明确写"匹配 `.2f` 语义,
  不要自造舍入规则"对应的就是这条。

### Part 3 — 告警迟滞状态机（本题真正的核心）

```python
state, up, down = "OK", 0, 0
for k in range(max_k + 1):
    cond = compare(stat_at(k), rule.op, rule.threshold)
    if cond: up, down = up + 1, 0
    else:    down, up = down + 1, 0
    if state == "OK" and up == rule.trigger_n:
        state = "FIRING"; emit("ALERT_ON", k); up = 0
    elif state == "FIRING" and down == rule.clear_n:
        state = "OK"; emit("ALERT_OFF", k); down = 0
```

**★ 迟滞（hysteresis）的核心：触发和解除比较的是"同一个条件"的两个相反方向，而 `op` 的严格/非严格
在这两个方向上正好翻转。** 举例：规则 `op=gte, threshold=100`，`stat==100` 时 `condition=True`（推
进 `up`，可能触发）；规则换成 `op=gt, threshold=100`，同样 `stat==100` 时 `condition=False`（推进
`down`，可能解除）。也就是说，**"严格 vs 非严格"这一个字段的选择，同时决定了"恰好等于阈值算不算异
常"和"恰好等于阈值算不算已经恢复"这两件事**——面试或做题时最容易漏掉的地方是只测了触发方向的边界，
没测解除方向的边界。

- **`max_k` 是全局的、跨规则共享的**：由整个事件流里出现过的最大 timestamp 决定，不是某条规则自己
  的数据决定。这意味着一条规则的 metric 如果"突然不再上报了"，它对应的 `count`/`avg`/`rate` 在后续
  每个窗口都是按"零匹配事件"计算（`avg`/`rate` 定义成 `0.0`），`consecutive_false` 会照常推进直到
  真正解除——**沉默不是跳过，沉默是一连串 `0.0` 的窗口**。
- **`rate` 分母为 0 时显式定义为 `0.0`，不是崩溃也不是"未知"**——除非 `op` 本身接受 `0.0`
  （如 `lte 0.0`），否则这种窗口永远不会触发。
- **输出顺序刻意不排序**：按 `RULES` 小节的输入顺序遍历规则，因为每条规则自己的转移序列本来就是按
  窗口时间线天然递增的，强行按 metric 名排序反而会打乱"这是一条时间线"的语义——这是 `S08` 里"什么
  时候不该排序"的反例。

### Part 4 — 乱序到达 + watermark 丢弃

```python
max_primary_seen = -1
for row in events_in_arrival_order:            # ★ 不重新按 timestamp 排序
    ev = parse(row)
    primary = ev.timestamp // step              # 原生分桶，与滑动窗口成员关系无关
    if primary < max_primary_seen - L:
        dropped += 1; continue                  # 太迟，丢弃，不参与任何窗口聚合
    incorporate(ev)                              # 正常并入它所属的（可能多个）滑动窗口
    max_primary_seen = max(max_primary_seen, primary)
```

丢弃之后，**用和 Part 3 完全相同的规则评估逻辑**跑一遍剩下的数据。

**★ "乱序"和"迟到"是两个不同的概念，容易被混为一谈**：`L=0` 时，只要一个事件的主分桶落后于当前见
过的最大主分桶就算迟到会被丢；但同一个主分桶内的乱序到达（比如先来了 `t=105` 再来了 `t=101`，两者
`primary` 都是 `101//10=10` 假设 `step=10`... 具体取决于 `step`）**不算迟到**，因为它们没有让
`max_primary_seen - L` 的下限失效。判断的是"分桶编号"而不是"具体时间戳"的先后。

---

## 坑（隐藏测试专门抓的）

1. **labels 顺序打乱必须合并成同一 series**：`b=2;a=1` 和 `a=1;b=2` 是同一个，规范化要在分组**之
   前**做。
2. **`gt` vs `gte`、`lt` vs `lte` 在恰好等于阈值处的分歧**，且这个分歧在"触发方向"和"解除方向"上
   同时生效，只测一个方向的边界不够。
3. **`rate` 分母为 0 → `0.0`**，不是崩溃、不是"未知"，也不是"跳过这个窗口不计入 `max_k` 走查"。
4. **`trigger_n=1`**：`OK` 状态下第一个满足条件的窗口立即触发，触发后 `consecutive_true` 清零——这
   意味着 `trigger_n=1` 的规则理论上可以"这个窗口刚触发,下一个窗口立刻又不满足又满足"反复横跳,要按
   状态机字面语义实现,不要图省事加一个"至少等一个窗口"的隐藏冷却。
5. **一条规则的 metric 全程未出现**：仍然要沿着别的 metric 决定的 `max_k` 走一遍全 `0`（或
   `0.0`）窗口序列,不能因为"这个 series 不存在"就跳过整条规则的评估。
6. **偶数长度窗口的 `p50`**：nearest-rank 定义下取的是"中点靠后"的元素,不是两者平均——和插值定义
   混淆是最常见的错误。
7. **滑动窗口下一个事件出现在多个窗口里**：是正确行为,不能去重,也不能只算进"第一个匹配的窗口"。
8. **Part 3/4 的告警转移行不排序**，用 `RULES` 出现的原始顺序;这一点和 Part 1/2 的"必须排序"正好
   相反,是本题 `S08` 故意设的对照组。
9. **Part 4 的 `L=0`**：任何落后于当前 watermark 的到达都算迟到被丢,但"落后"判断的是分桶编号而不
   是具体时间戳,乱序但同分桶不算迟到。
10. **丢弃是真丢弃，不是只在计数器上做样子**：被丢的事件必须从聚合和后续的规则评估里彻底剔除——
    隐藏测试专门构造了"丢弃与否直接改变某条 `ALERT_ON` 是否出现"的用例来验证这一点。
11. **`MALFORMED`/`DROPPED` 两行永远存在**（哪怕是 0），且顺序固定（`DROPPED` 在 `MALFORMED` 之
    前）。
12. **规则行本身格式错是致命错误**（`ValueError`），和事件行畸形"跳过计数"是两套完全不同的容错策
    略——一个是可信配置，一个是不可信数据流，弄反了两种处理方式是这题最容易犯的方向性错误。

---

## 变体

无——这是从零重建的训练题（见开头置信度说明），不是真实来源的题面变体列表。如果在别的公司遇到类似
"metrics + alerting"的 OA/系统设计题，大概率会换成不同的输入格式和阈值语义，但"迟滞状态机""滑动
窗口重叠成员""乱序到达 watermark"这三个模式本身是可迁移的，认出它们比记住这题的字段名更重要。

---

## Code Core 节点

`input.line-protocols` · `input.malformed` · **`chrono.windows`** · **`rules.thresholds`** ·
`model.event-stream` · **`model.state-machine`**（trigger/clear 迟滞） · `output.ordering`
（该排序 vs 不该排序的对照） · `output.formatting`（`.2f`、尾行恒在）

---

## 自测清单（写完逐条跑）

- [ ] 题面 Part 1 worked example，逐字节
- [ ] labels 顺序打乱后合并成同一 series；`-` 无标签 sentinel
- [ ] 4 种畸形事件行各自触发且互不影响 `MALFORMED` 计数
- [ ] 规则行格式错 → 程序应该崩溃（`ValueError`），不是跳过
- [ ] `count==threshold` 时 `gt` 不触发、`gte` 触发（触发方向）
- [ ] 同一个边界值在"解除方向"上的对应测试（`lt`/`lte`）
- [ ] `rate` 窗口零匹配事件 → `0.0`，不崩溃
- [ ] `trigger_n=1` 立即触发；触发/解除各来一次（两条独立的 `ALERT_ON`/`ALERT_OFF`）
- [ ] 一条规则的 metric 全程不出现，仍按全局 `max_k` 走一遍 0 值窗口
- [ ] 偶数长度窗口的 `p50` 边界
- [ ] 滑动窗口（`step<size`）一个事件落进 2–3 个窗口
- [ ] 滚动窗口（`step==size`）验证无重叠
- [ ] `L=0` 时任何落后 watermark 的到达被丢；同分桶乱序不算迟到
- [ ] 构造一个"丢弃与否改变 `ALERT_ON` 是否出现"的用例
- [ ] `MALFORMED 0` / `DROPPED 0` 显式输出，顺序固定
- [ ] 10^5 事件规模的耗时（`bisect` 而不是逐事件反推窗口）
