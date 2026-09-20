---
id: problems-file-sync-dedup-confirmation-side-channel
node: problems.media.file-sync
type: qa
step: 7
tags: [grown]
---
## Q
In a file sync system with cross-user content-addressed deduplication, why is exposing a client-facing 'does a block with this hash already exist' API a security risk, how can a design keep the storage savings without exposing it, and what does that scoping cost?

## A
If any client can freely query whether a given content hash already exists in the system, an attacker who knows the hash of a specific known file can probe the API to learn whether that exact file has been uploaded by anyone — a 'confirmation of a file' side channel that leaks information about other users' stored content without ever downloading it. A design can keep the underlying storage-layer deduplication (identical bytes still map to one stored block) while scoping the client-visible 'do you already have this' check to only the blocks already visible within the requesting account or shared space, so the boolean existence check is never exposed as a global, freely queryable oracle. This scoping has a real cost: for a block that already exists in storage from another user but that the requesting account has never seen, the server treats it as missing and makes the client upload the bytes anyway, deduplicating only on write (one extra reference, no second copy on disk) — so the disk-space saving is kept, but the network-bandwidth saving that a global existence check would have given for cross-user duplicates is lost.

## Q zh
在一个具有跨用户内容寻址去重能力的文件同步系统中，为什么向客户端暴露一个「这个哈希的块是否已存在」的 API 是一种安全风险？设计上如何在不暴露它的前提下保留存储节省？这种限定范围的做法要付出什么代价？

## A zh
如果任何客户端都能自由查询某个内容哈希是否已存在于系统中，一个知道某份已知文件哈希的攻击者就可以探测这个 API，从而得知这份确切的文件是否已经被别人上传过——这是一种「确认文件存在」的侧信道，在不下载任何内容的情况下泄露了其他用户已存储内容的信息。设计上可以保留底层存储层的去重能力（相同字节仍然映射到同一个已存储的块），同时把面向客户端可见的「你是否已拥有这个」检查限定在请求账号或共享空间内已经可见的块范围内，从不把这个布尔存在性检查暴露成一个全局可自由查询的预言机。这个限定范围的做法有真实代价：对于一个已经存在于存储里、但请求账号从未见过的块（典型的跨用户重复内容），服务器会把它当成缺失块，仍然要求客户端把字节上传一遍，去重只发生在写入这一步（只增加一条引用，磁盘上不重复写）——所以磁盘存储的节省保留了下来，但一个全局存在性检查本可以带来的、针对跨用户重复内容的网络带宽节省则失去了。
