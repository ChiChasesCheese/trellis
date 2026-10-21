# oa01 · Job Chain 报表（OA，1 题，100–120 分钟）


## 背景

调度系统里的 job 首尾相接组成若干条链：一个 job 跑完触发它的 `next_job_id`。给你一份 CSV 运行日志，
为每条链出一段统计；输入有任何不对就只输出 `Malformed Input`。

## 输入（stdin）

```
#job_id,runtime_in_seconds,next_job_id
1,60,23
23,30,3
3,15,0
5,200,0
```

* 第一行表头以 `#` 开头；空行忽略；逗号两侧可以有空格。
* `job_id > 0`；`runtime_in_seconds ≥ 0`；`next_job_id ≥ 0`，`0` 表示链尾。

## 输出（stdout）

```
-
start_job: 5
last_job: 5
number_of_jobs: 1
job_chain_runtime: 00:03:20
average_job_time: 00:03:20
-
start_job: 1
last_job: 3
number_of_jobs: 3
job_chain_runtime: 00:01:45
average_job_time: 00:00:35
-
```

* 每条链一段，段前段后都有 `-`。
* 时长格式 `hh:mm:ss`，小时至少两位、不截断（`100:00:00`）。
* `average_job_time` = 总时长 / job 数，整秒**截断**（例：35 s / 2 = 17.5 → `00:00:17`）。
* 链按 `job_chain_runtime` **降序**；相同时按 `start_job` 升序。

## Part

| Part | 签名（`JobChains`） | 内容 |
|---|---|---|
| 1 | `List<Job> parse(List<String>)` · `String hhmmss(long)` | 解析 + 单行校验；格式化 |
| 2 | `List<Chain> chains(List<Job>)` | 拼链 + 跨行校验 + 排序 |
| 3 | `Outcome analyze(List<String>)` · `List<String> render(Outcome)` · `Main` | 整题，stdin → stdout |

`Job`、`Chain`、`Outcome`（sealed：`Ok` / `Malformed`）在 starter 里已给出。

## 非法输入（全部 → 只输出 `Malformed Input`，原文要求 **exit zero**）

| 类别 | 例子 |
|---|---|
| 字段数不是 3 / 不是整数 / 分隔符不对 | `1,2` · `a,2,3` · `1;2;3` |
| 取值越界 | `0,5,0` · `3,-5,0` · `99999999999,1,0` |
| 自环 | `4,1,4` |
| 重复 `job_id` | 两行都是 `1,…` |
| 悬空 `next_job_id` | 指向不存在的 job |
| 多前驱（两个 job 指向同一个） | `1,10,3` + `2,10,3` |
| 环（含「好链 + 独立环」） | `2,10,3` + `3,10,2` |

## 考什么

不是算法（O(n) 哈希即可），而是**把模糊题面变成完整的校验清单**、精确输出格式、以及不信任输入。公开用例只有 2 个，隐藏用例几乎全打边界。
