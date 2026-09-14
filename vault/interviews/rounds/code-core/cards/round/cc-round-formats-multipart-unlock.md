---
id: cc-round-formats-multipart-unlock
node: round.formats
type: qa
---
## Q
The assessment is one bespoke problem in five parts that unlock in sequence, each part extending the same program, and no score is ever shown. What does that scoring model tell you to do differently from a set of independent LeetCode problems?

## A
**Partial credit accumulates across parts, so an earlier part locked in is money in the bank — and a Part 4 change can break Part 2's tests.**

- Read every part before choosing the data structure; the last part decides the shape.
- Re-run every earlier sample after finishing each new part.
- Never trade a passing part for a speculative one: finish, verify, unlock the next.
- Independent problems let you abandon one cleanly; here, abandoning the middle costs you everything above it. See [[cc-round-time-lock-before-next]].

## Q zh
笔试是一道定制题，分成依次解锁的五个部分，每部分都在扩展同一个程序，而且从不显示分数。相比一组互相独立的 LeetCode 题，这种评分方式要求你做什么不同的事？

## A zh
**部分分是跨 part 累加的，所以锁死的前面部分就是存进银行的钱 —— 而 Part 4 的一次改动可能弄坏 Part 2 的测试。**

- 选数据结构之前先读完所有部分；形状由最后一部分决定。
- 每做完一个新部分，重跑之前所有的样例。
- 绝不用一个已经通过的部分去赌一个没把握的部分：做完、验证、再解锁下一个。
- 独立题目可以干净地放弃一道；这里放弃中间一部分，等于把它上面的全丢了。见 [[cc-round-time-lock-before-next]]。
