---
nodes: [problems.commerce.payment-system]
url: https://developer.squareup.com/blog/books-an-immutable-double-entry-accounting-database-service/
---
# Books: an immutable double-entry accounting database service

值得读：Square 官方工程博客披露了其内部双录账本服务 Books 的具体规模——约 20 TB 数据,
仅 3 名工程师维护——以及"除当前余额字段所在的表之外,其余表只有插入语句、没有更新语句"
这一实现细节,并给出了把"应付商户金额"建模成一个独立账户、使得计算打款金额退化为读一行
而不是聚合查询的具体例子。与本题解不同的地方在于：Square 的文章没有讨论幂等提交与账本
写入的关系,本题解把幂等发起(客户端幂等键 + PSP 侧幂等键)和账本不可变性当作两个独立
但互补的机制分别设计,而不是把幂等归入账本本身的职责。
