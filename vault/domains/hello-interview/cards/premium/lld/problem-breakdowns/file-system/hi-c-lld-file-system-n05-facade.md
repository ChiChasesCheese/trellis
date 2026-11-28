---
id: hi-c-lld-file-system-n05-facade
node: lld.problem-breakdowns.file-system.notes
type: qa
step: 5
---
## Q
**内存文件系统 · 要不要 `FileSystem` 门面**｜摘要 · 必会

不建 `FileSystem` 类，直接把根文件夹暴露给调用者行不行？

## A
- **不建门面（反面）：** 调用者拿着根，一层层 `create_folder`、再 `create_file`。要在 `/home/user/docs/` 下建文件，得自己拆路径、逐层走、处理中间目录不存在的情形，然后才创建。
- **后果：** 每个调用者重复实现路径解析（违反 DRY）；没有明确的入口，调用者还得自己保存根并到处传。
- **建门面（选这个）：** `FileSystem` 持有根，所有操作收绝对路径，由它解析、导航、校验，再委托给具体的文件夹或文件。这是门面模式（Facade）：把树导航的复杂度藏在简单的路径接口后面。
- **状态很少：** 只有根；路径是现解析的，不用存。
- **接口：** `create_file`、`create_folder`、`delete`、`list`、`get`、`rename`、`move`。
- **构造：** 建一个空的根；所有方法收路径，失败时抛异常（路径无效、找不到、重名）。
