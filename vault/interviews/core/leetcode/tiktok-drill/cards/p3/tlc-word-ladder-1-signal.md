---
id: tlc-word-ladder-1-signal
node: p3.word-ladder
type: qa
step: 1
---
## Q
**LC 127 单词接龙**｜Hard · LC TikTok 热度 62/100 · 近一年被问：美国 2 次、国内 1 次 · CodeTop 国内累计 6 次 · 最近 2026-10-25（美国面试记录）

字典 `wordList` 中从 `beginWord` 到 `endWord` 的**转换序列**是一个序列 `beginWord -> s1 -> s2 -> ... -> sk`：相邻两个单词只差一个字母；每个 `si`（`1 <= i <= k`）都在 `wordList` 中（`beginWord` 不需要在字典里）；`sk == endWord`。给 `beginWord`、`endWord` 和 `wordList`，返回从 `beginWord` 到 `endWord` 的**最短转换序列中的单词数目**；不存在则返回 `0`。

约束：`1 <= beginWord.length <= 10`，`endWord.length == beginWord.length`，`1 <= wordList.length <= 5000`，`wordList[i].length == beginWord.length`，所有单词由小写英文字母组成，`beginWord != endWord`，`wordList` 中的字符串互不相同。

例：`beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]` → `5`（`hit -> hot -> dot -> dog -> cog`）；去掉 `"cog"` 后 → `0`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「每次只能改变一个字母」「最少转换步数」→ 状态之间有统一代价为 1 的转移 → **隐式图的 BFS 最短路**（单词是顶点，差一位为边）。
- 「最短序列」要求单词个数 → BFS 层数 + 1（起点计入）；「`endWord` 不在字典则无解」是一个直接的剪枝。
- `N = 5000`、`L = 10`：显式两两比较建图 `O(N²·L)` 约 `2.5·10^8`，太重 → 用「逐位替换 + 集合查询」生成邻居。

**推导链。**
1. 暴力：DFS 枚举所有转换序列取最短，指数级，且 DFS 不保证先找到最短。
2. 建图：两两比较所有单词是否差一位，再 BFS；`O(N²·L)`，约 `2.5·10^8`。
3. 洞察：邻居不必预先建图——对当前单词逐位替换 26 个字母，用集合判断是否在字典，`O(26·L²)` 每个单词；入队时从集合删除，保证每个单词只入队一次。
4. 最优：单向 BFS `O(N·L²·26)`；再加双向 BFS 能大幅减小搜索量。

**同模式的题**：LC 126 单词接龙 II、LC 433 最小基因变化、LC 752 打开转盘锁、LC 773 滑动谜题、LC 1091 二进制矩阵中的最短路径。
