---
nodes:
- architecture.three-layer-model
- architecture.storage-compute-separation
- architecture.multi-cluster-shared-data
- architecture.cloud-services-layer
- architecture.cloud-agnostic-multi-region
- storage.object-storage-backend
title: Snowflake 关键概念与整体架构
corpus: snowflake-docs
section: 01-intro-key-concepts
url: https://docs.snowflake.com/en/user-guide/intro-key-concepts
tags:
- canonical
---

# Snowflake 关键概念与整体架构

理解 Snowflake 的起点:存储、计算(虚拟仓库,virtual warehouse)与云服务(cloud services)三层物理、逻辑分离,只通过元数据通信。其架构是共享磁盘(shared-disk)与无共享(shared-nothing)的混合体——所有计算节点访问同一份持久化存储,但每个虚拟仓库拥有独立的、大规模并行处理(MPP)计算集群,互不干扰。云服务层负责鉴权、查询解析优化、元数据管理等,从不直接触碰表数据字节。文中还提到 Snowgrid 跨云跨区域(cross-cloud/cross-region)技术层,把安全策略和容灾复制扩展到不同云和地域;表数据最终以压缩列式格式存放在云对象存储中而非本地磁盘。读完应能画出三层架构草图,理解为什么存储计算分离是后续弹性、多集群共享数据等一切特性的前提。
