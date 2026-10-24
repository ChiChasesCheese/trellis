---
id: pl-fuzz-pitfall-checksum-gate
node: engineering.fuzzing
type: qa
step: 8
---
## Q
为什么 fuzz 跑了几百万次、一个 bug 也没找到，不代表代码没有 bug？以校验和为例说明，并给出补救办法。

## A
覆盖率引导靠「输入逐步接近目标时执行路径会变」来搜索。校验和、哈希、签名这类条件打破了这个前提：输入差一位，校验就失败、走进同一个拒绝分支，没有任何信号告诉模糊器「更近了」。

**例**：`Decode` 要求输入是「4 字节 CRC32 加正文」，校验通过才调用 `Body`；`Body` 里藏着越界 bug：

```go
func Decode(b []byte) byte {
    if len(b) < 5 { return 0 }
    if crc32.ChecksumIEEE(b[4:]) != binary.BigEndian.Uint32(b[:4]) {
        return 0 // rejected: bad checksum
    }
    return Body(b[4:])   // b[0]=='X' && b[1]=='Y' -> reads b[2]
}
```

对 `Decode` 做 10 秒模糊测试：

```text
fuzz: elapsed: 10s, execs: 9787851 (884426/sec), new interesting: 2 (total: 3)
PASS
```

近 1000 万次执行，只发现 3 个「有趣」的输入，没有失败：随机字节能碰巧通过 CRC 的概率是 2^-32。bug 一直躲在校验后面，但这是一个**假阴性**。

**补救**：
- **直接测内层**：为校验之后的 `Body` 单独写一个 fuzz 目标。同样跑 10 秒，不到 0.1 秒就失败了；
- **在 fuzz 构建里绕过校验**：用构建标志或接口替换，让校验在 fuzz 时恒为真（LLVM 生态里常见的做法，叫 fuzzing mode 开关）；
- **让 fuzz 目标自己补上校验和**：目标函数先把输入当作正文，自己算好 CRC 再拼接。

规则：看 fuzz 的覆盖率报告，确认深层代码真的被执行过；没被执行的代码，没有被测试过。
