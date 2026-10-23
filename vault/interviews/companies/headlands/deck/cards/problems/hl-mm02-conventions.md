---
id: hl-mm02-conventions
node: problems.mm02-job-runner
type: qa
step: 2
---
## Q
Job Runner 题面没写清、需要自己约定的情况有哪些？每种怎么判？

## A
| 情况 | 判定 | 理由 |
|---|---|---|
| 表头必须**逐字**是 `#job_id,runtime_in_seconds,next_job_id`（整行首尾空白可容忍） | 否则 Malformed | 「malformed in any way」 |
| 每个字段必须是纯数字 `\d+`：不带符号、空格、小数点，不能为空 | 否则 Malformed | `Integer.parseInt("+5")` 能成功，所以先用正则拦一道 |
| id、时长、next 用 `long` 存，超出范围判 Malformed | — | 题面说 integer 没说范围 |
| id = 0 | Malformed | 0 是链尾标记，用作 id 会混淆 |
| id 重复 | Malformed | 题面说 unique integer id |
| next 指向不存在的 job | Malformed | 链断了 |
| 两个 job 的 next 指向同一个 job | Malformed | 一条链是一个**序列**，不会分叉或汇合 |
| 有环（包括自己指向自己） | Malformed | 环永远到不了 0 |
| 只有表头、没有 job | 输出一行 `-` | 一天没跑任何 job 不算格式错误 |
| 总时长相同 | 按 `start_job` **升序** | 题面没说，要保证输出确定 |
| 文件末尾的空行 / CRLF 换行 | 接受 | 真实文件经常这样；但 job 之间的空行判 Malformed |
| 超过 99 小时 | 小时部分照常多写几位（`100:00:00`） | `%02d` 是最少两位，不是只保留两位 |

汇合判 Malformed 是一个约定：题面说一条链是一个 job 序列，next 是「在它之后运行的那个 job」，一次运行的 job 3 不可能同时排在两条不同的链之后；另一种读法「输出两条共享尾部的链」不太自然，不采用。

隐藏测试可能与这些约定不同，所以面试时要把这些假设说出口。
