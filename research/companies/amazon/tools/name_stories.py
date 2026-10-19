"""Replace story codes (S1-S11, M1, R1-R3, G1-G4) with story names on the Amazon LP pages (Chi, 2026-10-19:
「不要用字母代号，就点出具体的故事」). Idempotent: run again and nothing changes.

    python3 research/companies/amazon/tools/name_stories.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KIT = ROOT / "vault/interviews/companies/amazon"
NAMES = {
    "S1": "Amex 结算管线", "S2": "Quality-check 框架", "S3": "ACH 费用 NULL 事故", "S4": "澳洲 Amex 退款费",
    "S5": "Net Settlement 数据源切换", "S6": "费用异常检测器 go/no-go", "S7": "schema pool",
    "S8": "Terraform 7 分钟 RCA", "S9": "Amex 出款延迟事故", "S10": "退款费 billing-terms 复盘",
    "S11": "实习：Kafka 事件流", "M1": "新人 onboarding 与带教", "R1": "Quant-Stroller 研究平台",
    "R2": "AI-native 迁移", "R3": "Aiki 消费者 App", "G1": "一个自信的错数字", "G2": "不依赖 agent 自述的正确性",
    "G3": "GenAI 不必要的时候", "G4": "什么时候信任 LLM",
}
CODE = re.compile(r"(?<![A-Za-z0-9_/\-])(S1[01]|S[1-9]|M1|R[1-3]|G[1-4])(?![0-9A-Za-z_])")
FENCE = re.compile(r"```.*?```", re.S)


def rename(text: str) -> str:
    # headings that start with a code: "# S3 · title" / "## G1 · title" -> drop the code
    text = re.sub(r"^(#{1,3}) (?:S1[01]|S[1-9]|M1|R[1-3]|G[1-4]) · ", r"\1 ", text, flags=re.M)
    # matrix first column "**S1** English name" -> "**story name**"
    text = re.sub(r"\*\*(S1[01]|S[1-9]|M1|R[1-3])\*\* [^|\n]+", lambda m: f"**{NAMES[m.group(1)]}**", text)
    parts = re.split(r"(```.*?```|\[\[[^\]]*\]\])", text, flags=re.S)   # leave code and wikilinks alone
    for i in range(0, len(parts), 2):
        parts[i] = CODE.sub(lambda m: f"「{NAMES[m.group(1)]}」", parts[i])
    text = "".join(parts)
    return text.replace("「「", "「").replace("」」", "」")


files = list((KIT / "lp").rglob("*.md")) + [KIT / "README.md", KIT / "LOOP_GUIDE.md"]
changed = 0
for p in files:
    old = p.read_text(encoding="utf-8")
    new = rename(old)
    if new != old:
        p.write_text(new, encoding="utf-8")
        changed += 1
left = sum(len(CODE.findall(FENCE.sub("", re.sub(r"\[\[[^\]]*\]\]", "", p.read_text(encoding="utf-8"))))) for p in files)
print(f"{changed} file(s) changed; codes left outside code/wikilinks: {left}")
