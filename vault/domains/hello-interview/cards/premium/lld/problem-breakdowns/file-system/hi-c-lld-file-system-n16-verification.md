---
id: hi-c-lld-file-system-n16-verification
node: lld.problem-breakdowns.file-system.notes
type: qa
step: 16
---
## Q
**内存文件系统 · 走一遍创建、移动和错误**｜摘要 · 追问

写完代码后，怎样验证树和父指针在创建、移动、出错时都对？

## A
- **建目录：** 空树只有根。创建 `/home`：父是根，名字 `home`，无冲突，挂到根下。创建 `/home/user`：父是 `home`，挂上。
- **建文件并看路径：** 创建 `/home/user/notes.txt`；`get_path()`：先问父 `user` 要路径 `/home/user`，再拼上 `/notes.txt`，得 `/home/user/notes.txt`。
- **移动：** 把它移到 `/home/notes.txt`：源是 `user` 下的文件，目标父是 `home`；文件不是目录，跳过成环检查；`home` 没有同名；从 `user` 摘下（父指针置空）、挂到 `home`（父指针改为 `home`）。再取路径得 `/home/notes.txt`，没有更新任何字符串。
- **错误：** 在 `/home` 下再建 `notes.txt`→重名；删除不存在的路径→找不到；把 `/home` 移到 `/home/user/stuff`→从目标父向上走碰到 `home`，拒绝。
- **重点：** 每次操作后核对"字典里有没有它"和"它的父指针"是否一致。
