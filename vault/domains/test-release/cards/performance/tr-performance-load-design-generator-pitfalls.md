---
id: tr-performance-load-design-generator-pitfalls
node: performance.load-design
type: qa
step: 3
---
## Q
负载测试的结果显示"服务吞吐上不去"，但问题其实出在压测客户端自己。有哪些常见的压测客户端陷阱？怎么排除？

## A
**常见陷阱**：
- **客户端 CPU 打满**：Python 写的压测脚本单进程处理成千上万个流式响应，解析每个返回片段都要 CPU，客户端自己成了瓶颈。症状：压测机 CPU 接近 100%，服务端 CPU 和加速卡利用率不高。
- **连接数上限**：HTTP 客户端的连接池默认上限很小（例如 `aiohttp` 的 `TCPConnector` 默认 `limit=100`），请求在客户端排队，服务端看到的并发远低于预期。
- **文件描述符上限**：`ulimit -n` 为 1024 时，超过约 1000 个并发连接直接失败。
- **实际发送速率低于目标**：开环测试设定每秒 20 个请求，但客户端赶不上，实际只发了 12 个；结果被误读为"服务在 20 时的表现"。
- **测量时间点错误**：从"客户端真正发出"计时，而不是从"计划发出"计时；服务卡住时客户端也跟着慢下来，少发了请求，延迟被低估（协同遗漏，coordinated omission）。
- **和被测服务同机运行**：压测客户端和服务抢 CPU 与内存带宽。

协同遗漏：开环测试按计划时间均匀发请求，服务卡住时客户端也停发：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<g font-family="sans-serif" font-size="12">
<rect x="148" y="14" width="104" height="96" fill="currentColor" fill-opacity="0.12"/>
<text x="200" y="28" text-anchor="middle" fill="currentColor">服务卡住</text>
<text x="62" y="54" text-anchor="end" fill="currentColor">计划发送</text>
<text x="62" y="94" text-anchor="end" fill="currentColor">实际发出</text>
<line x1="66" y1="50" x2="330" y2="50" stroke="currentColor" stroke-width="0.6"/>
<line x1="66" y1="90" x2="330" y2="90" stroke="currentColor" stroke-width="0.6"/>
<line x1="76" y1="42" x2="76" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="102" y1="42" x2="102" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="128" y1="42" x2="128" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="154" y1="42" x2="154" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="180" y1="42" x2="180" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="206" y1="42" x2="206" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="232" y1="42" x2="232" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="258" y1="42" x2="258" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="284" y1="42" x2="284" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="310" y1="42" x2="310" y2="58" stroke="currentColor" stroke-width="2"/>
<line x1="76" y1="82" x2="76" y2="98" stroke="currentColor" stroke-width="2"/>
<line x1="102" y1="82" x2="102" y2="98" stroke="currentColor" stroke-width="2"/>
<line x1="128" y1="82" x2="128" y2="98" stroke="currentColor" stroke-width="2"/>
<line x1="258" y1="82" x2="258" y2="98" stroke="currentColor" stroke-width="2"/>
<line x1="284" y1="82" x2="284" y2="98" stroke="currentColor" stroke-width="2"/>
<line x1="310" y1="82" x2="310" y2="98" stroke="currentColor" stroke-width="2"/>
<text x="200" y="130" text-anchor="middle" fill="currentColor">卡住期间少发了 4 个请求</text>
<text x="200" y="150" text-anchor="middle" fill="currentColor">按实际发出计时：延迟被低估</text>
<text x="200" y="170" text-anchor="middle" fill="currentColor">按计划时间计时：等待都算进延迟</text>
</g>
</svg>
```

**排除方法**：
- **核对实际速率**：压测输出中的实际请求速率、实际并发，与设定值对比；`vllm bench serve` 的输出会给出实际的请求吞吐。
- **监控压测机**：CPU、网络、连接数，确认它不是瓶颈。
- **分开部署**：压测客户端放在另一台机器上，网络延迟要远小于被测延迟。
- **做一次空载校准**：对一个立即返回的假服务压测，确认客户端本身能达到的最大速率远高于测试需要的速率。
- **按计划时间计算延迟**：开环测试里，延迟从计划发送时间算起。
