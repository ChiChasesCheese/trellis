# 工厂游戏：24 小时产线冲分（Roblox OA）

目标：24 小时结束时手上的钱越多越好。可以测试很多次，成绩取最高的一次。考试只有 25 分钟。
本目录的定位是**拿到真实题目后 5 分钟内出方案，速度优先于最优**。搜索有 280 秒的硬性上限，默认跑 60 秒，教学关 2 秒内就收敛了。

```bash
cd vault/interviews/companies/roblox/games/factory
python3 -m unittest test_factory -v           # 14 条测试，每条对应说明里的一条规则
python3 factory.py level.json --time 60       # → 每台机器在游戏里该填什么 + 模拟出的余额 + 浪费
python3 calibrate_tutorial.py                 # 教学关对账：哪些配方能复现 $3,828 / 168 个三明治
```

## 5 分钟流程

1. **转录（2 分钟）**：复制 `sandwich_tutorial.json`，每台机器写一条：
   - `kind`：`supplier`、`maker` 或 `seller`。
   - `row`：在屏幕上的上下位置，数字小的在上。分配优先级平局时靠它决定。
   - `rate`：面板上的数字。Supplier 是“Order every hour”，Maker / Seller 是“Try to make”。
   - Supplier 的 `unit_cost`：面板上的 Cost per item。
   - Maker / Seller 的 `options`：每个可选产品写一条，包括 `inputs`（从哪台机器取、每件要几个）、`price`（Seller 的售价）、`period`（带时钟图标的写 2）。
   - `mods`：Modify Machine 面板里每种改装每件加多少钱。
   - 和默认值不同时才写：`max_rate`（默认 50）、`storage`（Maker 默认 100，Supplier 默认 1000）、`option`（当前选中的产品序号）。
2. **核对（30 秒）**：输出第一行 `as transcribed` 必须等于游戏里 Initial Test 的分数。
   对不上，说明转录错了，最常见的是配方数量或者售价。**对上了才往下走。**
3. **搜索（60 秒）**：照着 `enter in the game:` 一行一行填进游戏，点 Test Factory，拿游戏的分数和模拟分数对账。
4. 时间还有剩，就从测试结果里挑“剩余 / 浪费”最多的那台机器调小，这对应 Chi 心得的第 3、5 条。

## 规则（游戏内说明，2026-09-28 转录；Chi 确认的细节标 [Chi]）

| 类别 | 规则 |
|---|---|
| 目标 | 起始资金（教学关 $3,000），24 小时后的余额就是分数。可以测试多次，取最高的一次；可以从任意一次测试接着改 |
| Supplier | 每小时下单 N 件，**立即到货**，本小时就能用。**每件都要付钱**，用不用都付。存储上限 1000 |
| Maker | 每小时**尝试**做 N 件，上限 50。**原料不够一整批，这一小时就什么都不做**。产出在本小时末放进自己的存储，**下一小时**下游才能取用。存储上限 100 |
| 2 小时机器 | 带时钟图标的机器，产出在第二个小时末入库。[Chi] 开工时一次取够原料，然后占用 2 小时 |
| Seller | 没有存储，做出来立刻卖掉 |
| 存储满了 | 放不下的产出直接丢失。[Chi] 原料和改装费照扣 |
| 分配优先级 | 一台机器连着多个下游时，**离 Seller 最近的下游先拿**，[Chi] “最近”指经过的机器数最少；距离相同，屏幕上靠上的先拿。某个下游要的量凑不齐，就跳过它，一件也不给，接着看下一个。[Chi] 所有机器在每小时开始时按这个顺序取货 |
| 切换产品 | 有的 Maker 可以换产品，换了之后需要的原料种类、数量和售价都会变 |
| 改装（只能装在 Maker 上，**每做一件都额外收费**） | 2x Output Max：上限从 50 变成 100，是提高上限，不是把产出翻倍；½ Materials：原料用量减半，奇数向上取整（这一条是猜的）；1 Hour Production：只对 2 小时的机器有效；2x Storage：存储上限翻倍 |
| 界面 | Draft 面板会显示 Starting Money 和每小时的 Material Costs |

**对账**：教学关每小时材料费是 $35.50，等于 15×0.5 + 24×0.5 + 30×0.2 + 20×0.5。
$3,828 − $3,000 + 24 × $35.50 = $1,680 = 168 × **$10**，由此反推出三明治的售价。
截图上看不到配方，`calibrate_tutorial.py` 找到 20 组“配方 + 终端产量”能精确复现 $3,828 和 168 个。
这说明模型的时序和计价**能**对上游戏，但光靠这些数据还不能把配方唯一确定下来。
网上（prachub、Glassdoor、AceOffer 等）**没有**任何一份给出这些数值规则，游戏内的说明就是唯一的一手来源。

## Chi 的 151k 心得，以及它在模型里对应什么

1. **先保基础产量，从终端倒推**：`backward_fill()` 就是这一步，而且会对“关掉若干条产品线”的每种组合各做一次，对应“只做赚钱的”。终端先开到上限，上游按下游需求逐级填，哪里超了上限就压低终端。Chi 说这一步能拿到 100k–110k。
2. **Buff**：
   - a. **原料减半**是主力，用来突破中间环节的产能瓶颈、多卖终端产品，不是用来省原料钱的，因为 Buff 本身也要钱。
   - b. **产量翻倍**要慎用：它按件收费，本来不收钱的那部分产量也开始收钱了。只有当这条产线能拉满、而且产出都能被下游用掉时才划算。
   - c. **2h 变 1h**：二十几元，基本稳赚。

   搜索会逐个节点试开和关，按模拟出的分数决定取舍。注意：游戏里的 2x Output Max 是把上限从 50 提到 100，不是把产出翻倍。
3. **启动晚的下游**：上游在第 x 小时开始供应，下游第 x+2 小时才开工，那么上游早产出的部分只是提前付钱。可以把上游调小一点。报告里“剩余库存”那一行会显示这类浪费。
4. **终端多设一点，减少批次**：在“整批”规则下，终端设高一点、批次少一点，有可能把最后剩下的材料用掉，总数反而更多。搜索会逐个试步长 ±1、±2、±5、±10、±25。
5. **2 小时的加工厂直连终端**：24 小时结束时，2 小时产出的材料可能还有剩余，可以适当按比例提高终端销量，把剩下的材料吃掉。

网上帖子的补充：**先砍掉亏钱的产品**，再从后往前把赚钱的产线拉满；两种产品共用一个零件时，优先分给利润高的。

## 同类游戏的资料（2026-09-27 调研）

- **机器人 / 造车（Robots）**：给车装部件（轮子、Blowtorch 等），每个部件有 Energy Cost，有总量上限（截图里是“0 of 3”）。让车通过障碍赛道，有的版本比的是造出的车数量。
  部件装在不同位置效果可能完全不同。可以测试多次，一次只改一个部件。
- **Outpost: Mars（技术岗）**：积木式编程，控制火星上的机器人或无人机完成地图任务。要把重复动作封装成带参数的函数（截图里是 `diag(x, y, size, length, f)`），
  一个函数要在多个 Example 里都匹配成功。可以先用 Roblox 的“Coding Cookies”熟悉界面。
- **CodeSignal**：LeetCode 高频题及其变形。
- 参考仓库：[sarikameera/roblox-assessment-suite](https://github.com/sarikameera/roblox-assessment-suite)。作者自称是复刻版，但没有许可证，数值和机制都是作者编的；它的工厂是“建机器 / 升级”，和真实界面对不上，所以**不采用**。
  如果真实题目变成了“建机器 / 升级”的形式，可以这样映射：建机器相当于一次性收费（`flat`），升级相当于提高 `max_rate`。
  [anhducnguyen2006/KaijuCatsAI](https://github.com/anhducnguyen2006/KaijuCatsAI)（MIT）只写了 Kaiju Cats 的地图生成，规则是作者自己猜的。

### 来源

- Chi 的实测心得（151k）和截图，2026-09-27
- 小红书《Roblox OA 游戏 小技巧》（Chi 转述），2026-09-27
- [Glassdoor：Task 2 工厂 + 250–1000 字策略文章；Task 3 造车](https://www.glassdoor.com/Interview/Task-2-Problem-Solving-and-Communication-Assessments-45-minutes-It-s-in-a-game-format%EF%BC%9AGiven-a-factory-how-do-you-desig-QTN_8468961.htm)
- [Glassdoor：24 小时工厂赚最多钱](https://www.glassdoor.com/Interview/One-of-the-logic-problem-games-that-I-was-asked-involved-optimizing-a-factory-to-produce-the-most-money-in-a-24hr-period-QTN_6604622.htm)
- [csvoprep：Roblox OA 复盘（Mars + BQ + Code）](https://csvoprep.com/oa/roblox-oa-mars-bq-code/)，代写 / 代考服务站，可信度低
- [AceOffer：Factory Profit Maximization](https://aceoffer.app/interviews/rblx_factory_profit_maximization_assembly_line_optimization_oa)，同样是服务站，只给了策略，没有数值
- 一亩三分地 [thread-942545](https://www.1point3acres.com/bbs/thread-942545-1-1.html)：抓取返回 403，没读到
