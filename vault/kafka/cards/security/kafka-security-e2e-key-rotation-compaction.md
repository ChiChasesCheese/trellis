---
id: kafka-security-e2e-key-rotation-compaction
node: security.protocols-auth-encryption
type: qa
source: kafka-2e
---
## Q
端到端加密建议定期轮换用于加解密消息的共享密钥，但为什么这在压实型主题（compacted topic，对每个 key 只保留最新一条消息的主题）上会格外麻烦？

## A
轮换密钥能降低密钥一旦泄露的影响范围、防止暴力破解，但只要用旧密钥加密的消息还在保留策略内，新旧密钥就必须同时保持可用以便解密。普通主题的旧消息会随时间过期，压实主题却可能长期保留某个 key 下用旧密钥加密的历史消息，等于要长期维护多套密钥，甚至需要用新密钥对旧消息重新加密；而重新加密期间为避免和新写入的消息产生冲突，通常要求生产者和消费者暂时下线。
