---
id: hl-omap-skiplist-experiment
node: foundations.ordered-maps-trees
type: qa
step: 17
---
## Q
向手写跳表按升序插入 100 万个 key（普通 BST 的最坏输入），用到几层？这说明什么？

## A
实测用到 **26 层**（log₂ n 约 19.9），1000 次查找全部命中。升序输入对跳表毫无影响：层数靠硬币，与 key 顺序无关。最高层数 26 略多于 log₂ n，是少数节点运气好。
