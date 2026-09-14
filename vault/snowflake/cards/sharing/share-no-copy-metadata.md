---
id: share-no-copy-metadata
node: sharing.secure-data-sharing-mechanics
type: qa
source: snowflake-docs
---
## Q
Snowflake 的安全数据共享（Secure Data Sharing）把一个 1TB 的表共享给另一个账户，需要多久？消费方要为这 1TB 付存储费吗？为什么？

## A
几乎瞬间完成，消费方也不付存储费。因为共享时账户之间不复制、不传输任何实际数据：共享完全通过 Snowflake 的云服务层和元数据存储实现，消费方拿到的只是指向提供方存储中数据的元数据授权。共享数据不占消费方账户的存储，消费方唯一的费用是查询这些数据时自己虚拟仓库（virtual warehouse）消耗的计算资源。
