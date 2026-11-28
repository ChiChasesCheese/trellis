---
id: hi-c-lld-file-system-n14-folder-sync
node: lld.problem-breakdowns.file-system.notes
type: qa
step: 14
---
## Q
**内存文件系统 · `Folder` 的双向一致性**｜摘要 · 必会

`add_child` 和 `remove_child` 为什么要顺手改孩子的父指针？

## A
- **`add_child`：** 条目为空或名字冲突返回失败；否则放进字典，并把孩子的父指针设为自己。
- **`remove_child`：** 从字典取出，若存在就把它的父指针清空，返回被移除的条目。
- **为什么：** 路径靠父指针现算。如果移动时忘了更新父指针，`get_path` 会沿着旧的父亲走，返回错的位置；双向引用只有在一个地方统一维护才可靠。
- **规则：** 孩子是否挂在某个文件夹下，只能通过这两个方法改变，别处不准直接改字典或父指针。
- **`File`：** 只是数据持有者：内容、是否目录（否）。
