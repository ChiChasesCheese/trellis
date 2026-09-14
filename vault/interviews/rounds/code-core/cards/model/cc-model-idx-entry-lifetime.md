---
id: cc-model-idx-entry-lifetime
node: model.index
type: qa
---
## Q
An index pins each notebook object to the server that first hosted it. Its connections come and go. When is the pin removed?

## A
**Only when the statement says — and here it deliberately outlives the rows it was created from.**

The pin survives every disconnect (a kernel stays where it was started) and is cleared only when that server is shut down. An implementation that deletes the pin when its last connection leaves is a different, wrong program.

The general rule: an index entry's lifetime is a modelling decision to be read out of the spec, not an implementation detail. Write it as a comment next to the map, because "when does this entry die?" is the question every later part will ask.

## Q zh
一个索引把每个 notebook 对象钉在最先承载它的服务器上。它的连接来来去去。这个 pin 什么时候被移除？

## A zh
**只在题面说的时候 —— 而这里它被有意设计成比创建它的那些行活得更久。**

pin 会挺过每一次断连（内核留在它启动的地方），只有当那台服务器下线时才被清除。一个"最后一个连接离开就删掉 pin"的实现，是另一个、错误的程序。

通则：索引条目的生命周期是要从题面读出来的建模决定，不是实现细节。把它写成映射旁边的注释，因为「这个条目什么时候消亡？」正是后面每一部分都会问的问题。
