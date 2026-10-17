---
nodes: [amazon.amz-parking-fees]
url: https://docs.python.org/3/library/datetime.html
---
# datetime — Basic date and time types

值得读：官方文档，讲清 `datetime.combine`、`weekday()`（周一为 0、周日为 6）以及朴素时间与带时区时间的区别。本题解的 `next_change` 正是用 `combine` 在当天拼出高峰边界，用 `weekday() < 5` 判断工作日；它只处理朴素的本地时间，夏令时切换日的 23 或 25 小时留给「扩展与追问」。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/datetime.html)

## Archived copy
![[src-pydocs-hotel-booking-clip]]
%% trellis:end %%
