---
id: tr-performance-load-design-sweep-goodput
node: performance.load-design
type: qa
step: 2
---
## Q
负载测试怎么找到系统的容量拐点？"满足延迟目标的吞吐"（goodput）是什么，为什么比单纯的吞吐更有意义？

## A
**阶梯扫描（step sweep）**：
1. 从低负载开始，例如每秒 1 个请求，逐级加到预计容量的 1.5 倍以上，例如 1、2、4、8、12、16、20；
2. 每一级保持足够长时间（例如 5–10 分钟），丢弃开头的预热和过渡期，只用稳定期的数据；
3. 每级记录吞吐、p50 和 p99 延迟、错误率、排队长度；
4. 画"负载 – 延迟"曲线：低负载时延迟基本平坦，接近容量时 p99 开始快速上升，超过容量后排队无限增长、延迟发散。**拐点**就是 p99 开始陡升的位置。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 225">
<g font-family="sans-serif" font-size="12">
<line x1="50" y1="190" x2="320" y2="190" stroke="currentColor"/>
<line x1="50" y1="190" x2="50" y2="15" stroke="currentColor"/>
<line x1="50" y1="110" x2="315" y2="110" stroke="currentColor" stroke-dasharray="5 4"/>
<path d="M50,165 L150,162 C200,158 225,145 240,120 C255,95 262,60 270,20" fill="none" stroke="currentColor" stroke-width="2.5"/>
<circle cx="232" cy="133" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
<text x="180" y="214" text-anchor="middle" fill="currentColor">负载（请求/秒，逐级加压）</text>
<text x="22" y="105" text-anchor="middle" fill="currentColor" transform="rotate(-90 22 105)">p99 延迟</text>
<text x="60" y="152" fill="currentColor">平坦</text>
<text x="160" y="140" text-anchor="end" fill="currentColor">拐点：开始陡升</text>
<line x1="164" y1="136" x2="226" y2="134" stroke="currentColor" stroke-width="0.8"/>
<text x="276" y="40" fill="currentColor">发散</text>
<text x="60" y="104" fill="currentColor">延迟目标</text>
<text x="280" y="128" fill="currentColor">超标</text>
</g>
</svg>
```

`vllm bench serve` 也支持在一次运行中逐步加压：`--ramp-up-strategy linear --ramp-up-start-rps 1 --ramp-up-end-rps 20`；但分级运行、每级单独统计更容易分析。

**goodput**：只计算**满足延迟目标的请求**的吞吐。以文字生成服务为例，它把文字切成叫 token 的小单位（约一个词）逐个输出；目标可以是首 token 等待 ≤ 500 毫秒、之后每个 token ≤ 50 毫秒，那么一秒内完成了 10 个请求、但只有 6 个满足目标，goodput 就是 6 个/秒。`vllm bench serve` 用 `--goodput ttft:500 tpot:50` 指定这些目标（单位毫秒）。

**为什么更有意义**：
- 单纯的吞吐在过载时仍可能很高：服务一直在忙，但每个用户都等很久。吞吐最高的那一点，往往用户体验已经不可接受。
- goodput 把"能服务多少用户"和"服务得好不好"合成一个数，容量规划可以直接用：goodput 的峰值所在的负载，就是这个配置在给定目标下的可用容量。

**常见错误**：只测一个负载点就报告"吞吐 X"；或者只看平均延迟，拐点附近平均值还很好看，p99 已经超标。
