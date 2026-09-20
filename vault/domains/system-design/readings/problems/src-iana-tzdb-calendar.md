---
nodes: [problems.realtime.calendar]
url: https://www.iana.org/time-zones
---
# IANA Time Zone Database

值得读：IANA 时区数据库官方页面,说明这份数据库会随政治实体对时区边界、UTC 偏移量和
夏令时规则的变更而定期更新（本题解引用的 2026d 版本,2026 年 9 月 11 日发布,包含加拿大
西北地区转为永久 UTC-06 这一具体变更）。比多数题解文章更具体的地方是：它给出了一个真实
的、有具体发布日期的规则变更实例,用来支撑"循环事件不能把时区换算固化成创建时刻算好的
UTC 偏移量"这一论点——本题解「深入探讨」第 3 节直接引用这个例子。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.iana.org/time-zones)
%% trellis:end %%
