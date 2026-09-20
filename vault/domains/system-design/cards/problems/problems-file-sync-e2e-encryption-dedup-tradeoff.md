---
id: problems-file-sync-e2e-encryption-dedup-tradeoff
node: problems.media.file-sync
type: qa
step: 8
tags: [grown]
---
## Q
In a file sync system that relies on cross-user content-addressed deduplication for roughly 30% of its storage savings, why would making end-to-end (zero-knowledge) encryption the default break that deduplication entirely, and what is the design's remaining option to partially preserve it?

## A
Cross-user deduplication works because the server can compute a content hash over plaintext bytes and recognize when two users' content is identical; if clients encrypt content with their own per-user keys before upload, the same underlying plaintext produces completely different ciphertext (and thus a different hash) for each user, so the server can no longer tell that two encrypted blobs originated from the same content, and deduplication across users stops working. The remaining option is convergent encryption — deriving the encryption key from a hash of the plaintext itself, so identical plaintext still produces identical ciphertext across users — but this reintroduces a weaker version of the same confirmation-of-a-file side-channel risk that scoping the existence check was designed to avoid, so it trades away some of the privacy benefit it was meant to add.

## Q zh
在一个约 30% 存储节省依赖跨用户内容寻址去重的文件同步系统中，为什么把端到端（零知识）加密设为默认会让这个去重能力彻底失效？设计上还有什么办法能部分保留它？

## A zh
跨用户去重之所以有效，是因为服务器能对明文字节计算内容哈希、识别出两个用户的内容是否相同；如果客户端在上传前就用各自专属的密钥加密内容，同样的明文在不同用户那里会产生完全不同的密文（因而哈希也不同），服务器就再也无法判断两份加密内容是否源自同一份明文，跨用户去重直接失效。剩下的选项是收敛加密（convergent encryption）——用明文自身的哈希派生加密密钥，让相同明文在不同用户下仍产生相同密文——但这会重新引入一种较弱形式的、与「限定存在性检查范围」本来要避免的同一类「确认文件存在」侧信道风险，等于用它原本想增加的隐私收益去换一部分回来。
