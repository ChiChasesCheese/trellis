---
id: cc-algorithms-recognition-constraint-sizes
node: algorithms.recognition
type: cloze
---
The constraints name the allowed complexity before you write a line. n ≤ {{c1::20}} admits exponential work — subsets, bitmask DP, permutations with pruning. n ≤ 10^3 admits {{c2::O(n²)}}, so a double loop is fine. n ≤ 10^5 means {{c3::O(n log n)}} — sort, heap, bisect — and rules out any nested scan. n ≤ 10^6 means {{c4::a single O(n) pass}} with O(1) work per element, because an interpreted language manages roughly {{c5::10^7}} simple operations per second inside a two-second budget.

## zh
约束在你写下第一行之前就已经点名了允许的复杂度。n ≤ {{c1::20}} 容得下指数级做法 —— 子集、bitmask DP、带剪枝的排列。n ≤ 10^3 容得下 {{c2::O(n²)}}，所以双重循环没问题。n ≤ 10^5 意味着 {{c3::O(n log n)}} —— 排序、堆、bisect —— 并且排除任何嵌套扫描。n ≤ 10^6 意味着 {{c4::单趟 O(n)}} 且每个元素 O(1) 的工作量，因为解释型语言在两秒预算内大约只能做 {{c5::10^7}} 次简单操作。
