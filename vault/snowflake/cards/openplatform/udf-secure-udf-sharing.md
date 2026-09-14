---
id: udf-secure-udf-sharing
node: openplatform.snowpark-udf-udtf
type: qa
tags: [grown]
---
## Q
把一个 UDF 通过数据共享提供给其他账户时，为什么通常要把它定义为安全 UDF（secure UDF）？代价是什么？

## A
普通 UDF 的定义（函数体代码）对有权限的用户可见，优化器也可能在执行时暴露中间信息，消费方可能看到提供方的专有逻辑。安全 UDF 隐藏函数定义，只有所有者能看到代码，并禁用某些可能泄露底层数据的优化。代价是查询可能更慢，因为部分优化被关闭。
