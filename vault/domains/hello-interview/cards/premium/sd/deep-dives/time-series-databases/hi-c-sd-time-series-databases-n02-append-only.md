---
id: hi-c-sd-time-series-databases-n02-append-only
node: sd.deep-dives.time-series-databases.notes
type: qa
step: 2
---
## Q
**时序数据库 · 追加写入（append-only）**｜摘要 · 必会

为什么高吞吐写入要「只往文件末尾追加」？它和原地更新相比省在哪里？

## A
- **原地更新的代价：** 要先找到行的位置、读出旧数据、在内存里改、再写回去，每次都是随机 I/O（random I/O）。机械盘磁头要物理寻道，只有每秒约 100–200 次操作；SSD 好得多，但顺序访问依然明显更快。
- **追加的做法：** 每个新点直接写到当前文件末尾，不寻道、不先读后写，就是顺序 I/O（sequential I/O）；SSD 可到每秒数十万次顺序写，机械盘也能到数万次。
- **留下的问题：** 只追加的数据没有按键组织，读起来怎么办？这正是下一块积木（LSM 树）要解决的。
