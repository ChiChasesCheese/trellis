---
id: cc-verification-determinism-repeatable-runs
node: verification.determinism
type: qa
---
## Q
The same input produces different output on two runs of your program. Name the usual suspects and the rule that eliminates all of them.

## A
**Anything that reads the world instead of the input.**

- `set` iteration and `hash()` ([[cc-verification-determinism-stable-hash]]).
- `time.time()`, `datetime.now()`, `uuid4()`, `id()`, `os.environ` — a "today" default is the classic, and it makes the test pass this afternoon and fail after midnight.
- Unseeded `random` ([[cc-verification-determinism-seeded-random]]).
- Any concurrency, and any ordering derived from a set.

**Rule: the output must be a pure function of the bytes on stdin.** If the logic needs a clock, take it from the input, or make it a parameter with a fixed default that a test can override.

## Q zh
同一个输入，你的程序两次运行给出不同输出。说出常见嫌疑人，以及能一次性消灭它们的规则。

## A zh
**任何读取「外部世界」而不是读取输入的东西。**

- `set` 的遍历和 `hash()`（[[cc-verification-determinism-stable-hash]]）。
- `time.time()`、`datetime.now()`、`uuid4()`、`id()`、`os.environ` —— 以「今天」为默认值是经典款，它让测试今天下午通过、过了午夜失败。
- 没有种子的 `random`（[[cc-verification-determinism-seeded-random]]）。
- 任何并发，以及任何从 set 派生出来的顺序。

**规则：输出必须是 stdin 上那串字节的纯函数。** 逻辑需要时钟时，就从输入里取，或者把它做成带固定默认值、可被测试覆盖的参数。
