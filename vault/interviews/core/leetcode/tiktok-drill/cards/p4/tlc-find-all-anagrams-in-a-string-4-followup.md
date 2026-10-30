---
id: tlc-find-all-anagrams-in-a-string-4-followup
node: p4.find-all-anagrams-in-a-string
type: qa
step: 4
---
## Q
**LC 438 找到字符串中所有字母异位词**｜追问

面试官接着问：（1）只要判断 `s` 里有没有 `p` 的异位词（LC 567）？（2）`s` 是无限流，只能读一遍？（3）字符集是 Unicode，或者 `p` 有上万种字符？

## A
1. **是否存在**：同一个滑窗，第一次 `unbalanced == 0` 就 `return True`，最后返回 `False`；不用收集下标。
2. **流式输入**：窗口只依赖最近 `m` 个字符，用一个 `deque(maxlen=m)` 保存窗口内容，每读一个字符做同样的 `shift`；空间 `O(m + Σ)`，不需要保留整个 `s`。
3. **大字符集**：`Counter` 版不变，`unbalanced` 仍能 `O(1)` 判断，这是它比「每步比较两张表」好的地方（后者 `O(Σ)` 每步）。若要用数组加速，先把字符映射到编号，再用列表。

**对比** 「每个窗口排序后比较」`O(n·m log m)`、「每个窗口 `Counter` 比较」`O(n·m)`，面试里把这三档复杂度说出来，再给增量版。

**Python 提醒**：`Counter` 读不存在的键返回 `0` 但**不会**插入；而 `defaultdict(int)` 读一次就插入键，用 `len(d)` 当种数时会算错。另外 `Counter` 的 `c[k] -= 1` 减到 `0` 后键仍在，所以不能用 `len(need)` 判断「是否平衡」。
