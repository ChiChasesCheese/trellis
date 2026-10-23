---
id: hl-c13-relaxed-wrong
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 8
---
## Q
生产者先写 `data`，再 `ready.store(true, relaxed)`；消费者 `while(!ready.load(relaxed)); use(data)`。哪里错了？`atomic<int> a; a = a + 1;` 是原子递增吗？

## A
- `relaxed` **不建立 happens-before**：消费者可能看到 `ready == true` 却读到旧的 `data`。应 `release` 写、`acquire` 读。
- `a = a + 1` **不是**原子递增：先 `load` 再 `store`，两步之间别的线程可以插入；用 `fetch_add`、`a++` 或 `a += 1`。
- 同类错误：对 `atomic` 做「先读再写」两步（`if (a == 0) a = 1;`），要用 CAS。
