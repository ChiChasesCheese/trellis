# 工厂游戏：24 小时产线冲分（Roblox OA）

目标：在 24 小时里赚到尽可能多的钱。可以测试很多次，成绩取最好的一次。考试只有 25 分钟。
本目录的定位是**拿到真实题目后 5 分钟内出方案，速度优先于最优**。

```bash
cd vault/interviews/companies/roblox/games/factory
python3 -m unittest test_factory -v                  # 每条规则一条测试
python3 factory.py level.json --time 60              # 转录好的关卡 → 每个节点的设置 + 分数 + 剩余库存
python3 factory.py level.json --batch partial        # 规则开关，见下文“待确认”
```

## 5 分钟流程

1. **转录（2 分钟）**：照着 `sandwich_tutorial.json` 写 `level.json`。每个节点记下：
   - 屏幕上的数字 → `rate`
   - `x$0.50` → `unit_cost`
   - `1 of 2hrs` → `period: 2`
   - 配方 → `inputs`（每产 1 件要几件上游材料）
   - 售价 → `price`
   - 这个节点能开的 Buff → `buffs`

   Buff 的价格填进 `buff_cost`，按件收费填 `per_unit`，一次性收费填 `flat`。
2. **核对（30 秒）**：命令输出的第一行 `as transcribed` 是“按截图原样设置”的模拟分数。拿它和游戏里 Initial Test 的分数比：
   对不上，说明转录或规则有误，先改转录，再试 `--batch partial` 或 `--same-hour`。**对上了，模型才可信。**
3. **搜索（60 秒）**：`python3 factory.py level.json --time 60`。
4. **照着输出去游戏里设置**，点 Test，拿游戏的分数和模拟分数对账。

## 规则

| 来源 | 规则 |
|---|---|
| 截图 | 原料厂每小时供应 N 件，每件付 `x$` 单价；加工厂可以是 2 小时一批（“20 / 1 of 2hrs”）；产线是一张 DAG，终端卖产品 |
| 截图 | 可以测试多次（Tested Factories），可以从任意一次测试接着改（Edit from Test N），成绩取最好的一次 |
| Chi | 三种 Buff：原料减半、产量翻倍、2 小时变 1 小时。产量翻倍按件收费，而且产出的每一件都收 |
| Chi | 下游开始生产的时间比上游晚：一条链是错开启动的（第 x、x+1、x+2 小时……） |
| 网上（csvoprep，可信度低） | 零件超出存储就浪费；Buff 可以翻倍产量或者降低需求量，但更贵，要算回报 |
| 网上（小红书帖子） | 界面会直接告诉你每种产品的成本和售价；**很多产品是亏钱的**，先只做赚钱的 |

### 待确认（在 `factory.py` 里都是开关，默认值用的是 Chi 心得里最说得通的读法）

1. **整批还是零碎**：材料凑不齐一整批时，是整批等着（`--batch all`，默认），还是能做多少做多少（`--batch partial`）？
   Chi 的第 4 条技巧“多设一点，但批次变少”说明是整批等。
2. **同一小时能不能接力**：上游这一小时的产出，下游是这一小时就能用，还是下一小时才能用（默认）？
3. **Buff 怎么收费**：三种 Buff 分别是按件收费还是一次性收费，价格多少？“2h 变 1h，二十几元”听起来像是一次性收费。
4. **每个节点的产量上限**是多少？默认 50；“拉到 100”指的是开了产量翻倍之后吗？
5. **初始资金**是多少？最后的分数是现金余额，还是利润？
6. **一个零件供给多个下游**时，按什么顺序分？默认按 json 里下游节点的顺序。
7. **仓库有没有上限**？网上有“超出存储就浪费”的说法。

## Chi 的 151k 心得，以及它在模型里对应什么

1. **先保基础产量，从终端倒推**：`backward_fill()` 就是这一步。终端先开到上限，上游按下游需求逐级填，哪里超了上限就压低终端。Chi 说这一步能拿到 100k–110k。
2. **Buff**：
   - a. **原料减半**是主力，用来突破中间环节的产能瓶颈、多卖终端产品，不是用来省原料钱的，因为 Buff 本身也要钱。
   - b. **产量翻倍**要慎用：它按件收费，本来不收钱的那部分产量也开始收钱了。只有当这条产线能拉满、而且产出都能被下游用掉时才划算。
   - c. **2h 变 1h**：二十几元，基本稳赚。

   搜索会逐个节点试开和关，按模拟出的分数决定取舍。
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
