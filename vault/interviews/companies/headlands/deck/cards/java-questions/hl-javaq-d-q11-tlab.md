---
id: hl-javaq-d-q11-tlab
node: java-questions.d-memory
type: qa
step: 3
---
## Q
描述 TLAB 里一次 `new` 的具体步骤。TLAB 满了怎么办？

## A
线程私有的 TLAB 有 `top`（已用边界）和 `end`（缓冲末尾）两个指针：
1. 检查 `top + size <= end`。
2. 是：`obj = top; top += size`——一次加法加一次比较，**无锁**。
3. 否：申请新的 TLAB，或走慢路径（可能触发 GC）。
4. 然后：内存已被清零 → 写对象头（mark word + 类指针）→ 调用构造器。

TLAB 满了就申请一块新的；**Eden 满了触发 young GC**。
