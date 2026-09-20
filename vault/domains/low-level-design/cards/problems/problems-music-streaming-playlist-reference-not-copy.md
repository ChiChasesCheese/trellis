---
id: problems-music-streaming-playlist-reference-not-copy
node: problems.social.music-streaming
type: qa
step: 1
tags: [grown]
---
## Q
音乐流媒体（Spotify）设计里，播放列表为什么只存曲目 id、而不是直接持有 `Track` 对象或复制一份曲目数据？

## A
如果播放列表持有的是对象引用甚至一份数据副本，一首歌从曲库下架之后，播放列表不会自动“发现”这件事——Python 的对象依然在内存里，除非每次读播放列表都反过来问一遍曲库“这个还在吗”。只存 id 把“播放列表是曲目的一个引用集合、不拥有它的生命周期”这句话落成了具体的数据结构：额外维护一份“曲目 id → 引用过它的播放列表”的反向索引，一首歌下架时可以直接查到受影响的播放列表并摘除引用，不用扫描系统里可能存在的成千上万份播放列表。
