---
id: cc-algorithms-recognition-brute-force-first
node: algorithms.recognition
type: qa
---
## Q
Twenty-five minutes left, the elegant solution is not obvious, and n ≤ 2000. What do you write?

## A
**The brute force, immediately.** A correct O(n²) at n = 2000 is 4·10^6 operations and passes comfortably.

- Grading is per test group: a correct slow solution scores every group except the performance one, while an unfinished clever one scores nothing. Partial credit is what advances candidates.
- Write it behind the signature the fast version will use, so swapping it out later is a one-line change.
- Keep it afterwards as an **oracle**: run both on random inputs and diff. That is the cheapest correctness evidence available under time pressure.
- Only optimize what the constraints force ([[cc-algorithms-recognition-constraint-sizes]]). "It feels quadratic" is not a reason when n ≤ 10^3.

## Q zh
还剩二十五分钟，优雅解法并不明显，而且 n ≤ 2000。你写什么？

## A zh
**立刻写暴力解。** n = 2000 上正确的 O(n²) 是 4·10^6 次操作，轻松通过。

- 判分是按测试组来的：正确但慢的解能拿到除性能组外的每一组，而没写完的聪明解一分都没有。部分分正是让人晋级的东西。
- 把它写在快速版将要用的函数签名之后，这样以后替换只需改一行。
- 之后把它当作**对拍器**保留：在随机输入上跑两个版本做 diff。这是限时压力下最便宜的正确性证据。
- 只优化约束逼你优化的部分（[[cc-algorithms-recognition-constraint-sizes]]）。当 n ≤ 10^3 时，「感觉像二次」不是理由。
