---
slug: task-scheduler-ii
---
## Q
**LC 2365 任务调度器 II**｜Medium

`tasks[i]` 是第 `i` 个任务的类型，必须按顺序完成，每天做一个任务或休息；同类型两个任务之间至少隔 `space` 天。求完成全部任务的最少天数。

## A
**一句话。** 顺序固定，不用逐天模拟：哈希表记每种类型上次做的那天，当前任务的日子取「前一天 + 1」和「上次 + `space` + 1」的较大者。

```python
def task_scheduler_ii(tasks, space):
    last = {}                 # 类型 -> 上次做它的那天
    day = 0
    for t in tasks:
        day += 1              # 每个任务至少过一天
        if t in last:
            day = max(day, last[t] + space + 1)  # 跳过休息日
        last[t] = day
    return day
```

**复杂度。** 时间 `O(n)`，空间 `O(不同类型数)`。

**易错点。**
- 逐天模拟休息：`space` 可到 `10^5`，天数可达 `10^10`，必然超时。
- 间隔写成 `last[t] + space`：中间要隔满 `space` 天，最早是 `last[t] + space + 1`。

**追问。**
- 任务可以重排（LC 621）？：顺序自由时看最高频次：`(maxf - 1)(space + 1) + 最高频的类型数`，再和任务总数取大。

**同模式。** LC 1 两数之和、LC 219 存在重复元素 II、LC 621 任务调度器
