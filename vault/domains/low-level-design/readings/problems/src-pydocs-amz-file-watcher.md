---
nodes: [amazon.amz-file-watcher]
url: https://docs.python.org/3/library/os.html#os.scandir
---
# os.scandir（Python 标准库文档）

值得读：英文官方文档。`DirEntry` 的 `is_dir(follow_symlinks=False)` 与缓存的 `stat()` 是本题解 `DiskFileSystem` 遍历目录的依据；同一页还提醒了遍历途中文件可能消失，所以消失的文件应当跳过而不是报错。
