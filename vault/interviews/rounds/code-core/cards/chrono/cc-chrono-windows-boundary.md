---
id: cc-chrono-windows-boundary
node: chrono.windows
type: cloze
---
"At most {{c1::3}} requests in the last {{c2::60}} seconds" has to be pinned to one comparison. Reading the window as the half-open range `(t − w, t]` means an event at exactly {{c3::`t − w` is outside}} while one at `t` is inside, and the eviction loop is then {{c4::`while ev and ev[0] <= t - w: ev.popleft()`}}. The other reading, `[t − w, t]`, admits one more event and is a different answer — so write down which one you implemented.

## zh
「最近 {{c2::60}} 秒内最多 {{c1::3}} 个请求」必须固定成一个比较。把窗口读作半开区间 `(t − w, t]`，意味着恰好落在 {{c3::`t − w` 的事件在窗口外}}，而落在 `t` 的在窗口内，驱逐循环于是是 {{c4::`while ev and ev[0] <= t - w: ev.popleft()`}}。另一种读法 `[t − w, t]` 会多放进一个事件，是不同的答案 —— 所以要写明你实现的是哪一种。
