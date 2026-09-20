---
id: problems-url-shortener-counter-vs-hash
node: problems.foundations.url-shortener
type: qa
step: 3
tags: [grown]
---
## Q
In a URL shortener design, why is a pre-generated counter-based key pool (a Key Generation Service, or KGS) preferred over hashing the long URL (e.g., MD5) and truncating to 7 Base62 characters for short-code generation?

## A
Truncating a hash to 7 Base62 characters gives a keyspace of about 3.52×10^12 codes; by the birthday-paradox approximation, inserting 1.825 billion codes (5 years at 1,000,000/day) into that space makes collisions certain: the expected number of colliding pairs is n²/2N ≈ 470,000 over those five years. Any single insert rarely collides — at most the fill ratio n/N ≈ 0.05% — so retries are cheap; the real cost is that every write must be a conditional insert (or read-then-write), because you cannot know in advance which one collides, and that erases the hash approach's supposed statelessness advantage. A counter-based KGS instead hands out pre-generated, guaranteed-unique codes in batches (e.g., 1,000 per writer instance), so there is zero collision by construction, and each instance only contacts the coordination service roughly once per exhausted batch — at 35 peak write QPS that's under 0.04 coordinator calls per second per instance.

## Q zh
在一个短链接设计中，为什么用预生成的计数器键池（短码生成服务，Key Generation Service / KGS）而不是对长 URL 做哈希（如 MD5）后截断成 7 位 Base62 字符来生成短码？

## A zh
把哈希截断成 7 位 Base62 字符，键空间约为 3.52×10^12 个码；按生日悖论（birthday paradox）近似估算，把 18.25 亿个码（5 年、每天 100 万条）插入这个空间，碰撞是必然的：五年内预期碰撞对数 n²/2N ≈ 47 万。单次插入很少撞上——概率至多是填充率 n/N ≈ 0.05%——所以重试很便宜；真正的代价是每次写入都必须是条件写（或先读后写），因为无法事先知道哪一次会撞，这抵消了哈希方案本应具备的无状态优势。基于计数器的 KGS 则以批次（例如每批 1,000 个）预先分配保证唯一的短码，从结构上做到零碰撞，且每个实例大约每消耗完一批才需要联系协调服务一次——在峰值写 QPS 为 35 的情况下，每实例每秒调用协调服务的次数低于 0.04 次。
