---
id: hl-cq-q10-script
node: cpp-questions.b-standards
type: qa
step: 29
---
## Q
用英文 60 秒回答：What's new in C++20 and C++23, and which of it would you use? (concepts, ranges, span, `<=>`, coroutines, `std::expected`)

## A
结构：C++20 四大件 → 日常小件 → C++23 三项 → 区分即插即用（concepts/span/bit/expected）与重投入（协程/modules），并诚实说明掌握程度。

- **C++20's big four**: **concepts**, which constrain templates and turn page-long errors into one readable line; **ranges**, lazy pipelines like filter-then-transform; **coroutines** for suspendable functions; and **modules** to replace headers.
- Everyday small features: `std::span` as a pointer-plus-length view, the **spaceship operator** to generate all comparisons, designated initializers, `consteval`, `std::jthread` that joins automatically, `<bit>` for popcount and rotates, and `std::format`.
- **C++23** gives us `std::expected` for value-or-error without exceptions, `std::print`, and deducing `this`.
- Concepts, `span`, `<bit>` and `expected` are drop-in wins; coroutines and modules are bigger commitments, and I'd be upfront about which of these I have shipped and which I know at the concept level.
