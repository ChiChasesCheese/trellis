---
id: profile-overview-time-categories
node: query.reading-query-profile
type: cloze
source: snowflake-docs
---
查询画像（Query Profile）的 Profile Overview 把执行时间分解为：{{c1::Processing}}（CPU 处理数据）、Local Disk IO（等待本地磁盘）、Remote Disk IO（等待远程磁盘）、{{c2::Network Communication}}（等待网络传输）、{{c3::Synchronization}}（参与进程之间的同步）和 {{c4::Initialization}}（查询处理的准备工作）。
