---
id: uth-devtools-git-objects-1-content-address
node: devtools.git-objects
type: qa
step: 1
---
## Q
**git 用内容给对象起名**｜Git · 2.56

同一份文件内容在仓库里存几份？文件名存在哪里？

## A
**结构。** 对象库就是键值存储：键是 SHA-1（`"blob <字节数>\0"` 加内容），值是 zlib 压缩后的内容，存在 `.git/objects/<前2位>/<后38位>`。

**细节。**

- `git hash-object -w --stdin` 写入 `test content` 后，得到 40 位十六进制名字，前 2 位是目录，后 38 位是文件名
- 文件名不在 blob 里，而在目录对象（tree）里，所以内容相同的两个文件共用一个 blob
- 默认 SHA-1，源码里也支持 SHA-256，官方的迁移设计文档正是为此而写

**为什么。** 内容寻址让去重和完整性校验几乎免费，哈希对不上就是数据坏了；代价是 SHA-1 已有碰撞攻击，所以要迁移。

**对应 LeetCode：** LC 49 字母异位词分组 · LC 652 寻找重复的子树
