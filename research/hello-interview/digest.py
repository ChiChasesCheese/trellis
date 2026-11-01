"""One compact line block per design question (title, crux, deep-dive heads, follow-up heads) for pattern mining.

    python3 research/hello-interview/digest.py   # -> research/hello-interview/digest.md
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
out = []
for f in sorted((ROOT / "vault/interviews/core/design-questions").glob("*.md")):
    t = f.read_text(encoding="utf-8")
    title = re.search(r"^\*\*([^*\n]+)\*\*｜(\S+)", t, re.M)
    crux = re.search(r"\*\*一句话。\*\*\s*(.+)", t)
    def heads(label):
        m = re.search(rf"\*\*{label}。\*\*(.*?)(?=^\*\*[^*\n]{{1,14}}。\*\*|\Z)", t, re.S | re.M)
        if not m:
            return []
        hs = re.findall(r"^(?:\d+\.|[-*])\s+(.+)$", m.group(1), re.M)
        return [re.split(r"[：:。]", h)[0][:60] for h in hs][:8]
    out.append(f"## {f.stem} — {title.group(1) if title else f.stem} ({title.group(2) if title else ''})\n"
               f"- 难点：{crux.group(1)[:160] if crux else ''}\n- 深入：{' | '.join(heads('深入'))}\n- 追问：{' | '.join(heads('取舍与追问'))}\n")
(ROOT / "research/hello-interview/digest.md").write_text("\n".join(out), encoding="utf-8")
print(len(out), sum(len(x) for x in out))
