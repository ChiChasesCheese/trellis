---
id: problems-pastebin-dedup-privacy-tradeoff
node: problems.foundations.pastebin
type: qa
step: 4
tags: [grown]
---
## Q
In a pastebin design that content-addresses object-storage-backed blobs by their SHA-256 hash (so two identical pastes collapse to one stored object with a reference count), why should this deduplication be applied only to public pastes and never to private or unlisted ones?

## A
Content-addressed dedup on private content creates two privacy problems. First, an existence oracle: an attacker who already possesses specific sensitive content can compute its hash and create a paste with that same content; if the write completes unusually fast (because it only bumps a reference count instead of uploading bytes), that timing difference lets the attacker infer that someone else already pasted the identical content, even without ever reading it. Second, deletion stops being real erasure: if one user's private paste references the same deduplicated bytes as another user's paste, deleting the first user's paste only decrements the reference count — the underlying bytes remain until every reference is gone, breaking a private paste's implicit promise that deleting it removes the content. Public pastes have no such secrecy claim to protect, so the storage savings from dedup are worth taking only there.

## Q zh
在一个 pastebin 设计中，对象存储里的 blob 按其 SHA-256 哈希做内容寻址（两条内容相同的粘贴会合并成一份带引用计数的物理对象），为什么这种去重应该只应用于公开粘贴，绝不能用于私有或不可列出的粘贴？

## A zh
对私有内容做内容寻址去重会带来两个隐私问题。第一，存在性预言：已经掌握某份敏感内容的攻击者可以计算出它的哈希，然后创建一条内容相同的粘贴；如果这次写入明显异常地快（因为只是把引用计数加一，而不是真的上传字节），这个耗时差异就能让攻击者推断出已经有人贴过完全相同的内容，即使他从未真正读到这份内容。第二，删除不再是真正的擦除：如果一个用户的私有粘贴和另一个用户的粘贴恰好引用了同一份去重后的字节，删除前者只会让引用计数减一——底层字节要等所有引用都消失才会真正释放，这打破了私有粘贴「删除即移除内容」这一隐含承诺。公开粘贴没有这种保密诉求需要保护，所以去重带来的存储节省只值得在公开粘贴上拿。
