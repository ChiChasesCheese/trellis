---
id: hl-javaq-j-q43-details
node: java-questions.j-storage
type: qa
step: 3
---
## Q
`force(true)` 和 `force(false)` 有什么区别？新建文件后要注意什么？什么是 `O_DIRECT`？`fsync` 与 `fdatasync` 呢？
`fsync` vs `fdatasync`?

## A
- **`force(false)`** 只刷数据、不强制刷非必要元数据，对应 `fdatasync`，更快；`force(true)` 对应 `fsync`，连元数据一起刷。
- **元数据**：新建文件后要 fsync 目录项才保证文件名也持久；追加写扩展文件大小是元数据。预分配文件（`fallocate`）避免每次扩展元数据。
- **绕过 page cache**：`O_DIRECT`（Java：`ExtendedOpenOption.DIRECT`，要求缓冲区和偏移对齐到块大小），数据库自己管缓存时用。
- **读路径**：刚写的数据重读来自 page cache；冷读才碰设备。
