---
nodes:
- security.column-masking-policies
title: 列级安全:动态数据脱敏(Masking Policy)
corpus: snowflake-docs
section: 26-security-column-intro
url: https://docs.snowflake.com/en/user-guide/security-column-intro
tags:
- canonical
---

# 列级安全:动态数据脱敏(Masking Policy)

脱敏策略(masking policy)是挂在列上的一段函数,在查询时根据当前角色决定该列返回真实值还是脱敏后的值,底层数据本身从未被改写(不是静态脱敏)。策略在查询计划里凡是引用到该列的地方——投影、JOIN 条件、WHERE 谓词、ORDER/GROUP BY——都会被强制应用,这是为了防止用户借助巧妙的查询结构“绕过”脱敏、间接反推出真实值。条件脱敏(conditional masking)允许用另一列的值决定第一列是否需要脱敏,例如按“可见性”标记决定邮箱是否公开。对象所有者默认无法查看被脱敏的数据、也无权解除策略,这种角色分离正是列级安全区别于普通安全视图的核心优势。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/security-column-intro)

## Archived copy
![[snowflak-column-masking-clip]]
%% trellis:end %%
