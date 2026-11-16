# Tap interactions for coding and design cards on AnkiMobile

Research date: 2026-11-16. Scope: what the Anki community and adjacent tools do for tap-only interaction and testing, what learning science says about the formats, and which interactions are worth adding to `scripts/quick_deck.py` (formats today: single choice, multi-select with 确定, tap-to-order, match, tap-the-wrong-line, cloze, flash Q&A).

How to read the evidence. "Works on AnkiMobile" below means one of three things: (a) the source says so, (b) the source is plain HTML/JS with no add-on and uses the same mechanisms our deck already ships (class `tappable`, `onclick`, `sessionStorage`, the unofficial `ankitap` message), or (c) my inference from those mechanisms. Nothing here was run on a device by me. Where a claim is secondhand or I could not open the page, it says so.

## 1. What the AnkiMobile platform lets a template do (the constraints every idea inherits)

- **Tap behaviour.** The AnkiMobile manual's JavaScript section says an element must carry class `tappable` (AnkiMobile 2.0.39+) for taps to reach it instead of triggering the tap-zone action, which is "show answer" by default. Our deck already does this (class plus `onclick`, children with `pointer-events:none`). Forum threads confirm the same fix for hint buttons and checkboxes: https://forums.ankiweb.net/t/hint-fileds-buttons-not-working-on-ankimoblie/21347 and https://forums.ankiweb.net/t/tapping-on-a-choice-not-being-registered-on-ankimobile/21991 (both older than 2024, still the reference answers). A 2025-05-04 thread shows the failure mode when it is missing: tapping option text flips the card, https://forums.ankiweb.net/t/adjust-multiple-choice-behaviour-to-be-the-same-as-desktop/60290.
- **No script API to show the answer.** Dae (Anki's maintainer) wrote on 2023-06-19 that AnkiMobile has no built-in user JavaScript actions, so hint-reveal or one-by-one scripts live in the template: https://forums.ankiweb.net/t/hint-reveal-and-cloze-one-by-one-for-mobile-gamepad/31295/2. The community workaround for auto-flip is the private `ankitap` message that simulates a tap in a chosen zone. It is documented in a 2024-12-07 forum template (Clozemaster-style game, tap zone must be mapped to Show Answer, "has broken before") https://forums.ankiweb.net/t/randomized-multiple-choice-cloze-tests-similar-to-clozemaster-for-anki-desktop-and-mobile-experimental-card-template-mini-game/52843 and in Cloze Interactive v1.5.0 (2026-10-19), which says "relies on AnkiMobile's private API and may break in future updates" and makes the zone configurable: https://github.com/huandney/Anki-Cloze-Interactive. Our `flip()` is the same mechanism with a fall back to a normal tap, which is the right hedge. One improvement worth copying: make the zone name a config value, not a constant.
- **Front to back state.** Two proven routes: `sessionStorage` (the Memrise template by Eltaurus-Lt moved to it so MC cards work on AnkiMobile, https://github.com/Eltaurus-Lt/Anki-Card-Templates, v5.2 2026-07-07; the Clozemaster-style template above; ours) and the small library anki-persistence (https://github.com/SimonLammer/anki-persistence, last push 2023-01-27, README shows front and back screenshots on iOS). Our `keep()` also writes `window._qk`, which covers clients that reuse one page. No change needed.
- **Fragile spots reported in 2025 threads.** `DOMContentLoaded` may never fire on AnkiMobile and `onUpdateHook` may not be called (thread dated 2025-03-15, https://forums.ankiweb.net/t/javascript-code-compatibility-issue-with-ankimobile-on-ios/57299); `position:fixed` scrolls with content on iOS; there is no console (Eruda did not show on iPad in that thread). Our scripts run inline immediately and avoid fixed positioning, so we are on the safe side. Keep it so for every new format.
- **Drag and drop is the wrong primitive on a phone.** The ikkz Ordering, Item Ordering and Match templates are drag-and-drop and their docs tell the user to disable Anki's swipe gestures (https://anki.ikkz.fun/templates/classic/ordering and /match; the pages mention AnkiDroid only, nothing on AnkiMobile). Swipes and drags compete in AnkiMobile; tap-only avoids the conflict.

## 2. Survey of community templates and tools (newest first)

| Idea | What it is | Source and date | AnkiMobile without add-ons | Ten-second test of coding or design knowledge |
|---|---|---|---|---|
| Ordering with up/down buttons | JSON `Items` field in correct order; front shuffles, you move items with up and down controls; back marks each position right or wrong | DamianZaremba/anki-ordering, created 2026-07-26, pushed 2026-11-15, https://github.com/DamianZaremba/anki-ordering | Plain JS, so likely yes, but README claims no platform list; I did not test. Moving by buttons costs about n²/2 taps for n items | Process order, but slower than our tap-in-sequence (n-1 taps). Not worth adopting; the back-side "each position marked" idea we already have |
| Checkbox multi-answer MCQ | `Answers` JSON of text and correct; tick all you believe correct; back shows correct, wrong, missed | DamianZaremba/anki-multiple-choice, 2026-07-26 to 2026-11-15, https://github.com/DamianZaremba/anki-multiple-choice | Plain JS; likely | "Missed" versus "wrong" distinction is the useful bit (also in anki-boi below) |
| Drag-and-drop template | Up to 10 pairs, drag onto targets | DamianZaremba/anki-drag-and-drop, created 2026-06-09, https://github.com/DamianZaremba/anki-drag-and-drop | Drag conflicts with swipes; avoid | Same as our match, slower to operate |
| AnkiEco classic templates 3.0 | MCQ, True/False, Match, Ordering, Item Ordering, Cloze, Native Cloze, Input; packager CLI that builds .apkg from template sources | ikkz/anki-eco, pushed 2026-09-12, 121 stars, https://github.com/ikkz/anki-eco and https://anki.ikkz.fun/templates/classic/ | Docs name AnkiDroid only; AnkiMobile unconfirmed | The packaging idea (templates as source, `.apkg` out) matches what `quick_deck.py push` already does |
| True MCQ note template | Click-to-commit multiple choice, shuffles every review, multi-answer, a selection cap equal to the number of right answers, back says Correct, Wrong or Missed; its PROBLEMS.md argues recognition under exam conditions is the right tool when the exam is recognition | anki-boi/True-Anki-MCQ-Note-Template, pushed 2026-10-22, https://github.com/anki-boi/True-Anki-MCQ-Note-Template | README says it works on AnkiMobile | Missed-versus-wrong feedback; "pick exactly k" cap (a hint that leaks the count, not the identity). Our multi-select could print "选 2 个" |
| Kprim and single/multiple choice | Kprim = four statements, each judged true or false; add-on only for creating notes, cards review on all clients | zjosua/anki-mc, pushed 2025-10-06, https://github.com/zjosua/anki-mc | README: "can be reviewed with all Computer and mobile apps and on AnkiWeb" | Four taps, one per statement. Forces a judgement on every option, which "pick all right ones" does not |
| Statement MCQ | Up to eight terms on the front, each with two buttons, green or red marking, shuffled | Forum template, posted 2024-12-12, https://forums.ankiweb.net/t/new-mcq-card-template/53086 | AnkiMobile not mentioned; no persistence; hard-coded eight terms | Same idea as Kprim, one tap per statement |
| MC library with random distractors | Choices field, first line is correct, other choices drawn at random from a longer list on every review; template 1 flips on tap (needs "show answer on tap" on AnkiMobile), template 2 does not flip | ale18V/Anki-Multiple-Choice, last push 2024-07-12, https://github.com/ale18V/Anki-Multiple-Choice | README documents the AnkiMobile setting | A bank of 5 to 6 plausible wrong options per point, 2 or 3 shown each time, gives variation without new notes. Needs per-review state; sessionStorage as above |
| MC suite | Several MC templates; muctebanesiri adds RTL; Eltaurus-Lt's Memrise template adds generated choices via a desktop add-on | muctebanesiri/anki-multiple-choice-question-template (2025-09-26, https://github.com/muctebanesiri/anki-multiple-choice-question-template); oscar-labit/Anki-MCQ (2025-11-23, https://github.com/oscar-labit/Anki-MCQ; README says desktop and AnkiDroid, so no iOS claim); mikael-myc/anki-multiple-choice-notes (2025-11-02) | Mixed; many do not claim iOS | Nothing we lack |
| Staged cloze reveal | Tap a cloze to reveal it; swipe gestures via User Actions; optional auto-flip after the last; highlights the next cloze | huandney/Anki-Cloze-Interactive v1.5.0, 2026-10-19, GPL-3.0, "tested on AnkiMobile 25.09", https://github.com/huandney/Anki-Cloze-Interactive | Yes: clozes carry `tappable`. One-by-one on iOS failed in a 2025-01-13 forum thread (all clozes revealed at once) until `tappable` is set correctly: https://forums.ankiweb.net/t/ankimobile-one-by-one-cloze-reveal/54301 | Chains of 3 to 4 items, each tap a self-check. About 8 to 12 seconds |
| Clozolkor | Reveals several clozes one by one, auto-flips if none has a hint | thiswillbeyourgithub/Clozolkor, 2025-12-15, https://github.com/thiswillbeyourgithub/Clozolkor | Not checked | Same as above |
| Cloze Anything | Template trick that turns `((c1::text))` in any note type into a cloze, with hints | matthayes/anki_cloze_anything, 2026-04-13, https://github.com/matthayes/anki_cloze_anything | Pure template; yes | Lets one note type hold code cloze without the desktop cloze editor; our generator already writes `{{c1::}}` directly |
| Cloze Overlapper | Add-on that turns an ordered list into overlapping clozes (hide item k, show a few neighbours) | glutanimate/cloze-overlapper, last push 2021-12-30, https://github.com/glutanimate/cloze-overlapper | The add-on is only needed to make the notes; the result is ordinary cloze cards, so AnkiMobile is fine. The add-on itself is stale | Ordered lists longer than four: "what comes after X". Our generator can emit the same overlapping clozes without the add-on |
| Anki Persistence | Library that stores a value on the front and reads it on the back, with an `isAvailable()` check | SimonLammer/anki-persistence, 2023-01-27, https://github.com/SimonLammer/anki-persistence | README shows iOS front and back | What we already do with `sessionStorage` |
| Closet for Anki | Add-on framework for building interactive templates (cloze show/hide/reveal helpers); later versions dropped the persistence dependency | https://forums.ankiweb.net/t/closet-for-anki-official-support/4560 (old thread, I did not date it; not checked for current Anki versions) | Needs the add-on for authoring only; treat as stale | Not needed |
| Image occlusion | Built into Anki from 23.10; AnkiMobile reviews it and recent versions can create it (secondhand: 2026 blog posts and https://mandarinmosaic.com/blog/image-occlusion-anki; older forum threads say the opposite, so check on his version) | Anki manual and the forum threads above | Native note type, no add-on | "Which box is the rate limiter, which is the queue": one mask per card. Good for architecture diagrams; low value for pure code |
| AnKing note types | Cloze and image-occlusion note types with collapsible hints and tag-driven styling | AnKing-VIP/AnKing-Note-Types, 2026-06-08, https://github.com/AnKing-VIP/AnKing-Note-Types | Yes, they are designed for AnkiMobile | Hints are static; no tap interaction we lack |
| Type-in answer | Anki's own `{{type:Field}}` | Anki manual | Typing is what Chi wants to avoid; also AnkiMobile has reported script problems on type cards | Skip |
| Parsons-style code ordering for Anki | I searched GitHub (`anki parsons`, `anki ordering`, `anki sequence`) and the forum and found no Parsons template for Anki. The nearest are the ordering templates above | search, 2026-11-16 | n/a | Our `order` format with a distractor line would be new to the Anki ecosystem |

Not found: a community Anki template for confidence marking, for ranking with partial credit, or for fill-the-blank-from-a-word-bank (the Clozemaster-style template above is the closest, but it picks a random word, not a code token).

## 3. Adjacent apps

- **Duolingo-style word bank and tap-to-arrange.** Tap a word tile and it jumps into the answer area; tap it again to send it back. Cambridge One documents the two variants for gap fill, single tap fills the first open gap (older), or tap the word and then tap the blank (newer): https://cambridgeonehelp.cambridge.org/hc/en-gb/articles/33718091394834-How-word-selection-activities-work. Sublearn's sentence builder is tap-to-add, tap a placed tile to remove it, https://sublearn.com/help/guides/sentence-builder. This is exactly our `order` mechanic, so the format is established; the word-bank fill-in is the one we lack.
- **Parsons problems (drag code lines into order) are the research form of this.** The ITiCSE 2023 working group report says they typically beat fix-code and write-code exercises on learning efficiency while lowering cognitive load, and that distractor lines help students learn to recognise and avoid common errors; it also says the benefit is not universal (some prefer writing code): https://falmouth-test.eprints-hosting.org/5216/1/ITiCSE_2023_WorkingGroup_Parsons_Report.pdf (secondhand through a search snippet; the PDF host did not open for me). A faded-Parsons pilot (blanks inside the supplied lines) rated harder than plain Parsons and easier than writing: https://escholarship.org/content/qt8794g5s0/qt8794g5s0.pdf. Proof Blocks, the same idea for proofs, https://arxiv.org/pdf/2211.09609. Brilliant uses drag-and-drop block programming in some lessons, but I could not confirm its question types, so I do not rely on it.
- **Execute Program.** Per Matuschak's notes from a 2020 conversation with its author, every prompt is answered by executing code ("doesn't have non-executable prompts"), reviews use few levels, and a failed review halves the level: https://notes.andymatuschak.org/Execute_Program, https://www.executeprogram.com/spaced-repetition (the page itself returned only a title to my fetcher). The lesson for us: it never asks a recognition question for code; the tap formats should therefore stay on judgement and structure (order, fault, fill a token), and recall of whole snippets stays in the main deck.
- **Mochi and RemNote.** I found nothing about tap-based ordering or choice interactions in either. Mochi templates are Markdown fields (https://mochi.cards/docs/templates/intro-to-templates/); nothing to borrow.

## 4. Learning science and expert advice, as it bears on the choice of format

- **Atomic prompts.** Matuschak (2020-12, https://andymatuschak.org/prompts/): prompts should be focused ("one detail at a time") and tractable (answerable almost always, "often means breaking the task down, or adding cues"); "procedures are lists", and for procedures ask for the important verbs and when to move between them; a list kept in a fixed order is learned by its "visual shape"; unordered lists are hard to turn into prompts; yes/no or this/that prompts "tend to require little effort and produce shallow understanding"; cloze is prone to pattern matching. His note on atomic units, https://notes.andymatuschak.org/zFgK9ArxAXq57iMukRsVVE9, adds Nielsen's argument that a failed compound prompt does not show where the gap is.
- **Nielsen** (Augmenting Long-term Memory 2018, https://augmentingcognition.com/ltm.html; and the mathematics essay https://cognitivemedium.com/srs-mathematics): make question and answer as atomic as possible, split compound cards, ask for the minimal answer, restate each idea several ways. I read the second essay; the first only through summaries.
- **Wozniak** (20 rules, 1999; current wiki copy last edited 2026-07-22, https://supermemo.guru/wiki/20_rules_of_knowledge_formulation): avoid lists, sets and enumerations, or turn them into cloze; use redundancy (the same fact from different angles). Together with Matuschak this is the case for ranking cards of at most four items and for chain cloze beyond that.
- **Multiple choice versus recall.** Little, Bjork, Bjork and Angello (Psychological Science, 2012-03, summary https://www.psychologicalscience.org/news/full-frontal-psychology/two-cheers-for-multiple-choice-tests.html) found that multiple-choice practice with competitive, plausible lures produced as much or more later learning than short-answer practice and slightly helped related untested items; implausible lures gave no benefit. Little and Bjork 2015 (Memory & Cognition, https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2017/01/LittleBjorkMC2014.pdf) say the same. The critics' standard objection is that recognition is easier and shallower than recall. Reading the two together: choose-formats are fine for a first pass if every wrong option is a near miss, and recall must follow. This is the rule already in the deck's memory (recognition formats first pass only, always with a recall card).
- **Confidence-based marking.** Gardner-Medwin's scheme (UCL): the student declares confidence before the answer is marked; a confident wrong answer costs more than an unsure one, so guessing stops paying: https://www.physoc.org/?p=55824. Evidence is mostly from its author; an independent 2019 trial found better course appreciation but no gain on the summative exam: https://bmcmededuc.biomedcentral.com/track/pdf/10.1186/s12909-019-1610-2. Sparck, Bjork and Bjork found confidence-weighted practice tests transferred better to new related questions than standard MC (reported in the Little and Bjork line of work, I did not open it). For us the grade buttons 1 to 4 already are a confidence report; the card can only make it honest (see recommendation 3).
- **Successive relearning.** Rawson and Dunlosky (Current Directions in Psychological Science, 2022, https://journals.sagepub.com/doi/full/10.1177/09637214221100484): retrieve to a criterion in each of several spaced sessions; after three sessions the initial criterion matters little. A 2023 critique notes comparisons often lack a restudy control: https://link.springer.com/article/10.1007/s10648-023-09809-2. This is what Anki's learning steps (1m 2h 6h) plus review already do, and it is the case for putting the same point into a different format on the second and third pass.

## 5. Recommendations, ranked by value

Ranking criterion: how much does the interaction add to what the deck already has, per hour of implementation, for coding and design points that must be judged in under ten seconds. All eight are plain HTML/JS on the existing helpers (`arm`, `free`, `keep`, `flip`, `SAVED`, `SHOW`), so none needs an add-on, and each stores its result in `sessionStorage` key `qk` like the current formats.

### 1. Rank-by-tap with partial credit (extend `order` into `rank`)

What changes. The `order` format already lets the user tap rows in sequence and shows the rank on a badge, and it auto-fills the last item. What it lacks for Chi's use is (a) a statement of what the rank means (do-first priority in a design, or step number in a process), (b) a score that is not all-or-nothing, and (c) a rule for when a rank card is allowed to exist.

- Rows stay in fixed positions (never re-sorted, so the eye does not lose them); a badge circle at the left shows the rank given; a tap on a ranked row clears it and every later rank (already how `order` works); the last row is filled automatically, so 4 items cost 3 taps.
- Score by displacement: sum of |given rank minus right rank|. 0 is right; 2 is one adjacent swap; 4 or more is wrong. Show the right rank in small type beside every row that is off. Print a grade hint in the existing `#grade` line: 0 and answered quickly, Easy; 0, Good; one adjacent swap, Hard; otherwise Again. The hint is advice only; Chi still taps 1 to 4.
- Optional `Ties` field (for example "23") for items whose order is interchangeable, so that a defensible answer is not marked wrong.
- Writing rule from Matuschak and Wozniak: at most four items, and the order must have a reason a reader can state in one line (a later step depends on an earlier decision, or a mistake early is more costly). Put the reason in `Why`. If the order is arguable, it is not a rank card; make it a Kprim or a choice.
- Variant for five items: anchor rank, tap only the first and the last; the middle is not scored. Two taps.

Example, design priority (限流器，先后考虑的顺序):

> **Q** 设计 API 限流器，按「先想清楚的」到「后想的」依次点 1、2、3、4。
> Rows shown shuffled: 「被拒绝时返回 429 + Retry-After」「限流维度：用户、IP 还是 API key」「多实例共享计数：Redis + Lua 保证原子」「算法：令牌桶或滑动窗口」
> **Solution** 1 限流维度 → 2 算法与参数（突发容量、速率）→ 3 多实例计数的原子性 → 4 被拒后的响应。
> **Why** 先定对谁限，才谈得上选算法；算法定了，才知道分布式计数要存什么；响应形式最后定，改动最便宜。
> **Ties** none. **Grade hint** 全对 Good，相邻两项互换 Hard，其余 Again。

Example, process order with the same mechanic (幂等键):

> **Q** 处理带 Idempotency-Key 的扣款请求，按执行顺序点 1、2、3、4。
> Rows: 「执行扣款并写入结果」「用键原子占位（INSERT … 已存在则读旧结果）」「校验请求体哈希与首次一致」「返回响应并把结果缓存到该键」
> **Solution** 1 原子占位 → 2 校验请求体哈希 → 3 执行扣款并写入结果 → 4 返回并缓存。
> **Why** 占位必须在执行前，否则两个并发请求都会扣款。

Cost: small. The ordering script, the grade line and the back-side re-rendering exist; add the displacement score and an optional Ties string. Sources: Matuschak "procedures are lists" (2020-12); Parsons-problem evidence (ITiCSE 2023); tap-to-arrange precedent in Duolingo-style apps.

### 2. Kprim true/false grid ("判断组")

What. Four statements about one point; each row has two small buttons, ✓ and ✗; one tap per row; the card grades itself after the fourth tap and shows the wrong rows with a one-line reason. It replaces the multi-select where unpicked rows are ambiguous (not judged, or judged false?).
Source. Kprim in zjosua/anki-mc (2025-10-06) and the 2024-12-12 forum statement template. Pure JS.
Why it is better than "pick all right ones": every option must be judged, wrong rows are individually diagnosable, and four near-miss statements are exactly the competitive lures Little and Bjork found useful. Roughly 8 seconds.
Design details: the tap targets are the two buttons in each row (class `tappable`, 44 pt high); a row cannot be un-answered after the fourth tap but can be changed before; write exactly two true and two false only if the content allows, otherwise vary (3-1, 1-3), so the count is not a hint.

Example (幂等键):

> **Q** 关于幂等键，判断四句。
> 1 键由客户端生成，服务端按键去重。 ✓
> 2 同一个键带了不同的请求体，应直接返回上次缓存的结果。 ✗（应报错：请求体与首次不一致）
> 3 必须在处理开始前原子占位，不能处理完再写。 ✓
> 4 键要永久保存，不需要过期时间。 ✗（需要 TTL，否则存储无限增长）

### 3. An explicit "不会" option and a latency-based grade hint on every tapped format

What. Add a grey last option "不会 / 没把握" to `mc`, `multi` and `bug` (and a "没把握" chip on the new formats). Tapping it ends the card as a miss without the penalty of a wrong guess and prints "按 Again". After a right answer the card prints the elapsed time next to the suggested grade (under about 4 seconds and right: Easy; under 10: Good; slower: Hard). This is confidence-based marking at no extra tap, because the declaration is the answer itself.
Source. Gardner-Medwin (https://www.physoc.org/?p=55824); Sparck, Bjork and Bjork on confidence weighting; the grade line already exists in the templates (`SHOW`). Caveat: the independent 2019 BMC trial found no exam gain, so treat it as honest-grading hygiene, not a learning multiplier. The real gain is that Chi stops pressing Good on lucky guesses, which keeps the scheduler honest.
Also copy from anki-boi: after the answer, say whether a miss was a wrong pick or a missed correct option (we show wrong rows already; add "漏选" for multi).
Cost: tiny. Time is `Date.now()` stored with `keep()`; no new note fields except an optional per-point "must-know" flag for always showing 不会.

### 4. Fill the blank from a word bank, in code (faded-Parsons cloze)

What. A short code excerpt with one or two blanks; below it 4 chips; a tap on a chip fills the next blank; a tap on a filled blank empties it; two blanks cost two taps, then it grades itself. Distractor chips are near misses.
Source. Duolingo-style word bank (Cambridge One and Sublearn above), the Clozemaster-style Anki template (2024-12-07, https://forums.ankiweb.net/t/randomized-multiple-choice-cloze-tests-similar-to-clozemaster-for-anki-desktop-and-mobile-experimental-card-template-mini-game/52843) for the AnkiMobile mechanics, faded Parsons problems for the learning rationale (https://escholarship.org/content/qt8794g5s0/qt8794g5s0.pdf).
Why. Our `bug` format spots a wrong line; our cloze is self-graded. This tests whether the learner can produce the one load-bearing token (a condition, a status code, a command) with a visible menu, in about 6 seconds.

Example (乐观锁):

> **Q** 补全：
> ```
> UPDATE account SET balance = ?, version = version + 1
>  WHERE id = ? AND [1]
> -- 影响行数为 0 时：[2]
> ```
> Chips: `version = ?`　`balance > 0`　重读后重试　直接覆盖写入
> **Answer** [1] `version = ?`（只有版本没变才更新）；[2] 重读后重试。
> **Why** 「直接覆盖写入」是丢失更新；「balance > 0」是业务检查，不是并发检查。

### 5. Code lines in order with a distractor (Parsons with a decoy)

What. `order` with a fifth line that must not be tapped, then a 确定 button (same button style as `multi`). A tapped decoy counts as an error. This is the closest we can get to a Parsons problem, with the distractor evidence from the ITiCSE 2023 working group (distractors help learners recognise and avoid common errors). I found no Anki template for it, so it would be new to the ecosystem.
Cost: `order` plus a `Decoys` field of indices and the 确定 button from `multi`; scoring is the displacement score of recommendation 1 plus 2 per wrong tap.

Example (乐观锁的重试循环):

> **Q** 按执行顺序点出步骤（有 1 行多余，不要点），再按确定。
> Rows: 「SELECT balance, version FROM account WHERE id=?」「在内存里算出新余额」「UPDATE … WHERE id=? AND version=?」「影响行数为 0 就回到第一步重试」「SELECT … FOR UPDATE（悲观锁的写法）」
> **Solution** 1 读（含版本）→ 2 计算 → 3 带版本条件的 UPDATE → 4 行数为 0 则重试。 `FOR UPDATE` 是多余项：它是悲观锁。

### 6. Rotate the format of the same point across the successive passes (scheduling, not a template)

What. Keep one card per point for the first pass (a recognition format: choice, multi, bug, Kprim). When the point has been passed once, the next pass is a different format of the same point (rank, fill-from-bank, cloze), and the third is the production card (flash Q&A or the main deck's recall card). Anki's own learning steps (1m 2h 6h) already supply the successive-relearning sessions; the missing part is that the format changes.
Source. Successive relearning (Rawson and Dunlosky 2022, https://journals.sagepub.com/doi/full/10.1177/09637214221100484); Wozniak's redundancy rule ("from different angles"); Little and Bjork on MC plus recall. It is consistent with the rule in the deck's memory that recognition formats are first-pass only.
How in this deck. One extra card per top-weight point, written in a second format and held back by the existing planner (`quick_plan.py`) until the first card has an interval of, say, three days (suspended then unsuspended, or released by the planner). I would not do it for every point: it doubles the cards. Start with the points Chi missed twice in `report`.

Example (令牌桶), same point, three formats in order:
1. 选择：「令牌桶允许短时突发吗？」 是 / 否 / 不会。
2. 排位 or 填空：「令牌桶的 3 个参数」 chips 桶容量、填充速率、限流键 plus 滑动窗口大小 as a decoy.
3. 快问：「令牌桶满了之后新令牌怎么办？」 → 丢弃；容量上限即最大突发。

### 7. Staged reveal and a checklist self-check for chains and "说出要点" cards

What. Two variants of the self-graded card, both with `tappable`:
- Staged reveal (Cloze Interactive, 2026-10-19, tested on AnkiMobile 25.09): a chain of 3 to 4 items hidden behind chips; the learner thinks, taps each chip to check it, then grades. Use for chains that cannot be ranked because the items are not comparable, for example 「令牌桶：容量、速率、键」.
- Checklist back (my design, I found no community template): the front asks 「说出 X 的 3 个要点」; the back lists the points as rows that the learner taps if he had them; the count of taps prints the grade hint (3 of 3 Good, 2 Hard, fewer Again). It makes the self-grade less generous without typing.
Why this rank. Wozniak and Matuschak both warn about lists; these two keep the list short and give the learner a way to check items one by one. The risk is that self-checking is optimistic, which is why the checklist counts taps. It is slower than the others (8 to 12 seconds), so it belongs on the cards where the answer really is a short set.

Example (乐观锁):

> **Q** 乐观锁更新要具备哪 3 件事？
> Back rows, tap what you had: 「表里有版本号（或时间戳）列」「UPDATE 的 WHERE 带上读到的版本」「检查影响行数，为 0 则重试或报冲突」
> Hint line: 点到 3 个 → Good。

### 8. Native image occlusion for architecture diagrams

What. Anki's built-in image-occlusion note type for box-and-arrow diagrams (rate limiter in front of a gateway, the idempotency-key store next to the payment service): one mask hides one box, the card asks "this box is what, and why is it here". No script, no add-on; AnkiMobile reviews it natively. The deck's baseline wants at least a quarter of cards with a diagram (memory: diagram-baseline), and this satisfies it with the least code.
Caveats. Rendering differences on AnkiMobile versus desktop were reported (https://forums.ankiweb.net/t/image-occlusion-background-and-colors-distorted-inverted-on-ankimobile-ios-compared-to-desktop/70437), and creation on iOS is documented only secondhand. Generating IO notes from our script means writing the note type's occlusion field format, which I did not look into; check it before committing. The tap-to-reveal is the default Anki one, so it is not a tap-to-judge interaction; it competes with `bug` and `match` rather than adding a new skill.
Example (限流器架构图): mask the box between the gateway and the application servers; answer 「Redis（共享令牌桶或计数）」 with the extension line 「为什么不放在应用进程内：多实例各算各的，总速率超限」.

## 6. What I would not add

- Drag and drop, or up/down arrow reordering (ikkz, DamianZaremba): conflicts with AnkiMobile swipes, needs more touches than tap-in-sequence, and no source claims iOS support.
- Typed answers: Chi's constraint, and AnkiMobile has had script problems on type-in cards.
- Two-option yes/no choice cards: Matuschak's litmus-test note says they produce shallow understanding. Use Kprim (four judgements) so chance is not 50 percent per card.
- Long enumerations as one rank card: Wozniak and Matuschak both argue against lists; beyond four items use chain cloze (overlapping, as Cloze Overlapper did, generated by our script).
- Generated random distractors per review (ale18V approach) for now: cheap to build but needs a vetted bank of near-miss wrong options per point, which is the real work. Revisit if the deck gets stale on repeated options.

## 7. Unverified or not found

- Nothing was tested on a device by me. The `ankitap` flip is a private API; two sources (2024-12 forum, 2026-10 Cloze Interactive) say it may break, and our templates already fall back to a normal tap.
- I could not open the Execute Program page text or the ITiCSE report PDF; those points come from Matuschak's notes and search snippets. Brilliant's, Mochi's and RemNote's question formats were not found.
- The claim "no Anki Parsons template exists" rests on GitHub and forum searches on 2026-11-16, which are weak for this topic.
- Image occlusion on AnkiMobile: sources conflict by age; check on Chi's installed version.
