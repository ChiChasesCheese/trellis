---
id: cc-toolbox-heap-heapify
node: toolbox.heap
type: qa
---
## Q
You have 10^5 initial items to put in a heap. `heapify` or a loop of pushes? And is a sorted list already a heap?

## A
**`heapq.heapify(lst)` is O(n) in place; n pushes are O(n log n).** For a one-time build, always heapify.

- Any list already in ascending order satisfies the heap invariant, so `[(0, i) for i in range(n)]` needs no work at all — that is why a "all servers start at load 0" heap costs nothing to construct.
- `heapify` **mutates** the list; afterwards the list *is* the heap, and touching it by index (`lst[3] = ...`, `lst.sort()`, `lst.append`) breaks the invariant. Only `heappush` / `heappop` may modify it.
- `heappushpop(h, x)` (push then pop) and `heapreplace(h, x)` (pop then push) each do one sift instead of two — the inner loop of size-k selection ([[cc-toolbox-heap-topk]]).
- `heap[0]` peeks at the minimum without popping, which is what a lazy-expiry drain loop wants ([[cc-toolbox-cache-expiry-index]]).

## Q zh
你有 10^5 个初始元素要放进堆。用 `heapify` 还是循环 push？有序列表本身算不算堆？

## A zh
**`heapq.heapify(lst)` 原地 O(n)；n 次 push 是 O(n log n)。** 一次性建堆永远用 heapify。

- 任何已按升序排列的列表都满足堆性质，所以 `[(0, i) for i in range(n)]` 完全不需要处理 —— 这就是「所有服务器初始负载为 0」的堆构造起来零成本的原因。
- `heapify` 会**原地修改**列表；之后这个列表*就是*堆，按下标改动它（`lst[3] = ...`、`lst.sort()`、`lst.append`）会破坏不变式。只有 `heappush` / `heappop` 可以修改它。
- `heappushpop(h, x)`（先 push 后 pop）和 `heapreplace(h, x)`（先 pop 后 push）各只做一次筛选而不是两次 —— 这是 size-k 选取的内层循环（[[cc-toolbox-heap-topk]]）。
- `heap[0]` 在不 pop 的情况下查看最小值，这正是惰性过期清理循环所需要的（[[cc-toolbox-cache-expiry-index]]）。
