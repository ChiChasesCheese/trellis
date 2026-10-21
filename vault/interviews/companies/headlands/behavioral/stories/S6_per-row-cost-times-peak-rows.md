# S6 · 逐行方案撑不住：上线前用规模估算叫停（性能 · 容量推理 · 独立判断）

用于：a performance problem / a time you said no / how do you estimate / inherited project。
**先说边界**：这是**上线前的容量推理，不是对运行中系统的剖析**。

**Hook：「Before writing serving code, I ask what the per-row cost times the peak row count is.」**

## 数字

- QA：6 个合成商户，不到 10 亿行；生产：约 18,000 商户，峰值一天最多约 7.6 亿行。
- Phase 2（重训 + 推理重构）两三个月。
- 示例（假设值，必须说明是示例）：每行 10 µs → 7.6 亿行约 2.1 小时；每行 1 µs 也要约 12.7 分钟。

## 60 秒

> 先说：**this was capacity reasoning before anything shipped, not profiling a running system.**

**S**
- A departing intern left an **ML fee-anomaly detector** that had **only run in QA**: **6 synthetic merchants**.
- Production: ~**18,000 merchants**, up to **760M rows** on a peak day.

**T**
- Decide **continue or stop**, and how long production would take.

**A**
1. The serving design was a **per-row numpy forward pass**.
2. **Arithmetic**: per-row cost × peak rows; it would **time out** on a big warehouse.
3. QA could **never show** it: the data was too small.
4. Split **what leaves with the intern** from **what's rebuildable**; only the **analyst labels** were irreplaceable, so I **exported them first**.
5. **Phase 1**: only the deterministic rule `|amount| = rate × qty + fixed`, as **set-based SQL** in the warehouse.
6. **Phase 2**: retrain and redesign inference **behind a go/no-go gate**; I **froze** alerting and CI/CD until then.

**R**
- A launch that could have **paged the team at night** became a **reviewable, phased plan**.

**L**
- Ask **per-row cost × peak rows** before writing the serving path; do **set-based** work **where the data lives**.

## 2 分钟（在 60 秒上加）

- Wrote a **State / Handoff / Prod-Cutover** assessment so the state was on paper.
- **Alert volume**: a 99.5% threshold on hundreds of millions of rows a day gives **millions of alerts**; precision was **unknown** (no ground truth, only shadow mode).
- **If it had been live**: measure **per-row latency at small N**, separate **CPU from data movement**, extrapolate.

## 追问

- **Did you profile it?** **No**; it had never run at scale. I'd measure per-row latency, then CPU vs data transfer, then check batching.
- **Why is per-row numpy slow here?** Per-row **call overhead** and **data movement** out of the warehouse; a set-based query does **one scan** in place.
- **Why couldn't QA show it?** Six merchants hid the **constant per-row cost**.
- **Is pushdown always faster?** Only if the logic is **expressible set-wise** and the data is already there; a neural forward pass isn't, hence Phase 2.
- **How decide Phase 2 is worth it?** A **business driver** plus **measured precision** in shadow mode.

## 别说

- "I profiled it" / "I sped it up N×"。
- 把 10 µs 当事实。点名实习生。

## 待 Chi 补

- Phase 1 是否上线、真实耗时；一个真实剖析故事（`templates.md` T2）。
