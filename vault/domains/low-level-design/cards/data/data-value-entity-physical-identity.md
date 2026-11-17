---
id: data-value-entity-physical-identity
node: data.value-entity
type: qa
step: 6
---
## Q
去重工具按内容找到两个相同的文件 `a.txt` 和 `b.txt`，把它们删成一份算“节省了一个文件的空间”。但如果这两个路径是硬链接（hard link），为什么实际一个字节也没省？文件的身份到底是什么？

## A
**路径是名字，文件的身份是 (设备, inode)**

- **硬链接**：两个路径指向磁盘上同一份数据，同一个 inode；它们“内容相同”是因为本来就是同一个文件；
- **身份键**：`(st_dev, st_ino)`，inode 只在同一个设备内唯一，所以要带设备号；
- **节省量**：`size × (不同的 (st_dev, st_ino) 数 − 1)`，不是路径数减一；
- **成组仍然对**：按内容它们确实是一组，只是算空间要按身份去重；
- **同类问题**：符号链接指向别处，`stat` 默认跟随，`lstat` 才看链接本身。

```python
import os, tempfile

with tempfile.TemporaryDirectory() as d:
    a, b = os.path.join(d, "a.txt"), os.path.join(d, "b.txt")
    open(a, "w").write("same")
    os.link(a, b)                                  # b 是 a 的硬链接
    ids = {(s.st_dev, s.st_ino) for s in map(os.stat, (a, b))}
    size = os.stat(a).st_size
    print(len(ids), size * (len(ids) - 1))         # 1 0：一个文件，省下 0 字节
```

**知识点：**值对象与实体（Value vs Entity）
