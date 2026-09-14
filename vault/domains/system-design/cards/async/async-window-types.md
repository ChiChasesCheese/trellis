---
id: async-window-types
node: async.streaming.processing
type: cloze
---
The four stream window types: a **tumbling** window has {{c1::a fixed length and no overlap — every event belongs to exactly one window (e.g. 1-minute buckets)}}. A **hopping** window has {{c2::a fixed length but advances by a smaller hop, so windows overlap and each event lands in several (e.g. 5-minute windows every 1 minute, for smoothed aggregates)}}. A **sliding** window contains {{c3::all events within some interval of each other, with boundaries set by the events themselves rather than a fixed grid}}. A **session** window {{c4::has no fixed length at all — it groups an entity's burst of activity and closes after a gap of inactivity (timeout), so its span differs per key}}.

## zh
四种流处理窗口：**tumbling window（滚动窗口）**是{{c1::固定长度、互不重叠——每个事件恰好属于一个窗口（如 1 分钟一桶）}}。**hopping window（跳跃窗口）**是{{c2::固定长度但按更小的步长前进，窗口相互重叠、每个事件落进多个窗口（如每 1 分钟产生一个 5 分钟窗口，用于平滑聚合）}}。**sliding window（滑动窗口）**包含{{c3::彼此间隔在某个区间之内的所有事件，边界由事件本身决定而不是固定网格}}。**session window（会话窗口）**{{c4::完全没有固定长度——它把一个实体的一段连续活动聚在一起，在一段不活动间隙（超时）后关闭，所以每个 key 的窗口跨度都不同}}。
