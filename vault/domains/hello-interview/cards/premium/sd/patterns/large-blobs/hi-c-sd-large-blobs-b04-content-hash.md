---
id: hi-c-sd-large-blobs-b04-content-hash
node: sd.patterns.large-blobs.beyond
type: qa
step: 4
---
## Q
**大文件 · 内容寻址分块与去重**｜拓展 · 加分

网盘要节省存储并支持增量同步，大文件怎么切、怎么去重？

## A
**模式。** 内容寻址存储（content-addressed storage）：用内容哈希当对象的名字。
- **做法：** 把文件切成块（固定大小，或按内容切分的变长块），对每块算哈希（如 SHA-256），以哈希为键存储。上传前客户端先把块哈希列表发给服务器，服务器只回复缺失的块，其余不用传。
- **收益：** 相同内容只存一份（跨用户去重）；改动大文件的一小段，只重传变化的块（增量同步）；块哈希也能校验传输是否损坏。
- **固定块的缺点：** 在文件开头插入一个字节，后面所有块的边界都移位，哈希全变；按内容切分（滚动哈希决定边界）能让边界跟着内容走，只有附近的块变化。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<g stroke="currentColor" stroke-width="1.2" fill="none">
<rect x="10" y="24" width="78" height="24"/><rect x="88" y="24" width="78" height="24"/><rect x="166" y="24" width="78" height="24"/><rect x="244" y="24" width="78" height="24"/>
<rect x="92" y="132" width="78" height="24"/><rect x="170" y="132" width="78" height="24"/><rect x="248" y="132" width="78" height="24"/>
</g>
<g stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="10" y="78" width="78" height="24"/><rect x="88" y="78" width="78" height="24"/><rect x="166" y="78" width="78" height="24"/><rect x="244" y="78" width="78" height="24"/>
<rect x="10" y="132" width="82" height="24"/>
</g>
<g font-size="12" font-family="sans-serif" fill="currentColor">
<text x="10" y="16">原文件</text>
<text x="10" y="70">开头插入 1 字节，固定大小切块：边界全移位</text>
<text x="10" y="124">开头插入 1 字节，按内容切分：边界跟着内容走</text>
<text x="10" y="184">阴影 = 哈希变了，要重传</text>
<g text-anchor="middle">
<text x="49" y="41">A</text><text x="127" y="41">B</text><text x="205" y="41">C</text><text x="283" y="41">D</text>
<text x="49" y="95">A′</text><text x="127" y="95">B′</text><text x="205" y="95">C′</text><text x="283" y="95">D′</text>
<text x="51" y="149">A′</text><text x="131" y="149">B</text><text x="209" y="149">C</text><text x="287" y="149">D</text>
</g>
</g>
</svg>

- **注意：** 跨用户去重有信息泄露风险（可以通过上传速度判断别人是否有这份文件），必要时按用户加盐或仅在用户内去重；删除要用引用计数，避免误删被共享的块。
