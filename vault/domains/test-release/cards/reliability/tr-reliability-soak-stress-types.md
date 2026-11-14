---
id: tr-reliability-soak-stress-types
node: reliability.soak-stress
type: qa
step: 1
---
## Q
负载测试（load test）、压力测试（stress test）、尖峰测试（spike test）和长稳测试（soak / endurance test）有什么区别？各自回答什么问题、跑多久？

## A
- **负载测试**：在预期负载（例如日常峰值 500 请求/秒）下运行，回答"在正常和高峰负载下，延迟和错误率是否达标"。通常运行几十分钟，排除预热阶段后取稳定期的数据。
- **压力测试**：负载逐步加到超过设计容量，直到系统出错或延迟失控，回答"极限在哪里、超过极限时怎么失败"。关注的是失败方式：是平稳地拒绝多余请求（返回 429），还是排队越来越长最后全部超时、甚至崩溃；负载退回后能否自己恢复。
- **尖峰测试**：负载在几秒内从低跳到很高再回落，回答"突发流量下自动扩容、限流、队列能否跟上"。
- **长稳测试**：在额定负载（例如峰值的 70–80%）下连续运行很长时间，常见 8 小时、24 小时、72 小时，回答"随着时间推移会不会变坏"。它暴露的是只有时间才能积累出来的问题：内存泄漏、文件句柄和连接耗尽、内存碎片、日志和临时文件填满磁盘、缓存无限增长、计数器溢出、性能逐渐下降。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260">
<g font-family="sans-serif" font-size="12">
<text x="10" y="20" fill="currentColor">负载测试 几十分钟</text>
<line x1="10" y1="100" x2="160" y2="100" stroke="currentColor" stroke-width="0.8"/>
<line x1="10" y1="100" x2="10" y2="28" stroke="currentColor" stroke-width="0.8"/>
<line x1="10" y1="54" x2="160" y2="54" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4 3"/>
<path d="M0,32 L140,32" transform="translate(14,28)" fill="none" stroke="currentColor" stroke-width="2.2"/>
<text x="180" y="20" fill="currentColor">压力测试</text>
<line x1="180" y1="100" x2="330" y2="100" stroke="currentColor" stroke-width="0.8"/>
<line x1="180" y1="100" x2="180" y2="28" stroke="currentColor" stroke-width="0.8"/>
<line x1="180" y1="54" x2="330" y2="54" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4 3"/>
<path d="M0,70 L30,62 L60,48 L90,30 L110,14 L125,60 L140,60" transform="translate(184,28)" fill="none" stroke="currentColor" stroke-width="2.2"/>
<text x="10" y="130" fill="currentColor">尖峰测试</text>
<line x1="10" y1="210" x2="160" y2="210" stroke="currentColor" stroke-width="0.8"/>
<line x1="10" y1="210" x2="10" y2="138" stroke="currentColor" stroke-width="0.8"/>
<line x1="10" y1="164" x2="160" y2="164" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4 3"/>
<path d="M0,65 L50,65 L56,12 L80,12 L86,65 L140,65" transform="translate(14,138)" fill="none" stroke="currentColor" stroke-width="2.2"/>
<text x="180" y="130" fill="currentColor">长稳测试 8–72 小时</text>
<line x1="180" y1="210" x2="330" y2="210" stroke="currentColor" stroke-width="0.8"/>
<line x1="180" y1="210" x2="180" y2="138" stroke="currentColor" stroke-width="0.8"/>
<line x1="180" y1="164" x2="330" y2="164" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4 3"/>
<path d="M0,46 L140,46" transform="translate(184,138)" fill="none" stroke="currentColor" stroke-width="2.2"/>
<text x="170" y="250" text-anchor="middle" fill="currentColor">横轴时间，纵轴负载，虚线为设计容量</text>
</g>
</svg>
```

**一个容易混淆的点**：长稳测试的负载不需要很高。它的目标是**时间维度上的积累**，负载太高反而会把问题变成压力测试的问题，难以分辨是"过载"还是"泄漏"。

**放在哪一档**：负载测试可以每晚跑；压力和尖峰测试在大改动和发布前跑；长稳测试放在发布验证中，因为它占用设备时间最长。
