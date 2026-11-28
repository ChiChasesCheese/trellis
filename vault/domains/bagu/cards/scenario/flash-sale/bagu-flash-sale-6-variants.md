---
id: bagu-flash-sale-6-variants
node: a.scenario.flash-sale
type: qa
step: 6
---
## Q
**变体 · 抢红包与大量人抢少量座位**｜追问

面试官：「如果换成抢红包，或者 10 万人抢 1000 个座位，方案要怎么调整？」

## A
**基本回答。** 抢红包：金额提前拆好放进 Redis 的 List，抢时没有任何计算，只是 `LPOP` 原子取一个，所以总额不会多发；再用 Set 判重，二者放同一个 Lua 里。拆分用二倍均值法：每人金额在 1 分到「剩余金额除以剩余人数的两倍减 1」之间随机，并给后面每人至少留 1 分，最后一个拿剩下的，总额守恒。抢座位：座位有编号、有身份，「还剩 3 个」说明不了哪个被谁占，所以每个座位一个 key，`SET seat:{id} <用户> NX PX`，NX 保证只有一人设置成功，PX 设过期，到时未付自动释放。10 万抢 1000 个座位，先排队或随机抽签压到约 1000 个候选再选座；抽签比纯拼速度更公平，网速最快的人不会永远赢。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">红包：金额提前拆好放进 List</text>
<rect x="8" y="24" width="58" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="37" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红包 1</text>
<rect x="74" y="24" width="58" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="103" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红包 2</text>
<rect x="140" y="24" width="58" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红包 3</text>
<rect x="206" y="24" width="58" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红包 4</text>
<rect x="272" y="24" width="58" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="301" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">红包 5</text>
<text x="8" y="74" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">抢时 LPOP 取最左边一个</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">座位：每个座位一个 key</text>
<rect x="8" y="124" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">10 万</text>
<text x="44" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">请求</text>
<rect x="92" y="124" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="128" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排队或</text>
<text x="128" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">抽签</text>
<line x1="80" y1="144" x2="85.0" y2="144.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="92,144 85.0,147.2 85.0,140.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="176" y="124" width="72" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="212" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 1000</text>
<text x="212" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">个候选</text>
<line x1="164" y1="144" x2="169.0" y2="144.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="176,144 169.0,147.2 169.0,140.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="260" y="124" width="72" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="296" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">占座</text>
<text x="296" y="155.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SET NX PX</text>
<line x1="248" y1="144" x2="253.0" y2="144.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="260,144 253.0,147.2 253.0,140.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="194" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">占座要有超时，到点未付自动释放</text>
</svg>
上半部分是红包：信封提前写好，抢的人只负责取；下半部分是座位：先把人数压到座位数的量级，再逐个座位占位。
**举个例子。** 1000 分红包分给 4 人，一次随机结果是 300、200、150、350，总和守恒、每人至少 1 分；四个数放进 List，第 5 个人 `LPOP` 得到空，返回「手慢了」。
```python
import random
def split(total, n):              # 预先拆好 n 个红包，单位：分
    out = []
    for left in range(n, 1, -1):  # left 为剩余人数
        cap = min(total - (left - 1), total // left * 2 - 1)  # 二倍均值，给后面每人留 1 分
        x = random.randint(1, max(cap, 1))
        out.append(x)
        total -= x
    return out + [total]          # 最后一个拿剩下的，总和守恒
```
**容易错。**
- **抢的时候才现算金额：** 并发下容易超发，要预拆分。
- **10 万人直接去抢座位 key：** 请求远大于座位数，先排队或抽签削峰。
