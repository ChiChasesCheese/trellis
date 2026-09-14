---
nodes:
- security.network-policies-private-connectivity
title: 网络策略:IP 允许/阻止名单与私有连接
corpus: snowflake-docs
section: 28-network-policies
url: https://docs.snowflake.com/en/user-guide/network-policies
tags:
- canonical
---

# 网络策略:IP 允许/阻止名单与私有连接

网络策略(network policy)控制谁能连接到 Snowflake 服务和内部 stage:允许名单里的来源可以访问,其余一律拒绝,阻止名单则用于在允许名单之外再显式排除特定来源。策略不直接罗列 IP,而是引用网络规则(network rule)——把相关标识符(IPv4/IPv6 段、私有连接的 VPC 终端 ID 等)打包成逻辑单元,便于按用途、按地区、按人群分别管理和加注释。私有连接(如 AWS PrivateLink、Azure Private Link)类型的规则优先级高于普通 IP 规则,能让流量完全绕开公网。网络策略可以分别作用于账户、用户或安全集成三个层级,越具体的层级优先级越高。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/network-policies)

## Archived copy
![[snowflak-network-policies-clip]]
%% trellis:end %%
