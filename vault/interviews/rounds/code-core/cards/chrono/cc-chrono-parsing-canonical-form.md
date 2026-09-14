---
id: cc-chrono-parsing-canonical-form
node: chrono.parsing
type: qa
---
## Q
One input carries `1735689600`, another `2025-01-01T00:00:00Z`, a third `09:05`. Later parts compare, subtract and sort them together. What does the parser do?

## A
**Convert every timestamp to one canonical form at the boundary** — normally an integer count of seconds (or minutes) since a fixed epoch, or a single timezone-aware `datetime`. Mixed representations turn every later comparison into a special case.

- Pick the smallest unit the spec ever mentions: minutes for `HH:MM`, seconds for `HH:MM:SS`. Integers sort, subtract and hash with no library.
- Keep the original string only if the output must echo it back verbatim — store it beside the canonical value, never instead of it.
- Never compare timestamps as strings unless they are fixed-width zero-padded ISO: `9:05` sorts after `10:05`.

See [[cc-chrono-parsing-hhmm-minutes]].

## Q zh
一份输入里是 `1735689600`，另一份是 `2025-01-01T00:00:00Z`，第三份是 `09:05`。后面的 part 要把它们放在一起比较、相减、排序。parser 该怎么做？

## A zh
**在边界处把每个时间戳转成唯一的规范形式** —— 通常是自某个固定 epoch 起的整数秒（或分钟），或者统一的 timezone-aware `datetime`。表示形式混用会让后面每一次比较都变成特例。

- 取 spec 提到过的最小单位：`HH:MM` 用分钟，`HH:MM:SS` 用秒。整数不依赖任何库就能排序、相减、做 key。
- 只有当输出要原样回显时才保留原始字符串 —— 放在规范值旁边，而不是取而代之。
- 除非是定宽补零的 ISO，否则不要按字符串比时间戳：`9:05` 会排在 `10:05` 后面。

见 [[cc-chrono-parsing-hhmm-minutes]]。
