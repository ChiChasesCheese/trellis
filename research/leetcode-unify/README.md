# LeetCode: one tree, one card per problem, everything else is a tag

Chi, 2026-11-14:

> 「所有的卡就是具体的每一个题目都是有唯一的一张卡……想集中看 Amazon 的题，我们就全都去 Amazon 这个 tag，然后想看具体某个知识点，我们就去知识树的叶子里」

## Layers

1. **Body.** Each problem has one answer body, `vault/interviews/core/leetcode/problems/<slug>.md`, in the short card
   shape of research/leetcode-daily/AGENT.md. It is the only place content is written. 同模式 links a problem to its
   related problems, whose code the card expands.
2. **Tree.** The 0x3F knowledge tree (`scripts/lc_tree.py`, domain `leetcode-tree`, deck 算法知识树（灵神题单）) is the
   only deck that holds problem cards. Every body has exactly one card there, `lct-<slug>`, on one leaf:
   - a problem on one of 0x3F's lists lands on the leaf he gave it;
   - any other problem is placed by us (PLACEMENT.md) through `sources/local/lc/expand.json`, on one of his leaves or on
     a leaf of ours (`sources/local/lc/our_leaves.json`, ids `<parent>.our-<slug>`).
   The leaf's learning card (`lct-learn-*`) comes first.
3. **Tags** (`scripts/lc_tags.py --apply`), all on the one card:
   - `榜单::Top_Interview_150`, `榜单::Blind_75`, `榜单::NeetCode_150`, `榜单::Hot_100`;
   - `榜单::LeetCode_Tops`, which is those lists plus the company-frequency 80/20 selection;
   - `榜单::TikTok_近半年`;
   - `公司::<Company>`, from the public company-wise lists, plus `sources/local/lc/company_extra.json` for companies we
     researched ourselves, e.g. Cerebras;
   - `已做过` for problems solved on LeetCode, and `必读` for today's must-read (`scripts/lc_mustread.py`).
4. **Views.** A view is the cards of one tag:
   - in Anki, search the tag, or build a filtered deck on the phone with `tag:公司::Amazon`;
   - as a sprint deck, run `scripts/lc_view.py <tag> -o plan.json` and then `scripts/company_deck.py`, which borrows the
     cards and gives them back to the tree on `release`. Example: `7 Cerebras 力扣`.
   - The daily deck 今日算法 deals new problems from the tree (`scripts/daily_extra.py`).

## Retired (2026-11-14)

- **Decks.** The per-problem copies in LeetCode Tops 01–17, 24 TikTok whole answers, 27 通用核心, 28 Daily, 00 必读, and
  the Amazon `lca-` / `lcb-` cards of problems we have bodies for.
  - `research/leetcode-unify/migrate.py` moved each copy's best progress and all its review history onto the tree card.
  - It suspended the copies and moved them to `📦 其他::待删除 · 旧 LeetCode 副本` for Chi to delete.
- **Skeletons.** leetcode-tops, tiktok-core, leetcode-daily and leetcode-mustread carry `anki_via: leetcode-tree`, so
  anki-push and anki_refresh refuse them.
  - leetcode-daily.yaml stays as the ledger of solved problems.
  - leetcode-tops' `selection.json` stays as the input of the `榜单::LeetCode_Tops` tag.
- **Kept.** The pattern cards, Python cards and TikTok custom cards in deck 24 are not copies of a problem, so they stay.
  Amazon cards with no body stay too: they are problems we have not written yet.
