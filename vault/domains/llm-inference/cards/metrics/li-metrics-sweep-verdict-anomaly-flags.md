---
id: li-metrics-sweep-verdict-anomaly-flags
node: metrics.sweep-verdict
type: qa
step: 3
---
## Q
推理服务的性能扫描表在交给客户之前，要自动标出哪些异常？吞吐随并发下降、负载升高 TTFT 反而变小、每用户速度 × 并发对不上总吞吐，各说明什么？写出检查代码。

## A
**先说词：** 大模型按 token（文字的小片段）逐个生成；并发是同时在服务里的请求数；TTFT 是看到第一个字的等待时间；每用户 tok/s 是一个人看到的出字速度；总 tok/s 是整台服务每秒产出的 token 数。

**物理上应当成立的规律：** 并发升高时，总吞吐先升后平，TTFT 只升不降，每用户速度只降不升。违反它们的行，要么是数据有问题，要么是系统有值得解释的行为。

```python
def anomalies(rows, tol=0.05):
    # rows: 同一模型、同一画像，按并发升序；字段 conc, ttft_ms, user_tps, total_tps
    flags = []
    for a, b in zip(rows, rows[1:]):
        if b["conc"] == a["conc"]:
            flags.append((b["conc"], "重复的并发点"))
        if b["total_tps"] < a["total_tps"] * (1 - tol):
            flags.append((b["conc"], "总吞吐随并发下降"))
        if b["ttft_ms"] < a["ttft_ms"] * (1 - tol):
            flags.append((b["conc"], "负载升高 TTFT 反而变小"))
    for r in rows:
        ideal = r["user_tps"] * r["conc"]          # 每人速度 × 人数 = 总吞吐上限
        if r["total_tps"] > ideal * (1 + tol):
            flags.append((r["conc"], "总吞吐超过上限，口径可疑"))
        elif r["total_tps"] < ideal * 0.5:
            flags.append((r["conc"], "总吞吐不到上限一半"))
    return flags
```

**每条异常的常见原因：**
- **总吞吐随并发下降：** 显存放不下所有请求的中间状态（KV 缓存：为每个已处理 token 保存的中间结果），服务把请求挤出去再重算，这是真实行为；也可能是某次运行被别的任务干扰。标出来让工程师确认，不自动删。
- **TTFT 随负载变小：** 几乎一定是数据问题：第一个点在冷启动时测的（没预热）；高并发档的输入恰好命中了前缀缓存；行顺序或列被弄错。
- **总吞吐超过每用户 × 并发：** 物理上不可能。最常见是"总吞吐"把输入 token 也算进去了，或单位一个是每秒一个是每分钟。要先问清口径。
- **总吞吐不到上限一半：** 每用户速度如果只按生成阶段算（不含等首字的时间），总吞吐本来就略低；低一半说明请求之间有大量空闲，可能是压测客户端没打满并发。
- **缺点和重复点：** 某个并发档没有数据或测了两遍，曲线会画出假拐点。

**容差 5% 的理由：** 单次性能测量本身有几个百分点的抖动，太紧会满屏误报。
