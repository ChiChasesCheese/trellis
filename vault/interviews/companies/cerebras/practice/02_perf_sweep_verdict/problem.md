# 02 · 性能扫描表 → 放行结论与异常标记（low priority）

限时 45 分钟，Python。

推理服务（把训练好的模型放在服务器上，接收用户的请求、生成回答）上线前，性能工程师会做一次"扫描"：固定一个模型和一种请求形状，把同时在线的用户数从 1 调到 64，每一档记下速度。结果是一张大表。客户只关心一句话："我的负载下，这个模型够不够快？"；部署工程师则要先确认这张表本身没错。这组练习让你写一个工具：读入列名五花八门的 CSV，只靠一份"列名约定"解析，按客户的服务要求给每个（模型，流量画像）出红黄绿结论，并标出数据里不合常理的点。换一个新模型必须不改代码。

## 背景：先把几个词说清楚

| 词 | 白话 |
|---|---|
| token | 模型读写文字的最小单位，大约是四分之三个英文单词或一个汉字左右。速度都按 token 算 |
| 输入长度 / 输出长度（input / output length，也写 ISL / OSL） | 一个请求发进去多少 token、模型生成多少 token |
| 预填充（prefill）与解码（decode） | 模型先一次性读完整个输入（预填充），然后一个 token 一个 token 地往外生成（解码） |
| TTFT（time to first token） | 发出请求到看到第一个字等了多久，主要花在预填充上。输入越长、同时排队的人越多，越久 |
| TPOT（time per output token，也叫 ITL，inter-token latency） | 之后每生成一个 token 隔多久。1000 / TPOT(ms) 就是一个用户看到的生成速度 |
| 每用户速度（tok/s per user） | 一个用户每秒收到多少 token，相当于"字往外蹦得多快" |
| 总吞吐（total tok/s） | 整台机器每秒为所有用户一共生成多少 token。约等于每用户速度 × 并发 |
| 并发（concurrency，也叫 batch size、users） | 同一时刻在服务的用户数。并发越高：总吞吐上升，每用户速度下降，TTFT 变长 |
| 流量画像（traffic profile） | 一种典型的请求形状，例如"读 8000 token、写 200 token"（长文档摘要） |
| SLA（服务水平要求） | 客户的硬性要求，这里是三条：在 N 个并发下，TTFT 不超过某值，每用户速度不低于某值 |

## 数据

`data/` 下两个文件，由 `make_data.py` 生成。

```text
sweep_ab.csv（模型 A、B，画像 1–3，并发 1/4/16/64）
model,profile,input_tokens,output_tokens,concurrency,TTFT (ms),TPOT (ms),tok/s/user,total tok/s
A,1,1000,300,1,52.5,0.49,2057.1,2057.1

Model_C_profile_2.csv（没有 model、profile 列，TTFT 单位是秒，多一列 notes）
ISL,OSL,batch_size,ttft_s,ITL (ms),Tokens/s per user,Throughput,notes
8000,200,1,1.4067,2.46,407.3,407.3,projection
```

## 列名约定（唯一的输入契约）

列名先归一化：转小写，`/` 读作 `per`，再去掉所有非字母数字字符。`TTFT (ms)` → `ttftms`，`tok/s/user` → `tokpersperuser`。归一化后查同义词表：

| 字段 | 必须能认出的列名（归一化后） | 单位换算 |
|---|---|---|
| `model` | model, modelname, modelid | 可缺，缺了从文件名取 |
| `profile` | profile, trafficprofile, workload, scenario | 可缺，缺了从文件名取 |
| `input_len` | inputlen, inputtokens, isl, promptlen, prompttokens, inputlength | |
| `output_len` | outputlen, outputtokens, osl, genlen, outputlength, completiontokens | |
| `concurrency` | concurrency, batchsize, bs, users, concurrentusers, numusers | |
| `ttft_ms` | ttft, ttftms, timetofirsttoken, timetofirsttokenms；ttfts、timetofirsttokens | 后两个是秒，× 1000 |
| `tpot_ms` | tpot, tpotms, itl, itlms, intertokenlatency, intertokenlatencyms, timeperoutputtoken, timeperoutputtokenms；tpots、itls | 后两个是秒，× 1000 |
| `tps_user` | tpsuser, tokpersperuser, tokenspersperuser, tokenspersecondperuser, pertpsuser, pertokpers, usertokpers, outputtokpersperuser | |
| `tps_total` | tpstotal, totaltps, totaltokpers, totaltokenspers, throughput, systemthroughput, totalthroughput, outputthroughput | |

- 认不出的列忽略。
- 两列归一化后指向同一字段：`ValueError`。
- 7 个数值字段缺任何一个：`ValueError`，信息里写出缺的字段名和看到的列名。
- 没有 `model` 或 `profile` 列时，从文件名 `Model_<X>_profile_<N>.csv` 取；文件名也不符合：`ValueError`。

## 任务

### Part 1：解析（约 12 分钟）

- `normalize_header(h) -> str`，`map_headers(headers) -> {字段: (列名, 倍数)}`。
- `parse_sweep(path) -> (points, anomalies)`：每行一个 `Point`。某个数值格子为空或不是数字时，这一行不产出 `Point`，改产出一个 `missing_value` 异常（带并发数，读不出来就是 `None`）。
- `load_all(paths)`：合并多个文件。`curves(points)`：按（模型，画像）分组，组内按并发升序，组按键排序。

### Part 2：红黄绿（约 13 分钟）

`verdict_for(curve, sla, flagged=set()) -> Verdict`，`verdicts(points, sla, anomalies=()) -> [Verdict]`（按模型、画像排序）。

1. 取并发 **不低于** 客户要求的最小那一档；不是正好那一档时，在 `reasons` 里写出用了哪一档。
2. 没有任何一档达到客户并发：红，`concurrency_used = None`，理由写"没有这个负载的数据"。
3. TTFT 余量 = (上限 − 实测) / 上限；速度余量 = (实测 − 下限) / 下限。
4. 任何一个余量 < 0：红，并列出每一条不达标的项。
5. 都达标但较小的余量 < `amber_margin`（默认 10%）：黄，写出余量。
6. 所用那一档在 `flagged` 里（那个点有异常）：本来是绿也降为黄，理由"数据有异常，先核对"。

### Part 3：异常标记（约 12 分钟）

`find_anomalies(points, step_tol=0.02, ratio_tol=0.10) -> [Anomaly]`，每条曲线按并发顺序检查：

| 类型 | 条件 | 为什么不合理 |
|---|---|---|
| `duplicate_point` | 同一并发出现两次（后一行不参与其他检查） | 不知道该信哪一行 |
| `throughput_drop` | 总吞吐比上一档低超过 2% | 多加用户，机器总产出不该变少 |
| `ttft_drop` | TTFT 比上一档短超过 2% | 排队的人更多，第一个字不该来得更快 |
| `total_mismatch` | 每用户速度 × 并发 和总吞吐相差超过总吞吐的 10% | 两列应该互相印证 |
| `tpot_mismatch` | 1000 / TPOT 和每用户速度相差超过每用户速度的 10% | 同上 |

### Part 4：报告（约 8 分钟）

`report(paths, sla) -> str`，`main(argv)`：命令行 `solution.py 文件... --concurrency 16 --ttft-ms 1400 --tps-user 300`，打印每条曲线一行（模型、画像、颜色、所用并发、TTFT、每用户速度、理由），再列出全部异常。

## 例子

参考解在默认 SLA（16 并发、TTFT ≤ 1400 ms、每用户 ≥ 300 tok/s）下：

| 模型 | 画像 | 结论 | 原因 |
|---|---|---|---|
| A | 1、3 | 绿 | |
| A | 2 | 黄 | 16 并发那一点 TTFT 比 4 并发还短，数据可疑 |
| B | 1、3 | 绿 | |
| B | 2 | 黄 | TTFT 1327 ms，只比上限少 5% |
| C | 2 | 红 | TTFT 3007 ms，每用户 280 tok/s，两条都不达标 |

异常正好 4 个：A/2 在 16 的 `ttft_drop`，B/1 在 4 的 `missing_value`，B/3 在 64 的 `throughput_drop`，C/2 在 4 的 `total_mismatch`。

## 边界情况

- 文件名是 `Model_L_profile_7.csv`、列名全换成另一套同义词（测试里就有）：必须直接出结论。
- `ttft_s` 这类秒为单位的列。
- 单元格写着 `n/a` 或为空。
- 客户并发介于两档之间（取上面一档）、高于最大一档（红）。
- 两条曲线互不干扰：B 的 TTFT 比 A 低，不算 A 的 `ttft_drop`。
- 1% 左右的小抖动不算异常。

## 面试官会追问

| 追问 | 答题要点 |
|---|---|
| 为什么取"不低于"客户并发的那一档，而不是最近的一档？ | 取更低的并发会高估速度，对客户是乐观的错误；取更高的是保守的。用了哪一档要告诉客户 |
| 为什么不在两档之间插值？ | 曲线在饱和点附近不是直线，插值可能给出从没测过的乐观数字。可以给出插值作参考，但结论按实测点下 |
| 异常点为什么要影响结论？ | 结论建立在数据上。数据可疑时给绿，等于替性能工程师的错误背书；降为黄，并把异常写在理由里 |
| 输入是 xlsx、一个文件多张表怎么办？ | 用 openpyxl 逐张表读出表头和行，后面完全复用同一条解析路径；表名或文件名提供模型和画像 |
| 同义词表认不出某个新列名怎么办？ | 报错时列出看到的列名和缺的字段，让人加一行同义词；不要猜。同义词表放在配置里，不改代码 |
| 只看性能数字，猜哪个模型最大？ | 解码时每生成一个 token 都要把全部参数读一遍，速度主要受内存带宽限制，所以单用户速度越低，模型越大：C 最大，A 最小 |
| 猜画像的用途？ | 长输入短输出（画像 2：8000 进 200 出）是检索问答或摘要；短输入长输出（画像 3：500 进 4000 出）是生成长文或推理；中等（画像 1）是普通对话 |
| 客户视图和工程师视图要分开吗？ | 要。客户只看结论、关键数字和"用的哪一档"；工程师看整条曲线和全部异常。全部列给所有人看不叫可配置 |
| 怎么测这个工具？ | 用小表逐条测每种异常和每种颜色；用生成器埋好已知缺陷，断言恰好找出这些；加一个"新模型、新列名"的文件确认零改动 |

## 评分看什么

- 列名契约写成数据（同义词表），模型名单从数据里来，代码里没有任何写死的模型名。
- 单位换算放在契约里，不散落在业务逻辑里。
- 结论规则清楚、可解释，每个黄或红都带理由，用了哪一档并发也说出来。
- 异常检查按曲线分组，阈值有容差，不把正常抖动当异常。
- 坏输入给出能定位的错误信息，不是 `KeyError` 一行。

## 怎么跑

```bash
cd vault/interviews/companies/cerebras
uv run --project ../../../.. pytest practice/02_perf_sweep_verdict -q
IMPL=starter uv run --project ../../../.. pytest practice/02_perf_sweep_verdict -q
cd practice/02_perf_sweep_verdict && uv run --project ../../../../../.. python solution.py data/*.csv
```
