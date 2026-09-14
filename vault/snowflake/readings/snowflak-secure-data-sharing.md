---
nodes:
- sharing.secure-data-sharing-mechanics
- sharing.reader-accounts
- sharing.data-marketplace-listings
title: 安全数据共享(Secure Data Sharing)、Reader 账户与 Listing
corpus: snowflake-docs
section: 29-data-sharing-intro
url: https://docs.snowflake.com/en/user-guide/data-sharing-intro
tags:
- canonical
---

# 安全数据共享(Secure Data Sharing)、Reader 账户与 Listing

安全数据共享不复制、不搬运任何数据:提供方(provider)创建一个共享(share)对象,把数据库中选定对象的访问权限授予消费方账户,消费方随即能创建一个只读数据库,近乎实时地看到与源端一致的数据,消费方只为查询所用的计算资源付费,不产生额外存储费用。共享方式包括:直接共享给指定账户、发布为可发现的 Listing(私有或上架 Snowflake Marketplace)、或组织成 Data Exchange 群组。对于还没有自己 Snowflake 账户的第三方消费者,提供方可以创建由自己账户承担费用的 Reader 账户,让对方只能查询导入的数据、不能做任何数据写入操作。
