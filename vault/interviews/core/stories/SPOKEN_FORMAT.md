# 故事口述格式（所有公司 kit 的故事文件都用这个）

Chi 的要求（2026-10-15）：「确保 stories 是口述清楚的正常顺序 / bulletpoint 着重关键词」。

故事是要**说出口**的。说的时候，眼睛扫一下就能接着往下讲，所以：

## 1. 口述提纲替代大段文字

每个故事的「60–90 秒版」和「2 分钟版」都改成 **按时间顺序的 bullet 提纲**，英文（面试时说英文），固定 5 段：

```markdown
### 60–90 秒（口述提纲）

**S · Situation**
- One line of context: **team / system**, **scale number**.

**T · Task**
- What **I** owned (not "we"), and **why it mattered** (money / customers / risk).

**A · Action** (in the order it happened)
1. **First thing I did** — the one reason why.
2. **Second thing** — ...
3. **Decision / pushback** — who, what I said, the **data** I used.

**R · Result**
- **Number**, **number**, **what changed** for customers / the team.

**L · Learning / Mechanism**
- The **rule or mechanism** I left behind (senior signal).
```

规则：
- **顺序 = 事情发生的顺序**。Action 是编号列表，不跳回去补叙。原稿顺序乱的，按 `core/stories/` 源文件里的时间线重排。
- **每条 bullet 是一句能直接说出口的短句**，≤ 20 个英文词；不写成段落。
- **关键词加粗**：数字和量级、技术名词、动词（*built / found / pushed back / removed*）、与 LP 对应的那个词（*ownership, dive deep, data*）。每条 1–3 个加粗，不要整句加粗。
- 一句话钩子（hook）放在提纲最前面，单独一行加粗：开口第一句就是它。
- 2 分钟版用同样的 5 段，只是 Action 更细（4–7 步）、Result 多一两个数字、加一条「What I'd do differently」。

## 2. 逐字稿降级为参考

原来的英文段落逐字稿**保留**，但放进折叠块，放在提纲下面：

```markdown
<details><summary>逐字稿（参考，不背）</summary>

...原段落...

</details>
```

逐字稿也要按同样的时间顺序；顺序和提纲不一致的，改逐字稿。

## 3. 其余小节

数字表、LP 换角度表、追问、证据边界、Senior 升级点、【待 Chi 补】都保留原样，不删不改内容；只有追问的「答案要点」也改成加粗关键词的短 bullet。

## 4. 不许做的事

- 不加原文件和 `core/stories/` 里没有的事实或数字；缺的继续写【待 Chi 补：…】。
- 不改故事的结论、不改「哪部分是我的 / 哪部分是队友的」的证据边界。
