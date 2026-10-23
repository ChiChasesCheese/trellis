---
id: hl-cache-false-sharing-visibility
node: foundations.cpu-cache-locality
type: qa
step: 24
---
## Q
伪共享实验为什么选原子读改写（RMW，`incrementAndGet`）？换成 `setOpaque` 或 `volatile` 写，差别还明显吗？

## A
伪共享是否可见取决于访问类型：
- `setOpaque` / `getOpaque` 写：8 字节组与 512 字节组几乎无差别（都约 124 ms）；
- `volatile` 写：8 字节组约 270 ms、128 字节组约 65 ms，有差别但很吵；
- **原子 RMW**（`incrementAndGet`）：差别最明显，约 2200 ms 对 260 ms。

原因：RMW 每次都必须先独占缓存行，对乒乓最敏感，所以选它做实验。这也是 `LongAdder` 内部 `Cell` 要用 `@Contended` 隔开的原因：它们被原子更新。
