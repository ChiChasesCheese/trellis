---
id: mcw-max-cluster-limits-by-size
node: warehouse.multi-cluster-scaling-policy
type: cloze
source: snowflake-docs
---
多集群仓库（multi-cluster warehouse）默认最多 {{c1::10}} 个集群，可用 SQL 调高，但上限随规格变小：XSMALL/SMALL/MEDIUM 最多 {{c2::300}}，LARGE 160，XLARGE {{c3::80}}，2XLARGE 40，3XLARGE 20，4XLARGE 及以上 {{c4::10}}。Snowsight 界面里最多只能选到 10。
