---
id: cc-performance-memory-input-is-resident
node: performance.memory
type: qa
---
## Q
Your own structures are tiny, yet peak RSS is 140 MB on a 10^6-line input. Where did the memory go, and what do you do about it?

## A
**The input itself is resident.** `sys.stdin.read().splitlines()` on 10^6 lines of ~40 characters holds ~40 MB of text plus ~50 bytes of `str` object header each — over 100 MB before you parse anything.

- Peak RSS is measured over the whole run, so a list that exists for one second still counts against the budget.
- Fix: iterate `for line in sys.stdin:` and fold each line into state as you go; if you must read the whole input, `del lines` once parsed so it can be freed before the heavy phase.
- Measure the peak, not the steady state — the peak is exactly what a memory budget checks.

## Q zh
你自己的数据结构很小，但在 10^6 行输入上峰值 RSS 是 140 MB。内存去哪了？怎么办？

## A zh
**输入本身就常驻内存。** 对 10^6 行、每行约 40 字符做 `sys.stdin.read().splitlines()`，光文本就约 40 MB，再加每个 `str` 对象约 50 字节的头 —— 你还没开始解析就超过 100 MB。

- 峰值 RSS 是整个运行期间的最大值，所以只存在一秒的列表照样算进预算。
- 修法：用 `for line in sys.stdin:` 边读边把每行折进状态；如果必须整读，解析完就 `del lines`，让它在重活开始前被释放。
- 要测峰值，不是稳态 —— 内存预算查的正是峰值。
