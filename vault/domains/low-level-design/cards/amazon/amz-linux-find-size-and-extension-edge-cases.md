---
id: amz-linux-find-size-and-extension-edge-cases
node: amazon.amz-linux-find
type: qa
step: 7
tags: [grown]
---
## Q
在 Linux find 文件搜索设计里，「大于 5MB」「后缀是 gz」这两个条件有哪些边界要先说清？

## A
- 「大于 5MB」是严格大于：`Size.over("5MB")` 的下界是 5MB+1，恰好 5242880 字节的文件不在结果里；闭区间的 `Size(min_bytes=5MB)` 才包含它。
- 只有普通文件有大小，目录和链接恒不匹配。
- `archive.tar.gz` 的后缀取最后一段 `gz`；`.bashrc` 这类隐藏文件没有后缀；`spec.XML` 不区分大小写匹配 `xml`。
- `~Extension("py")` 会把目录也选进来，要排除须再 `& OfType(Kind.FILE)`。
