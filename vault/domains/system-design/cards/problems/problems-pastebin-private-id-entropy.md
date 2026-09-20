---
id: problems-pastebin-private-id-entropy
node: problems.foundations.pastebin
type: cloze
step: 5
tags: [grown]
---
In a pastebin design, private/unlisted pastes rely on the link itself as the only access control, so their id needs enough entropy to resist brute-force scanning. Against a sustained attacker guessing {{c1::100,000 ids/second for 10 years}} (about 3.15×10^13 total attempts) trying to find any one of 50 million live private pastes, a 7-character Base62 id (the same scheme reused from a URL shortener's public short codes, ~41.7 bits) gives a near-certain hit, while a {{c2::16-character Base62 random id (~95.3 bits)}} drives that probability down to about {{c3::3.3×10^-8}} — which is why private pastes must use a different, much higher-entropy id scheme than public ones, not the same short-code generator.

## zh
在一个 pastebin 设计中，私有/不可列出粘贴把链接本身当作唯一的访问控制，因此其 id 需要足够的熵来抵御暴力扫描。面对一个持续 {{c1::以每秒 100,000 次、坚持 10 年}} 的攻击者（总尝试次数约 3.15×10¹³），试图在 5000 万条存活的私有粘贴中命中任意一条：一个 7 位 Base62 id（沿用 URL 短链接公开短码同款方案，约 41.7 bit）几乎必然被命中，而 {{c2::16 位 Base62 随机 id（约 95.3 bit）}} 能把这个概率压到约 {{c3::3.3×10^-8}}——这正是为什么私有粘贴必须使用和公开粘贴完全不同、熵高得多的 id 方案，而不能复用同一套短码生成器。
