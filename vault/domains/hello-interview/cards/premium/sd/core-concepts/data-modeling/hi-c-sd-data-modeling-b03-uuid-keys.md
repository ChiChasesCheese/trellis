---
id: hi-c-sd-data-modeling-b03-uuid-keys
node: sd.core-concepts.data-modeling.beyond
type: qa
step: 3
---
## Q
**数据建模 · 主键怎么生成**｜拓展 · 加分
自增整数、随机 UUID、按时间排序的 ID（如 UUIDv7、雪花 ID）作主键各有什么利弊？

## A
- **自增整数：** 紧凑、索引友好、顺序插入；缺点是单点生成（分片后要协调），并且泄露业务量、容易被枚举。
- **随机 UUID（v4）：** 无需协调、不可猜；但随机值插入 B 树索引时落在任意叶子页，造成页分裂、缓存局部性差，大表上写入变慢，且 16 字节比 8 字节大。
- **时间有序 ID（UUIDv7、雪花）：** 前缀是时间，插入基本追加到索引尾部，兼具无协调生成与良好的写入局部性，也方便按创建时间做游标分页；代价是泄露大致创建时间，雪花类还要管理机器号和时钟回拨。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 112" font-family="sans-serif" font-size="11">
<text x="10" y="14" fill="currentColor">随机 UUID（v4）：新键落在任意叶子页</text>
<rect x="10" y="22" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="72" y="22" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="134" y="22" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="196" y="22" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="258" y="22" width="52" height="24" fill="none" stroke="currentColor"/>
<circle cx="36" cy="34" r="5" fill="currentColor"/>
<circle cx="160" cy="34" r="5" fill="currentColor"/>
<circle cx="222" cy="34" r="5" fill="currentColor"/>
<text x="10" y="74" fill="currentColor">时间有序（UUIDv7、雪花）：追加到最右叶子</text>
<rect x="10" y="82" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="72" y="82" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="134" y="82" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="196" y="82" width="52" height="24" fill="none" stroke="currentColor"/>
<rect x="258" y="82" width="52" height="24" fill="none" stroke="currentColor"/>
<circle cx="272" cy="94" r="5" fill="currentColor"/>
<circle cx="284" cy="94" r="5" fill="currentColor"/>
<circle cx="296" cy="94" r="5" fill="currentColor"/>
</svg>

- **2026 亮点：** UUIDv7 已是标准（RFC 9562）：高 48 位是毫秒级 Unix 时间戳，其余为随机位，可在客户端生成，不需要中心化发号器；PostgreSQL 18 内置 `uuidv7()`。索引插入集中在最右叶子，页分裂和缓存失效都少。代价是 ID 暴露创建时间，且跨节点只是近似有序、不保证严格单调。
- **面试说法：** 分片或多写者系统倾向时间有序 ID；单库简单业务用自增即可。
