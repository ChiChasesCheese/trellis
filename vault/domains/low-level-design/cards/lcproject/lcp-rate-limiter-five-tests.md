---
id: lcp-rate-limiter-five-tests
node: lcproject.lcp-rate-limiter
type: qa
step: 9
tags: [作答]
---
## Q
时间只够你为 LLM 网关限流器写五个测试（公开测试已经覆盖按客户端与接口隔离、stats 的基本形状）。你写哪五个？每个钉住哪条规则？

## A
**评分点**
- 说出合同数字例子：窗口 10000、limit 2，t=0/3000/3500 精确得 (True,1,10000)、(True,0,7000)、(False,0,6500)
- 说出恰好满一个窗口的边界：t=window 时旧请求不再计数
- 说出被拒不留痕：被拒几次之后，恢复时刻仍由第一次放行决定
- 说出令牌桶部分补充并保留小数：0.6 个令牌被拒并返回 800，再过 800 ms 放行
- 说出屏障并发：两百线程抢五十个额度，放行数恰好 50，allowed 加 rejected 恰好 200
- 说出五个都用注入的假时钟或屏障，没有 sleep

<details class="pt"><summary>参考答案</summary>

一，窗口示例 0/3000/3500 的三个精确返回值；二，`t=window` 的边界；三，拒绝五次后恢复时刻不变；四，令牌桶 0.6 → `(False,0,800)`，再过 800 ms 放行；五，`threading.Barrier` 让两百线程抢五十个额度，断言放行恰好 50、计数之和 200。时钟注入，全程没有 `sleep`。

</details>

**知识点：** 测试并发代码（Testing Concurrency）、为测试而设计、验证输出（Verification）
