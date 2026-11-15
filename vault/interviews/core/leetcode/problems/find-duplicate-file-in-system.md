---
slug: find-duplicate-file-in-system
---
## Q
**LC 609 在系统中查找重复文件**｜Medium

每项形如 `"root/a 1.txt(abcd) 2.txt(efgh)"`：目录后跟若干 `文件名(内容)`。找出内容相同的文件，每组返回它们的完整路径，只保留至少两个文件的组。

## A
**一句话。** 以内容为键做哈希分组，值是完整路径列表，最后只留下长度大于 1 的组。

```python
def find_duplicate(paths):
    groups = defaultdict(list)
    for line in paths:
        d, *files = line.split()
        for f in files:
            name, body = f[:-1].split("(")   # 去掉末尾的 )
            groups[body].append(d + "/" + name)
    return [g for g in groups.values() if len(g) > 1]
```

**复杂度。** 时间 `O(总字符数)`，空间 `O(总字符数)`。

**易错点。**
- 用文件名分组：重复指的是内容相同，文件名可以不同。
- 保留只出现一次的组：题目要的是至少两个文件。

**追问。**
- 真实文件系统里文件很大怎么办？：先按大小分组，再对同大小的文件比较前几个字节、最后算整体哈希（如 SHA-256）才逐字节比对。
- 内存装不下所有内容？：别存内容，只存哈希值和路径；或按哈希前缀分片处理。

**同模式。** LC 811 子域名访问计数、LC 588 设计内存文件系统、LC 1166 设计文件系统
