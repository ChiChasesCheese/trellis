---
id: hl-oa01-what-asked
node: problems.oa01-job-chain
type: qa
step: 1
---
## Q
任务链报表（Job Chain）题：输入是 CSV 日志，要求输出什么？给一个小例子。

## A
调度系统里的 job 首尾相接：job 跑完触发 `next_job_id`，`0` 表示链尾。每行 `job_id,runtime_in_seconds,next_job_id`，第一行表头以 `#` 开头，空行忽略，逗号两侧可有空格。

任务：找出每条链（chain），输出起始 job（`start_job`）、结束 job（`last_job`）、job 数、总时长、平均时长，段前后各一行 `-`。输入只要有一点不对，**只输出 `Malformed Input`**，并且进程退出码为 0。

例：`1,60,23` / `23,30,3` / `3,15,0` / `5,200,0` 得到两条链：1→23→3（3 个 job，105 s = `00:01:45`，平均 35 s = `00:00:35`）和 5（`00:03:20`）。链按总时长**降序**，相同时按 `start_job` 升序，所以链 5 在前。

这题不考算法（哈希表 O(n) 即可），考的是把模糊题面变成完整的校验清单、精确的输出格式、不信任输入。
