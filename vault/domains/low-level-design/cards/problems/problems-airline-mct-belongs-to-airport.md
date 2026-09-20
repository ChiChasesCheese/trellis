---
id: problems-airline-mct-belongs-to-airport
node: problems.booking.airline
type: qa
step: 3
tags: [grown]
---
## Q
航班管理设计里，最短衔接时间（Minimum Connection Time，MCT）为什么建模成挂在机场上的规则，而不是挂在航班或某条具体航线上？

## A
MCT 反映的是机场的物理条件——航站楼之间的距离、要不要重新过安检、行李转运效率——和具体飞哪一班、去哪里无关。如果按航班或航线存一份，一个机场调整航站楼布局或新增安检流程，就要去改成百上千条航线的配置；建成独立的 `MinimumConnectionTime`（默认值 + 按机场覆盖 + 跨承运人加时），机场变化只需要改一处。
