---
nodes: [problems.marketplaces.food-delivery]
url: https://github.com/kumaransg/LLD/tree/main/FoodKart
tags: [no-archive]
---
# kumaransg/LLD — FoodKart

值得读：一份真实的 Flipkart 机考题面（90 分钟、纯内存、要求可演示、明确按"可扩展性 / 边界
处理 / 可读性"打分），最值得学的是它的**约束风格**——"餐厅只卖一道菜""按 pincode 判断是否
可送""餐厅可服务多个区域""按评分或价格降序展示"，每一条都窄到能在九十分钟内做完。它其实是
一道**目录、库存与排序**题：没有骑手这一方，也没有订单生命周期，`place_order` 之后就结束了。
把它和本题解并排看，能清楚看到"加一个参与方"让难度跳了一级：一旦骑手进来，状态机就必须回答
"谁有权走这条边"，派单时机也才成为一个问题。它的评分规则（rating 是所有评价的平均）可以
当作本题第 4 关的一个额外追问。（仓库无 LICENSE，只链接不复制。）
