# ps13 · Incident Monitor：按 (merchant, status_code) 分组的滑动窗口 + 状态翻转，练的是"阈值方向语义不能想当然"

> [!tldr]
> - 这题考的是：对每个 `(merchant_id, status_code)` 独立维护一个滑动窗口错误计数，计数跨过阈值就发 `TRIGGER`/`RESOLVE`；再叠加乱序输入、按商户覆盖规则、三档告警梯度
> - 三步套路：先把"滑动窗口 + 状态翻转"在**单个 pair** 上写对（deque 进出 + 一个布尔状态） → 用 `defaultdict` 把这套逻辑套到每个 pair 上，绝不共享一个全局 running sum → 后面的 Part 只是换"排序方式"或"阈值来源"或"档位数量"
> - 最值得带走的一个模式：**"触发/恢复"是状态翻转，不是每次都拿当前值和阈值比**——只在"跨过边界的那一刻"发事件，状态本身（当前是否在阈值之上）才是要记的东西，不是历史事件本身

这题**部分**基于真实候选人报告：Part 1 的规则（滑动窗口、`TRIGGER`/`RESOLVE` 的 `<`/`>=` 双向语义）有 PracHub 结构化题面佐证，但报告标题和本仓库的题目名对不上，候选人自己也说"后面几个 Part 记不清了"。**Part 2 起的规则、全部输入输出格式都是本仓库自拟，练的是里面的 S04/S05/S10/S12/S16 技能，别背格式。**

## 1. 题目在说什么（人话版）
Stripe 的错误率监控盯着每个 `(merchant_id, status_code)` 组合：滚动窗口内的错误数一旦够到阈值就报警（`TRIGGER`），后来降回阈值以下就解除（`RESOLVE`）。四个 Part：① 输入已按时间排好序的单一全局规则；② 输入乱序，要先按 `(timestamp, 输入位置)` 排序；③ 每个商户可以有自己的窗口/阈值覆盖默认规则；④ 从"触发/恢复"两态升级成"正常/警告/严重"三档，一条记录可能一次跨两个边界。

```
WINDOW=3 THRESHOLD=4
1,m1,500,2   2,m1,500,2   5,m1,500,1   6,m1,500,1
-> 2,m1,500,TRIGGER      (窗口[0,2]: 2+2=4>=4)
-> 5,m1,500,RESOLVE      (窗口[3,5]: 只剩1<4)
```

## 2. 读题：把文字变成模型
- **实体**：日志记录（`timestamp, merchant_id, status_code, count`），分组 key 是 `(merchant_id, status_code)`。
- **输入长什么样**：一行参数（`WINDOW=.. THRESHOLD=..`，Part 3/4 换成别的参数形状）+ 若干日志行。
- **输出要什么**：每个触发/恢复事件一行 `timestamp,merchant,status,EVENT_TYPE`，按**处理顺序**（Part 2 起是排序后的顺序）。
- **状态**：每个 pair 一个 deque（还在窗口内的记录）+ running sum + 一个"当前是否在阈值之上"的布尔量。**绝不能用一个全局 deque/sum 给所有 pair 共用**。
- **一句话建模**：这是一个 **按 key 分组、各自独立维护滑动窗口和二值/三值状态** 的问题，Part 2-4 都是在"分组"和"状态机"这两个维度上做变体。

> [!note] 为什么"状态翻转"比"每次都比阈值"更对
> 候选是"每条记录都检查一次 `sum >= threshold`，是就输出 TRIGGER"——但这样同一个 pair 连续 5 条记录都在阈值之上会输出 5 次 TRIGGER，题面明确要求"只在跨越的那一刻"。正确做法是每个 pair 记一个"当前状态"（在/不在阈值之上），只有状态真的翻转了才发事件——这是把"边沿触发"和"电平触发"分清楚的经典坑，Part 4 的三档升级把它继续放大成"一次记录可能连续翻过两个边沿，要按顺序都发出来"。

## 3. 下笔顺序（面试里就按这个顺序敲）
1. **骨架先行**：`main()` 解析 `PART n` + 参数行 + 日志行，分发。先写 `_parse_records`（4 字段整数校验）。
2. **Part 1 最小可用**：`defaultdict` 给每个 pair 存 `(deque, running_sum, above_threshold)`；顺序处理每条记录：进 deque、加 sum、弹出窗口外的旧记录、减 sum，然后检查这个 pair 的布尔状态是否要翻转，翻转才输出一行。用样例自测边界（窗口恰好卡在 `t-W+1`）。
3. **Part 2 叠加**：加一层排序 `sorted(records, key=lambda r: (r.ts, r.order))`（`order` 是输入位置，保证同时间戳的 tie-break 是输入序不是别的），排序后调用 Part 1 完全相同的核心循环——**核心循环一行不改**。
4. **Part 3 叠加**：加一个"按商户查规则"的小函数 `rule_for(merchant) -> (window, threshold)`（有覆盖用覆盖，没有用默认），核心循环从"全局一份 window/threshold"改成"每次先查这个记录所属商户的规则"，其余逻辑不变。
5. **Part 4 叠加**：把布尔状态换成 0/1/2 三档 `_level(total, warn, crit)`，写一个"从旧档位走到新档位，依次跨过哪些边界"的小函数，每跨一个边界发一个事件（方向决定事件名）。
6. **收尾**：确认没有把一个 pair 的窗口/状态和另一个共享；确认 Part 4 一次记录可能连发两个事件，且顺序是"先近后远"（升的时候先 WARN 再 CRIT，降的时候先 CRIT 再 WARN）。

## 4. 代码怎么组织
```
_parse_records(lines) -> list[Record]              # 4 字段整数解析
_parse_and_sort(lines) -> list[Record]              # Part2 起：按 (ts, 输入位置) 排序
_events_single_threshold(records, rule_for) -> list[str]   # Part1/2/3 共用的核心循环，两态翻转
_level(total, warn, crit) -> int                    # Part4：三档判定
_events_two_level(records, warn, crit, window) -> list[str]  # Part4 的核心循环，逐边界发事件
part1..part4(lines)                                  # 解析 -> 选规则来源 -> 调核心循环 -> 格式化
main(stdin, stdout)
```
拆分原则：**"怎么排序"和"规则从哪来"和"核心的窗口+状态机循环"三件事分开**。`_events_single_threshold` 接受一个 `rule_for(merchant)` 回调而不是写死 `(window, threshold)`，这样 Part 1（全局一份规则）和 Part 3（按商户查规则）能共用同一个核心循环——只有 Part 4 因为状态从二值变三值才需要一个新的核心循环，但排序和分组这两层完全复用。

## 5. 核心代码（骨架，≤ 40 行，带注释）
```python
# 只放主线：分组滑窗 -> 状态翻转 -> 三档梯度。省略参数解析与商户规则查表细节。
def _events_single_threshold(records, rule_for):
    state = defaultdict(lambda: (deque(), 0, False))   # pair -> (窗口, running_sum, 是否在阈值之上)
    out = []
    for r in records:
        window, threshold = rule_for(r.merchant_id)
        key = (r.merchant_id, r.status_code)
        live, total, above = state[key]
        live.append(r); total += r.count
        while live[0].ts < r.ts - window + 1:          # 踢掉窗口外的旧记录
            total -= live.popleft().count
        now_above = total >= threshold
        if now_above != above:                          # 只在状态翻转的一刻发事件
            out.append(f"{r.ts},{r.merchant_id},{r.status_code}," + ("TRIGGER" if now_above else "RESOLVE"))
        state[key] = (live, total, now_above)
    return out

def _level(total, warn, crit):                          # Part4：0/1/2 三档
    return 2 if total >= crit else 1 if total >= warn else 0

def _events_two_level(records, warn, crit, window):
    state = defaultdict(lambda: (deque(), 0, 0))         # 多存一个 level
    boundary_events = {(0, 1): "TRIGGER", (1, 2): "ESCALATE", (2, 1): "DEESCALATE", (1, 0): "RESOLVE"}
    out = []
    for r in records:
        key = (r.merchant_id, r.status_code)
        live, total, level = state[key]
        live.append(r); total += r.count
        while live[0].ts < r.ts - window + 1:
            total -= live.popleft().count
        new_level = _level(total, warn, crit)
        step = 1 if new_level > level else -1
        while level != new_level:                        # 一次记录可能连跨多个边界，逐个发
            nxt = level + step
            out.append(f"{r.ts},{r.merchant_id},{r.status_code},{boundary_events[(level, nxt)]}")
            level = nxt
        state[key] = (live, total, level)
    return out
```

## 6. 面试里怎么说（边写边讲）
- 开始前：「我确认一下窗口是闭区间 `[t-W+1, t]`，`TRIGGER`/`RESOLVE` 都是非严格的 `>=`/`<`，同一时间戳的记录按输入序处理。」
- 写 Part 1 时：「每个 `(merchant, status)` 对我单独存一个 deque 和 running sum，绝不共用一份，否则不同商户的错误会互相污染。触发/恢复我记一个布尔状态，只在状态真的翻转时才输出，不是每条记录都判一次。」
- 写 Part 2 时：「乱序输入我先排序，tie-break 用输入位置而不是随便选一个字段，这样同一时间戳的记录处理顺序和原始文件一致。」
- 写 Part 4 时：「三档我抽成一个 `_level` 函数，核心循环变成'从旧档走到新档，逐个边界发事件'，这样将来要加第四档也只用改 `_level` 和事件映射表，不用碰循环结构。」
- 交付时：「样例都过了；我特意测了'一条记录直接从 0 跳到 2 档'这种情况，确认先发 TRIGGER 再发 ESCALATE，顺序符合题面。」

## 7. 常见跑偏（方法层面，3 条）
- **所有 pair 共用一个 running sum/deque**：小样例只有一个商户时看不出问题，一旦有两个不同的 `(merchant, status)` 组合，错误计数就会互相污染——分组这一步必须先做，且用 `defaultdict` 天然隔离，不要偷懒共享一份状态。
- **每次都拿"当前值 vs 阈值"判断要不要发事件，而不是记状态**：会在连续多条记录都在阈值之上时重复发很多次 `TRIGGER`——先想清楚这是"边沿触发"，状态本身要被记下来，事件只在状态改变的那一刻发生。
- **Part 4 只处理"移动一步"的情况，没考虑一次记录跨两个边界**：`if new_level > level: emit(...)` 这种写法只发一个事件，遇到"从 0 直接跳到 2"的用例就漏发——升级到多档阈值时要用循环"走完每一步"，不是简单的 if-elif。

## 8. 同族题 / 延伸
- 与 `problems/q41_observability_metrics` 主题相邻（都是"可观测性/监控告警"），但**规则集完全不同，不要混着背**：q41 是"指标聚合 → 时间窗 → 告警规则"的更通用管线，具体聚合方式（sum/avg/max）、告警形状（单阈值/滞回）可能都和这题的 `[t-W+1,t]` 闭区间求和不一样；事件命名也不同（这题是 `TRIGGER/RESOLVE/ESCALATE/DEESCALATE`，q41 应以自己的 problem.md 为准）。两题唯一相同的是"按 key 分组 + 时间窗 + 状态机"这个方法论骨架。
- 同族模式：ps01 Part 2（60 秒窗口累计触线）是这题 Part 1 的近亲，都是 deque 滑窗 + running sum，区别只在"触线只报一次"还是"触线/恢复都要报"。
- 延伸思考：如果告警要支持"连续 N 条超阈值才真正触发"（防抖），只需要在状态里多存一个"连续超阈值计数"，不用改滑窗结构。
- 练习命令：`python3 loop/mock.py start ps13 -m 45`
