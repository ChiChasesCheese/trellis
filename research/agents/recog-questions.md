# Recognition questions for the algorithm deck — writer's brief

You write **one pattern-recognition question per LeetCode problem** for Chi's deck `2 算法模式识别`. Chi's gap is seeing
which technique a problem calls for. The card's front is your question; its back shows your answer and `why`, then the
problem's full solution card (added by the importer, not by you). The question must be answerable only by someone who
sees the right approach, and the wrong options must teach something when he falls for them.

## Your chunk

- Input: `sources/local/quiz/recog-todo-2026-11-21-NN.md` (NN is given in your task). One entry per problem:
  `topic`, 题目 (title ｜ what it asks), 所在叶子 (the technique leaf: **never** copy it into the question), 解法要点 (the
  accepted solution in one sentence: the correct option must agree with it).
- Output: four files, 25 problems each, in the input's order (the last file takes what is left):
  `sources/local/quiz/recog-bulk-NN.part1.json` … `part4.json`. Each is a JSON array.
- After writing each part run `uv run python scripts/daily_quiz.py lint <part file> --set recog` and fix it until it
  prints `N questions pass the lint`. Nothing else is run: no import, no Anki, no git, no web, no subagents.
- **Resume rule:** a part file that exists and passes the lint is done; skip it.
- **Question by question.** Read each problem and think about what a learner would wrongly reach for. Do not write a
  script or template that generates questions; a batch produced that way is rejected.

## One question

```json
{"topic": "leetcode-tree::subarray-sums-divisible-by-k",
 "title": "LC 974 和可被 K 整除的子数组",
 "statement": "整数数组（含负数）和 k，数有多少个非空连续子数组的和能被 k 整除。",
 "question": "该用哪种思路？",
 "point": "同余的前缀配对",
 "options": ["前缀和取模，哈希表数相同余数", "滑动窗口，和超过 k 的倍数就收缩", "排序后相向双指针找和为 k", "哈希表存每个数，查 k - x 是否出现"],
 "correct": 0,
 "why": "子数组和 = 两个前缀和之差，差能被 k 整除等价于两个前缀余数相同。有负数，滑窗不成立。"}
```

Sixty finished examples: `sources/local/quiz/recog-2026-11-21.json`. Read ten of them before you start.

- `topic`: copy it from the entry. `title`: `LC <number> <name>` as in the entry (at most 44 characters).
- `statement`: what the problem asks, one or two lines, at most 100 characters, plain Chinese with English terms left
  in English. Keep every property a solver needs to choose the approach (negative numbers, sorted input, duplicates,
  "O(1) space", "one pass", n up to 10⁵). It must not name the technique.
- `question`: 「该用哪种思路？」 by default; 「最直接的判断是什么？」 for an insight problem; a multi-select
  「需要哪几样配合？」 when the solution is a combination of two or three basic moves (then `correct` is a list of 2 or 3
  indexes and there are 4 or 5 options).
- `options`: 3 or 4 concrete approaches, each at most 34 characters, the correct one first (`"correct": 0`; the
  importer shuffles). Say what is done, not just a name: 「按开始时间排序，小根堆存各房间结束时间」, not 「堆」.
- `why`: at most 90 characters. The signal in the statement that points to the right approach, then what breaks the
  most tempting wrong option, with a tiny counter-example where one exists (`[2,1,1,2]`, `([)]`).
- `point`: the transferable lesson in at most 16 characters (「越短越合法的滑窗」, 「关系会传递用并查集」).

## The rules that decide whether a question is accepted

1. **Every wrong option is actually wrong for this problem.** It answers a different question, breaks on a property in
   the statement, or violates a constraint written in the statement. If your distractor is only "slower", write the
   size limit that rules it out into the statement, and only a limit the real problem has. If you are not sure the
   real problem has it, use a distractor that is wrong for a structural reason instead. Never invent a requirement
   (a complexity bound, a memory rule, "one pass") to make a valid alternative wrong.
2. **Never list a second valid solution as wrong.** Many problems have two textbook solutions (heap or sweep line,
   BFS or DFS, sort or counting, DP or combinatorics, union-find or graph search). Leave the alternative out, or put
   both into the correct option (「带权并查集或建图搜路径」).
3. **Wrong options are what a learner would really try**: the neighbouring pattern (fixed window for a variable one,
   greedy where DP is needed, per-level sums on a tree DP, counters for bracket matching), not filler. 「二分答案再验证」
   or 「排序后双指针」 may appear only where someone would plausibly think of it.
4. **Length must not give the answer away.** In a file the correct option may be the longest in at most 40% of the
   questions, and it is never more than 1.25 times the longest wrong option; no option is more than 2.5 times the
   shortest. Give the wrong options the same level of detail as the right one.
5. **The pattern never appears on the front.** Not in the title beyond the problem's own name, not in the statement,
   not as a hint in the question.
6. **Agree with 解法要点.** If you believe the entry's solution is wrong or you do not know the problem well enough to
   judge the distractors, still write your best question and list it in your report.
7. Design problems (LRU, hash map, iterator…): ask for the core structure, and put the complexity requirement that
   decides it into the statement.
8. No "all / none of the above", no joke options, no Markdown, no code blocks; inline symbols like `dp[i]`, `O(n)` are fine.

## Fixing after a lint failure

Edit the one question the lint names, by hand, and read the whole question again afterwards. Do not patch options with
a script that addresses questions by position: in one chunk such a script shifted the option lists of nine questions
onto their neighbours, and the lint cannot see that the options no longer belong to the problem.

## Report (your final message, nothing else)

- Parts written and the lint line of each.
- Up to 12 questions you are least sure of: `LC <n>` and one sentence on the doubt (a distractor that may be valid, a
  solution you could not verify, a statement you had to guess a constraint for).

A second agent then verifies and repairs the chunk: `research/agents/recog-verify.md`. The orchestrator checks it with
`scripts/recog_review.py NN`, reads the change list and a sample, and imports the chunks in order.
