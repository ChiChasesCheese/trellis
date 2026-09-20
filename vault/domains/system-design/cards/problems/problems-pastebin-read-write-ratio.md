---
id: problems-pastebin-read-write-ratio
node: problems.foundations.pastebin
type: cloze
step: 1
tags: [grown]
---
In a pastebin design ingesting 2,000,000 new pastes/day, if each paste is read an average of 5 times over its lifetime with most reads landing within the first day, the resulting read-to-write ratio is about {{c1::5:1}} — structurally far lower than a URL shortener's typical {{c2::100:1}}, because a paste link is normally shared with a known small audience rather than embedded broadly and clicked by strangers, so {{c3::caching strategy carries far less of the design's weight here than in a URL shortener, and storage layering/expiry carry far more}}.

## zh
在一个每天新增 200 万条粘贴的 pastebin 设计中，如果每条粘贴一生平均被读取 5 次、且大多数读取发生在创建后第一天内，得到的读写比约为 {{c1::5:1}}——比 URL 短链接典型的 {{c2::100:1}} 低得多，因为粘贴链接通常发给一个已知的小群体，而不是被广泛嵌入、被陌生人反复点击；这意味着 {{c3::缓存策略在这道题里承担的权重远不如 URL 短链接，存储分层和过期回收承担的权重要大得多}}。
