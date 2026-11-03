# 低层设计（LLD）：从这里开始

这是一份可以直接执行的 LLD 学习计划：照着做，不用每天决定学什么。7 个阶段，约 8 周，每周 8 小时左右，42 道限时写代码的题，全部用 Python。

**今天做什么**：在本目录下运行 `python3 drill.py today`。

## 地图

| 想做什么 | 去哪 |
|---|---|
| 看全部阶段、目标和验收标准 | [[00-roadmap\|学习路线]] |
| 看自己做到哪了 | `python3 drill.py status`，然后打开 `PROGRESS.md` |
| 一次练习具体怎么做、怎么复盘 | [[02-how-to-practise\|怎么练]] |
| 判断自己是否准备好了 | [[03-readiness-checklist\|验收清单]] |
| 概念讲解和全部 59 道题 | [[低层设计（LLD） MOC]] |
| Amazon 的 OOD 轮 | [[ood-index]] |

## 命令

在本目录下运行：

```bash
python3 drill.py today                  # 下一步做什么
python3 drill.py start parking-lot -m 60   # 打印分关题面，复制 starter，开始计时
python3 drill.py test parking-lot       # 跑测试；-k part1 只跑某一关（部分老题没有分关标记）
python3 drill.py time parking-lot       # 还剩多少时间
python3 drill.py solution parking-lot   # 做完才看：题解在哪
python3 drill.py done s1-read           # 勾掉阅读任务
python3 drill.py status                 # 更新进度看板
python3 drill.py list                   # 全部题目和状态
```

你写的代码在 `work/<题名>/starter.py`，测试全绿后这个任务会自动勾掉。`work/`、`progress.jsonl`、`PROGRESS.md` 是个人进度，不进 git。

## 三份材料怎么配合

- **这里**：动手。限时写代码，跑测试。
- **牌组 `低层设计（LLD）`**：概念和 59 道题的知识点，每天复习。
- **课程牌组（子牌组 `01 高频真题`、`02 TikTok 高频设计题`、`04 低层设计`）**：课程每章的摘要、考点和拓展，以及高频真题的完整解答。

做错之后，先回对应阶段列出的卡片，再隔天重写，而不是接着刷新题。
