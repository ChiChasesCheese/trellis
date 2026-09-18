# 00 · Chakra AI 语音筛（20 min）

这一轮的材料全部在 `../../loop/rounds/00_ai_screen/`（入口 `README.md`），这里只给阅读顺序：

1. `../../../../core/playbooks/ai-voice-screen.md` —— 机制：Reporter 只读 transcript；3/2/1/0 打分；theoretical = Not Met；没说到 = 0。
2. `../../loop/rounds/00_ai_screen/playbook.md` —— 逐分钟剧本 + 英文自我介绍、危险追问、收尾；故事全文在 `stories.md`（S1–S10 + 追问版）。
3. `../../loop/rounds/00_ai_screen/scenarios.md` —— 12 个场景题全文；题库 `questions.md`（79 题），抽题 `python3 loop/mock.py bq ai -n 5`。
4. `../../../07-mock.md` —— 20 分钟计时自测 + 录音回听清单。
5. `../../loop/rounds/00_ai_screen/CARD.md` —— 关键词卡，考前贴摄像头旁；自评标准 `rubric.md`。

一句话：**每个回答 headline → mechanism → "I decided" → 量级 → learning，首答 60–90 秒，每答命中两条 JD 线（SQL · distributed systems · Java · database internals · large-scale production）。**
