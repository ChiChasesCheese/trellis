---
id: foundations-tail-latency-amplification
node: foundations.numbers
type: cloze
---
Tail latency amplification: a page fans out to 100 backend calls, each avoiding its slow path 99% of the time — the whole page avoids all slow paths with probability 0.99¹⁰⁰ ≈ {{c1::37%}}, so {{c2::~63%}} of user requests hit at least one p99-slow call. Fan-out turns a backend's {{c3::p99 into roughly the user-facing median}} — which is why high-fan-out services obsess over tails, not medians.


## zh
尾部延迟放大: 一个页面扇出到 100 个后端调用，各个避免其慢路径 99% 的时间 — 整个页面避免所有慢路径的概率 0.99¹⁰⁰ ≈ {{c1::37%}}，所以 {{c2::~63%}} 的用户请求命中至少一个 p99 慢调用。Fan-out 把后端的 {{c3::p99 变成大约用户面对的中位数}} — 这是为什么高 fan-out 服务痴迷尾部，不是中位数。
