# oa01 · Job Chain 报表

调度系统里的任务首尾相接：一个任务跑完，触发它的下一个任务。日志是一份 CSV，每行是 `job_id, run_time_seconds, next_job_id`，`next_job_id` 为 0 表示链到此结束。你要为每条链输出起点、终点、任务数、总时长和平均时长；只要输入有任何不对，整个输出就只有一行 `Malformed Input`。这是一道线上编程测试（OA）的题，也可能在视频面试里被拿来追问你当时怎么做的。解题入口是函数 `solve(lines)`：输入所有行，返回要打印的行。

## 面试官会怎么说

> "You're given a CSV log of jobs: `job_id,run_time_seconds,next_job_id`, where 0 means the chain ends. For each chain print the first job, the last job, the number of jobs, the total run time and the average run time as `hh:mm:ss`. If the input is malformed, print `Malformed Input`."
> 接着会问："How do you detect a cycle?" "What if a job has two parents?" "What if the file does not fit in memory?"

## 40 分钟怎么分

| 时间 | 做什么 |
|---|---|
| 0–3 分钟 | 复述题目，问清：输出的顺序？平均值怎么取整？哪些情况算 Malformed？ |
| 3–15 分钟 | **Part 1**：合法输入，解析 + 建 next / prev 表 + 从每个链头往下走 |
| 15–30 分钟 | **Part 2**：校验，所有不合法的输入都返回 `Malformed Input` |
| 30–40 分钟 | **Part 3**：口头追问，不写代码 |

## Part 1 · 合法输入（约 12 分钟）

| 语言 | 签名 |
|---|---|
| Java | `static List<String> solve(List<String> lines)` |
| C++ | `std::vector<std::string> jobchains::solve(const std::vector<std::string>& lines)` |

输入格式：

```
#job_id,runtime_in_seconds,next_job_id
1,60,23
23,30,3
3,15,0
5,200,0
```

- 以 `#` 开头的行（表头）和空行跳过；逗号两侧可以有空格；`job_id > 0`，`run_time >= 0`，`next_job_id = 0` 表示链尾。
- 返回的每条链占 6 行，前后各有一个 `-`：`start_job`、`last_job`、`number_of_jobs`、`job_chain_runtime`、`average_job_time`。时长是 `hh:mm:ss`，小时至少两位，不截断（`100:00:00`）。平均时长是总时长除以任务数，整秒截断。
- 链的顺序：总时长从大到小；总时长相同时，起点编号小的在前。
- 上面的输入输出：先是链 5（一个任务，`00:03:20`），再是链 1 → 23 → 3（总时长 105 秒，`00:01:45`，平均 35 秒，`00:00:35`）。
- 另一个例子：`1,60,23` / `2,23,3` / `3,12,0` / `23,30,0`，得到链 1 → 23（`00:01:30`，平均 `00:00:45`）和链 2 → 3（总 35 秒，平均 17.5 截断为 `00:00:17`）。
- 输入里只有表头：输出只有一行 `-`。
- `hhmmss`（Java）/ `hhmmss`、`trim`、`split`（C++）在 starter 里已经给出。

## Part 2 · 校验（约 15 分钟）

签名同 Part 1：不合法的输入，`solve` 返回只含一行 `Malformed Input` 的列表。

| 类别 | 例子 |
|---|---|
| 字段数不是 3 / 不是整数 / 分隔符不对 | `1,2` · `1,2,3,4` · `a,2,3` · `1;2;3` · `1,,0` |
| 取值越界 | `0,5,0` · `3,-5,0` · `3,5,-1` · `99999999999,1,0`（放不进 int） |
| 指向自己 | `4,1,4` |
| 重复的 `job_id` | 两行都以 `1,` 开头 |
| `next_job_id` 指向不存在的任务 | `1,10,7` |
| 一个任务有两个前驱 | `1,10,3` + `2,10,3` + `3,10,0` |
| 环（包括「一条好链加一个独立的环」） | `1,10,0` + `2,10,3` + `3,10,2` |

- 只要有一行不对，整个输出就是 `Malformed Input`，不能输出其它链。
- 行尾带 `\r`（Windows 换行）要当作合法输入处理。

## Part 3 · 口头追问（不写代码，答案在 solution.md）

1. 为什么「走完所有链头之后，还有任务没被走到」就一定说明有环？
2. 复杂度是多少？输出前的排序占多少？
3. 一条链有一百万个任务，递归地走链会怎样？
4. 文件大到内存放不下，怎么办？能边读边输出吗？
5. 一条链的总时长加起来超出 `long` 的范围怎么办？
6. 任务编号很稀疏、很大，用数组代替哈希表可以吗？

## 边界

- 只有表头；只有空行；单个任务（`5,200,0`）。
- 输入的行顺序不重要，链头不一定在最前面。
- 平均值取整：35 秒 / 2 个任务 = `00:00:17`。
- 总时长超过 99 小时：`100:00:00`。
- 两个任务指向同一个 next；任务指向自己；两个任务互相指向。

## 怎么跑

在 kit 根目录（`interviews/companies/headlands/`）下：

```bash
python3 tools/jtest.py start   loop/rounds/00_oa/oa01_job_chain       # Java：starter/ → work/
python3 tools/jtest.py run     loop/rounds/00_oa/oa01_job_chain --tag part1
python3 tools/cpptest.py start loop/rounds/00_oa/oa01_job_chain       # C++：cpp/starter.hpp → cpp/work.hpp
python3 tools/cpptest.py run   loop/rounds/00_oa/oa01_job_chain --tag part1
```
