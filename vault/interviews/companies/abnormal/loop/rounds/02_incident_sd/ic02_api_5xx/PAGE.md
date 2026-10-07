# PAGE · ic02

```
[ALARM] portal-api-5xx-rate-and-p99  (us-east-1, account 111122223333)
Expression: 100*(HTTPCode_Target_5XX_Count+HTTPCode_ELB_5XX_Count)/RequestCount > 5 AND TargetResponseTime(p99) > 3
LoadBalancer: app/portal-alb/7f3e2b1c9d4a6e05   Period 60 s, 3 of 3 datapoints
State changed OK -> ALARM at 2026-10-02T09:42:00Z
```

It is 10:05 UTC. The secondary on-call acked the page at 09:45 and hands it to you: "It got a lot better around 09:52 and then just… stayed bad. Customers say the portal is slow and some pages error." You have console access to this account; walk us through it.

---

工具：在本目录运行 `python3 awsim.py --help`（离线快照，命令形状模仿 AWS CLI；`--table` 输出紧凑文本，`--start/--end` 可写 `HH:MM`）。应用请求日志是**采样**的：每行带 `sample_rate`，估算请求数用 `stats sum(sample_rate)`，不是 `count()`。
先别看 `investigation.md` 和 `model_answer.md`。计时 30 分钟：前 2 分钟只说话（问什么、先看什么），之后每用一条命令先说出你要验证的假设。
