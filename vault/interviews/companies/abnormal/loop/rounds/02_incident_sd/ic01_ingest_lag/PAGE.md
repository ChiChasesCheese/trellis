# PAGE · ic01

```
[ALARM] alert-ingest-consumer-lag-high  (us-east-1, account 111122223333)
Metric: AWS/Kafka SumOffsetLag  ConsumerGroup=alert-ingest Topic=security-events   Statistic: Maximum
Threshold: > 50000 for 10 datapoints within 10 minutes (period 60 s)
State changed OK -> ALARM at 2026-09-30T14:19:00Z
```

It is 14:30 UTC. You have console access to this account; walk us through it.

---

工具：在本目录运行 `python3 awsim.py --help`（离线快照，命令形状模仿 AWS CLI；`--table` 输出紧凑文本，`--start/--end` 可写 `HH:MM`）。
先别看 `investigation.md` 和 `model_answer.md`。计时 30 分钟：前 2 分钟只说话（问什么、先看什么），之后每用一条命令先说出你要验证的假设。
