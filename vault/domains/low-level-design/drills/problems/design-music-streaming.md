---
nodes: [problems.social.music-streaming, patterns.state]
tags: [problem]
---
# Drill：音乐流媒体（Spotify）

一个音乐播放客户端：曲库里有艺人、专辑、曲目；用户能建播放列表（引用曲目、支持协作编辑）；
播放器在停止/播放/暂停三态间转移，围绕一个由来源（专辑/播放列表/电台）加洗牌、循环生成的
播放队列；播放历史用来算最常播放和最近播放。跨设备同步和真正的推荐算法不在这道题里。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：艺人、专辑、曲目，播放列表引用曲目而不是复制。先决定"一首歌从
  曲库下架，播放列表该怎么办"——这个决定不对，后面每一步都会留下悬空引用。
- 第 2 关（约 20 分钟）：播放器三态，播放队列。精确定义洗牌对"播放中途加歌"意味着什么、
  "上一首"在洗牌之后该怎么走、repeat=all 用完一轮之后队列该怎么继续——最后这条是本题的
  硬指标：队列不能随着循环的轮数无限变长。
- 第 3 关（约 15 分钟）：播放历史与派生统计（最常播放、最近播放），离线标记。统计必须是
  对历史现算出来的，不能是另存的计数字段。
- 第 4 关（选做）：给播放列表加多个协作编辑者，或者做一个由播放历史种子生成的简单推荐。
  评分点是"加它有没有碰到播放器或播放队列那段代码的任何一行"。

**怎么练**：把 `vault/domains/low-level-design/problems/music-streaming/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/music-streaming -q`。

**评分点**
- 播放列表只存曲目 id，配一份反向索引，一首歌下架时直接找到受影响的播放列表而不扫描全部（[[problems-music-streaming-playlist-reference-not-copy]]）。
- "上一首"永远沿真实播放过的顺序走，完全不受此刻洗牌开没开的影响（[[problems-music-streaming-shuffle-splits-history-upcoming]]）。
- 洗牌开着时新加的歌要插进剩余队列的一个随机位置，不能永远追加到末尾（[[problems-music-streaming-add-track-random-insert-when-shuffled]]）。
- repeat=all 用完一轮要原地重新生成待播列表，不能把来源拼接进已有队列，否则队列会随播放轮数无限变长（[[problems-music-streaming-repeat-all-regenerate-not-extend]]）。
- 播放器三态之间即便有一处行为差异，也不足以让每个状态各建一个类——判据是差异的规模，不是有没有差异（[[problems-music-streaming-player-enum-table-small-diff]]）。
- 最常播放、最近播放都是对播放历史现算出来的，不是另存、需要手动同步的计数字段（[[problems-music-streaming-stats-derived-not-counters]]）。
- 反向索引的大小是一个可以直接断言的不变量：一首歌下架后它应该变小（[[problems-music-streaming-referenced-track-count-shrinks]]）。
- 协作播放列表的权限只活在播放列表自己身上，加它不碰播放器或播放队列的任何一行代码（[[problems-music-streaming-collaborative-playlist-proves-extension]]）。

**题解**：[[solution-music-streaming]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
