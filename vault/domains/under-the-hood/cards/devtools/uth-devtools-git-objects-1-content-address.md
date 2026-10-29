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
**背景。** 版本控制要存每个版本的每个文件。每次提交都存一份完整副本太浪费，因为大多数文件没变。办法：用内容的指纹当名字。SHA-1 是一种哈希函数，把任意内容变成固定的 40 位十六进制数，不同内容几乎不会得到同一个数。名字由内容决定，内容相同名字就相同，自然只存一份。

**结构。** 对象库就是键值存储：键是 SHA-1（对 `"blob <字节数>\0"` 加内容计算），值是 zlib 压缩后的内容，存在 `.git/objects/<前2位>/<后38位>`。例：`a.txt` 和 `b.txt` 内容都是 `hello`，只存一个 blob（git 里表示“文件内容”的对象）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="75" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">tree 目录</text>
<text x="270" y="22" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">blob 内容</text>
<rect x="20" y="32" width="110" height="70" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="20" y1="67" x2="130" y2="67" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="75" y="55" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a.txt</text>
<text x="75" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b.txt</text>
<rect x="220" y="48" width="100" height="38" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="270" y="65" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ce01</text>
<text x="270" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">hello</text>
<line x1="132" y1="50" x2="213.033" y2="59.4225" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M218.0,60.0 L210.9,62.5 L211.7,56.0 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="132" y1="86" x2="213.048" y2="74.691" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M218.0,74.0 L211.8,78.2 L210.9,71.7 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="130" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">名字 = SHA-1(内容)</text>
<text x="170" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">内容相同 只存一份</text>
</svg>
```

**细节。**

- `git hash-object -w --stdin` 写入 `test content` 后，得到 40 位十六进制名字，前 2 位是目录，后 38 位是文件名
- 文件名不在 blob 里，而在目录对象（tree）里，所以内容相同的两个文件共用一个 blob
- 默认 SHA-1，源码里也支持 SHA-256，官方的迁移设计文档正是为此而写

**为什么。** 内容寻址让去重和完整性校验几乎免费，哈希对不上就是数据坏了；代价是 SHA-1 已有碰撞攻击，所以要迁移。

**例题：** LC 49 字母异位词分组

把字母异位词（字母相同、顺序不同的词）分到同一组，按任意顺序返回。例：`["eat","tea","tan","ate","nat","bat"]` → `[["bat"],["nat","tan"],["ate","eat","tea"]]`。

```python
from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: defaultdict[tuple[int, ...], list[str]] = defaultdict(list)
    for s in strs:
        count = [0] * 26                       # 26 个字母的出现次数就是指纹
        for ch in s:
            count[ord(ch) - ord("a")] += 1
        groups[tuple(count)].append(s)         # list 不可哈希，转成 tuple 才能当键
    return list(groups.values())
```
