---
id: python-modules-dependency-direction
node: python.modules
type: qa
step: 5
tags: [grown]
---
## Q
“依赖只许朝一个方向流”这条规则，在模块/包这一层具体是什么意思？Python 会在你违反它的时候报错吗？

## A
意思是低层的工具/基础设施包（比如 `pkg.utils`、`pkg.storage`）永远不应该 `import` 高层的业务编排包（比如 `pkg.orders`），只能反过来——依赖关系画出来应该是一张有向无环图（DAG），越底层的模块越通用、越稳定。Python **不会**在语言层面阻止你违反这个方向——只有当它真的形成一个 import 环时才会报错（见循环导入那张卡）；单向的“层级倒挂”（低层偷偷 `import` 了高层的一个具体类，但没形成环）完全能正常运行，需要靠代码评审或 `import-linter` 这类工具在 CI 里强制检查。
