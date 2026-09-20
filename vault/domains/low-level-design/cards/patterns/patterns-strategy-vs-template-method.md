---
id: patterns-strategy-vs-template-method
node: patterns.strategy
type: qa
step: 4
---
## Q
Strategy（组合）和 Template Method（继承）都能让"某一步怎么做"可替换，什么时候优先选哪一个？

## A
Template Method 把固定顺序的步骤写在基类里，只留一两个钩子给子类覆盖——继承关系是静态的，子类一旦选定，算法在对象的整个生命周期里都换不掉。Strategy 把整个算法当作一个对象持有，可以随时通过重新赋值换掉。Python 里更进一步：如果只有一个钩子要变，通常直接给固定流程传一个回调函数，比专门声明子类更轻，不必引入继承。经验：步骤顺序固定、只是想复用骨架时用 Template Method（或者干脆传函数）；需要在运行时整体切换算法时用 Strategy。
