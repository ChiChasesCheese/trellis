---
id: bagu-retry-2-backoff-jitter
node: a.protect.retry
type: qa
step: 2
---
## Q
**重试 · 指数退避和抖动解决什么问题**｜必会

面试官：「重试间隔你是固定 1 秒，还是别的？很多客户端同时失败时会发生什么？」

## A
**基本回答。** 指数退避加抖动：第 n 次重试前等 `random(0, min(cap, base × 2^n))`，base=100ms 时前三次上限 200、400、800ms。退避给下游恢复时间；抖动把同时失败的客户端错开，否则每一轮都是同步的重试浪潮，下游刚恢复又被打趴（完全抖动是在 0 到上限间随机取）。固定间隔只适合恢复时间稳定可预测的场景，否则形成周期性尖峰、下游没有恢复时间。参数：base 100ms 到 1s、倍数 2、cap 10 到 30 秒、次数 3 到 5 次。总耗时要算进去：读超时 1.5s、重试 3 次、等 1+2+4 秒，最坏 1.5×4+1+2+4=13s，在线请求受不了，所以次数要少并受总截止时间约束。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">指数退避：base = 100ms，等待上限每次翻倍</text>
<text x="8" y="41" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 1 次</text>
<rect x="60" y="24" width="60" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">≤ 200ms</text>
<text x="8" y="71" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 2 次</text>
<rect x="60" y="54" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">≤ 400ms</text>
<text x="8" y="101" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">第 3 次</text>
<rect x="60" y="84" width="240" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">≤ 800ms</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10 个客户端同时失败，什么时候重试？</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">无抖动</text>
<rect x="112" y="138" width="16" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="172" y="138" width="16" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<rect x="292" y="138" width="16" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">有抖动</text>
<line x1="74" y1="184" x2="74" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="92" y1="184" x2="92" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="126" y1="184" x2="126" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="150" y1="184" x2="150" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="171" y1="184" x2="171" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="200" y1="184" x2="200" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="232" y1="184" x2="232" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="262" y1="184" x2="262" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="290" y1="184" x2="290" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="314" y1="184" x2="314" y2="210" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="60" y1="218" x2="330" y2="218" stroke-width="1.2" stroke="currentColor"/>
<text x="120" y="236" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1s</text>
<text x="180" y="236" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2s</text>
<text x="300" y="236" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4s</text>
<text x="8" y="256" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同时重试 = 又一次冲击；抖动把它们摊开</text>
</svg>
三根横条是退避上限翻倍；下面对比 10 个客户端：无抖动总在同一时刻重试，有抖动摊在时间轴上。
**代码。**
```python
import random

def backoff(attempt, base=0.1, cap=10.0):
    # 完全抖动：在 [0, min(cap, base * 2^attempt)] 里随机等待
    return random.uniform(0, min(cap, base * 2 ** attempt))
```
**业务场景。** 零点一批定时任务同时调某下游并失败，无抖动时在整 1、2、4 秒齐刷刷重试，下游一直起不来；有抖动后第 1 次摊在 0~200ms，第 2 次 0~400ms，压力越来越稀；第 7 次 base × 2^7 = 12800ms 超过 cap，只取 10000ms。
**容易错。**
- **只加退避不加抖动。**
- **没有 cap。**
- **忘了总耗时。**
