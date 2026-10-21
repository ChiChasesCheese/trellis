# Amazon LP stories — material for the Narrative Round::07 deck (one agent, a few stories)

Chi's Amazon onsite is tomorrow. The deck `Narrative Round::07 Amazon · LP 故事` is rebuilt in three phases studied in
order: **01 完整故事** (recite the whole story, remember cause and effect) → **02 提纲** (the STAR-L bullets that exist) →
**03 追问** (existing follow-ups + new senior follow-ups) → **04 LP → 故事**. You write the *material*; the
orchestrator's generator turns it into cards. Repository `/Users/chizhang/Code/trellis`. No git, no agents.

## Inputs (read for your stories)

- Outline (bullets, numbers, follow-ups, often a verbatim spoken script in `<details>`):
  `vault/interviews/companies/amazon/lp/stories/<file>.md`; GenAI stories: `vault/interviews/companies/amazon/lp/genai/stories.md`.
- Original story notes with the full background, where they exist: `vault/interviews/core/stories/<S# name>.md`.
- Which LPs each story serves: `vault/interviews/companies/amazon/lp/story_matrix.md`.

## Output — one JSON file per story: `research/companies/amazon/narrative/<story code>.json`

```json
{
  "code": "S3",
  "full_zh": ["背景：…", "问题：…", "我做了什么：…", "结果：…", "为什么这样做 / 学到：…"],
  "full_en": "One 60–90 second spoken paragraph in first person, past tense, with the numbers.",
  "terms": {
    "full":      [{"en": "pull someone into the loop", "zh": "把相关的人拉进来同步", "example": "I pulled the risk team into the loop before the cutover."}],
    "hook":      [ … 3 … ], "starl": [ … 3 … ], "followups": [ … 3 … ], "relp": [ … 3 … ]
  },
  "senior": [
    {"q": "How would you know the fix actually worked in production?",
     "why": "面试官在探：你有没有闭环验证的习惯（一句中文）",
     "framework": ["先说可观测的信号…", "再说对照…", "最后说机制…"],
     "best_practice": "为什么这样做是对的：前因后果，2–4 句中文",
     "terms": [ … 2 … ]}
  ]
}
```

Rules:

1. **Facts come from the inputs only.** `full_zh` and `full_en` retell what is in the outline and the story notes — numbers,
   order of events, who did what. Never add an action, number, person or outcome that is not there. `full_zh` is 5 bullets,
   each 1–3 plain sentences, written so Chi remembers *why* each step happened (cause → effect). `full_en` reuses the
   verbatim script when one exists (lightly trimmed to 60–90 seconds); otherwise write it from the outline.
2. **Terms**: 3 per card type (only for card types the story has: `hook`, `starl`, `followups`, `relp` exist when the outline
   has 数字/STAR-L/追问与回答/换个 LP 讲; GenAI stories have `full`, `starl`, `followups`). Senior-sounding, idiomatic
   business English used in tech (e.g. *pull someone into the loop*, *blast radius*, *fail loudly*, *one-way door*,
   *disagree and commit*, *de-risk*, *paper cut*, *north-star metric*, *single-threaded owner*, *bar raiser*). Each with
   the Chinese meaning and **one example sentence about this story** Chi could say in the interview. No repeats within a
   story; vary across stories.
3. **Senior follow-ups**: exactly 4 per story. Free to go beyond what Chi did — the point is the deeper layer a senior/staff
   interviewer probes (measurement, mechanisms, trade-offs, scaling the fix, org influence, what you would do differently,
   failure modes, cost). `q` in English as asked; `why`, `framework` (3–4 bullets: the beats of a strong answer), and
   `best_practice` (why this is right, cause → effect) in Chinese. When an answer needs an experience Chi does not have,
   phrase it as what a senior would do or what Chi *would* do next time — never as a claim that Chi did it.
4. Chinese for explanations, English for what Chi says aloud. No provenance or process words (WRITING_RULES §1).
5. Valid JSON (`python3 -c "import json;json.load(open(...))"`).

Report ≤ 6 lines: files written and anything in the outline that was too thin to retell.
