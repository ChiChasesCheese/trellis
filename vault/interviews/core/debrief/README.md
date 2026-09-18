# debrief/ — 把一场面试的录音变成一份 mock 式评审

面完录音 → 本机转写 → 数字（语速 · 填充词 · 停顿 · 语法 · 题 ↔ 题库 · JD 线 · 每题 rubric）→ 人工评审。
**录音不出本机**：转写用本地 Whisper，语法用本地 LanguageTool，没有任何上传。

```bash
# 在仓库根目录，一次装好（macOS Apple Silicon 走 mlx-whisper，其它平台走 faster-whisper）
uv sync --extra debrief

# 1. 转写（30 分钟 mp3 在 M4 Pro 上约 70 s；首次会下载 ~1.6 GB 模型）
uv run --extra debrief python vault/interviews/core/debrief/transcribe.py <录音> \
    -o vault/interviews/companies/<co>/debrief/<date>-<round>

# 2. 分析（--bank 指向那一轮的题库；只录到自己麦克风的录音加 --candidate-only）
uv run --extra debrief python vault/interviews/core/debrief/analyze.py \
    vault/interviews/companies/<co>/debrief/<date>-<round> \
    --bank vault/interviews/companies/<co>/loop/rounds/<round>/bank.json [--candidate-only]

# 3. 人工评审：读 turns.md + report.md，对照 rubric.md / stories.md 写 REVIEW.md（模板见下）
```

产物（都在 `companies/<co>/debrief/<date>-<round>/`，**mp3 本身不进 repo**）：

| 文件 | 内容 |
|---|---|
| `transcript.json` / `transcript.md` | Whisper 原始结果（词级时间戳）/ 可读版 |
| `turns.md` | 按说话人切成的轮次；`--candidate-only` 时按 > 6 s 静音切成一个个回答 |
| `metrics.json` | report 引用的全部数字 |
| `report.md` | §1 说话与节奏 · §2 语法 · §3 题 ↔ 题库关键词覆盖 · §4 JD 线 · §5 自动结论 |
| `REVIEW.md` | **人写的**：一句话结论 → 这场实际的形状 → 逐题打分 + 改写 → 横向练法 → 发音清单 → 回写清单 |

## 开源工具选型（2026-09）

| 需求 | 选了 | 为什么 | 备选 |
|---|---|---|---|
| 语音转写 | **mlx-whisper**（`mlx-community/whisper-large-v3-turbo`） | Apple Silicon 原生（Metal），30 min 音频 ~70 s；词级时间戳；`condition_on_previous_text=False` 防长录音幻觉循环 | **faster-whisper**（CTranslate2，CPU/CUDA，自带 VAD，非 Mac 的默认）；openai-whisper（PyTorch，慢）；whisper.cpp（C++，需自己编） |
| 说话人分离 | **没上**——启发式（问句 = AI）+ `speakers.json` 人工覆盖；只录到自己麦克风时用 `--candidate-only` | pyannote 需要 HF token + PyTorch，且 AI 面试只有两方、问句特征明显 | **whisperX**（对齐 + pyannote diarization，torch）；pyannote.audio 单独用 |
| 语法 | **language-tool-python**（LanguageTool，本地 Java） | 开源、规则可解释、每条带上下文和建议；剔除标点/大小写类（那是 Whisper 的标点不是你的） | Gramformer（T5，需 torch）；调 LLM（要上传） |
| 语速 / 填充词 / 停顿 | 自己写（词级时间戳） | 30 行代码 | — |
| 题 ↔ 题库 | 自己写（Jaccard + keys 命中） | 题库 `bank.json` 已带 `keys` | 向量检索（过重） |
| 每题 rubric | 自己写（ownership / mechanism / number / structure / learning / length 六信号） | 直接对应 Chakra 的 Met 定义 | LLM 打分（要上传） |

## 已知边界

- 屏幕录制软件录 AI 面试通常**只录到你的麦克风**（AI 从耳机出来），所以 `--candidate-only` 是常态；AI 的问题只能从回答反推（`report.md` §3 的匹配是启发式，人工评审要重新对一遍）。想两边都录：系统音频用 BlackHole/Loopback 做 aggregate device。
- Whisper 在静音里会幻觉出 "Thank you." / "It's It's"；`analyze.py` 用词概率 < 0.35 + 幻觉短语表过滤，仍可能漏一两条，看 `turns.md` 时留意。
- 语法数字只计"真的错"（GRAMMAR / TYPOS / MISC / STYLE），不计标点和大小写；转写把口语断句成的句子也会触发少量误报（例如 `It's It's`），看例子再信。
- rubric 六信号是词表匹配，只能当"可能缺什么"的提示；3/2/1 的判断在 `REVIEW.md`。

## REVIEW.md 模板

```
# REVIEW · <公司> <轮次> · <日期>
## 0. 一句话结论（最伤分的三件事，按严重度）
## 1. 这场实际的形状（问了什么、顺序、和邮件/题库预期的差别）
## 2. 逐题评审（时间 · 反推的题 · 你说了什么 · Chakra 档 · 它会记下的证据 · 改写 ≤ 60 s）
## 3. 横向练法（一周内能改的三件事，每件一条命令）
## 4. 发音清单（转写听错的词 = AI 也听错的词）
## 5. 回写到 kit（02-process 亲历 · questions.md 新段 · stories.md 好句子）
```

第一份实例：`../../companies/snowflake/debrief/2026-09-17-chakra/`。
