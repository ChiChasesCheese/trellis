# ic01_ingest_lag · REPORT

告警 "alert-ingest consumer lag > 50k for 10 min"。根因（reconstructed）：14:02 部署 `alert-ingest:57`（"simplify geoip client"）改成每条消息同步调用 `geoip-svc`、零退避重试；`geoip-svc` 的 per-client 限额 1,200 rpm 把成功查询钉在 20/s，消费从 ~160/s 跌到 ~22/s，lag 每分钟 +~7,800；14:30 时 lag 209,844、最老未消费消息 1,380 s、DLQ 3,232。

## 快照规模（`env/`，`python3 build_env.py` 确定性生成，重建与仓库内容逐字节相同）

| 项 | 数 |
|---|---|
| 文件 / 字节 | 56 / 1,378,140 |
| 时间窗 | 2026-09-30T12:30:00Z → 14:30:00Z（121 分钟，每分钟一个数据点） |
| 指标 | 7 个命名空间、21 个指标文件、3,267 个数据点 |
| 日志 | 4 个 log group、21 个 stream、4,255 行 |
| CloudTrail / 部署 / 告警 | 8 / 5 / 5 |
| 配置（before/after）/ 资源描述 | 4 / 6（ecs×3、msk、rds、sqs） |

## 红鲱鱼

1. `report-renderer-cpu-high`（14:07 ALARM）：另一个集群 `prod-batch` 的另一个部署（13:58:41），alert-ingest 的 CPU 反而从 ~38% 降到 ~8%。
2. MSK broker-2 磁盘告警：12:55 ALARM → 13:01 OK（`UpdateBrokerStorage` 1000→1500 GiB），期间 lag < 300。
3. RDS `alerts-prod`：CPU < 25%，WriteIOPS 从 ~1,800 降到 ~490（被饿，不是瓶颈）。
4. `geoip-svc` 本身：5xx = 0、服务端 p99 ~41 ms、另一个 client `risk-engine` 未被限流、最近部署在 09-17——它在按配置限流，问题在调用方。
5. 告警空白（要指出的缺口）：`geoip-svc-5xx-high` 一直 OK，因为 429 不是 5xx。

## awsim 支持的查询（730 行，标准库）

`now` · `alarms [--state] [--name] [--history]` · `metrics list|get`（Average/Sum/Maximum/Minimum/SampleCount/pNN，`--period`，`--dim`）· `logs groups|tail|filter` · `logs insights`（fields / filter：比较、`like` 子串与正则、`not like`、and/or/not、括号 / `stats count() count(f) sum avg min max pct(f,N) count_distinct … by 字段, bin(Nm)` / sort / limit）· `trail lookup` · `deploys` · `describe` · `config list|show|diff`。全部支持 `--start/--end`（ISO 或 `HH:MM`）与 `--table`。错误以 AWS CLI 风格写 stderr、退出码 254。

## 测试（`… pytest tests -q -o addopts= -p no:cacheprovider` → `74 passed`）

| 文件 | `def test` | 收集数 | 内容 |
|---|---|---|---|
| `test_ic01_awsim.py` | 17 | 17 | 查询子集在手写小快照上的正确性 |
| `test_ic01_story.py` | 20 | 20 | 时间戳全部 UTC ISO 8601；根因证据存在（部署、config diff、lag 线性、成功数 = 限额、DLQ、日志与指标对账）；红鲱鱼确实无害 |
| `test_ic01_model_answer.py` | 3 | 37 | `model_answer.md` 的 35 个证据块（83 行输出）逐条重跑比对；`investigation.md` 的全部命令能运行 |

## 已知弱点

回滚后追平速度（"old version ~300 msg/s per task"）是模型常数，快照里只有 ~3 ms 的 enrich 延迟支持它。
