# Recognition questions — verifier's brief

A writer produced one chunk of pattern-recognition questions (rules: `research/agents/recog-questions.md`, read it
first). You are the second reader. Assume some questions are flawed and find them; then repair them in place.

## Your chunk

- Questions: `sources/local/quiz/recog-bulk-NN.part1.json` … `part4.json` (NN is given in your task).
- The problems: `sources/local/quiz/recog-todo-2026-11-21-NN.md` (题目, 所在叶子, 解法要点).

## Check every question, one by one

1. **Is the correct option right**, and does it agree with 解法要点? (If the entry's solution itself looks wrong, do not
   change the answer; report it.)
2. **Is any wrong option actually a valid solution** under the statement as written? Think of the standard alternatives
   (heap vs sweep line, BFS vs DFS, sort vs counting, DP vs formula, hash set vs two pointers, union-find vs graph
   search, binary search vs linear scan when nothing forbids it). A slower solution counts as valid unless the
   statement carries a constraint that rules it out.
3. **Does the statement invent a requirement** the real LeetCode problem does not have (a complexity bound, a memory
   rule, "one pass") only to make a valid alternative wrong? Size limits the real problem has are fine; if you are not
   sure the real problem has the limit, treat it as invented.
4. **Does the front give the technique away** (statement or question names the pattern or the leaf)?
5. **Is `why` true?** Work every counter-example by hand or with `python3 -c` (e.g. does greedy really fail on
   `[2,5,0,0,1]`?). A wrong counter-example is replaced by one you have checked.
6. Is a wrong option a throwaway nobody would try (「二分答案再验证」 on a tree problem)? Replace it with the pattern a
   learner would really confuse this problem with.

## Repair

Edit the part file with the smallest change that fixes the flaw:

- valid alternative listed as wrong → replace that option with an approach that is wrong for a structural reason;
- invented requirement → remove it from the statement and replace the distractor that depended on it;
- wrong `why` or counter-example → rewrite it (at most 90 characters);
- leak → reword the statement.

Keep `topic`, `title` and `question` unchanged (the importer identifies a question by them), keep the correct option
first, and keep the length rules (run `uv run python scripts/daily_quiz.py lint <part file> --set recog` after your
edits; every part must still pass). Do not rewrite questions that are fine. No import, no Anki, no git, no web, no
subagents.

## Report (your final message, nothing else)

- How many questions you checked and how many you changed.
- One line per change: `LC <n>`: what was wrong → what you changed.
- Questions you could not settle (you suspect a flaw but are not sure), one line each.
- The lint line of each part after your edits.
