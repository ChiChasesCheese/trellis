"""Pairs of merged cards (cards/premium/sdx/) that may teach the same thing, most similar first, for a human to judge.

    uv run --with scikit-learn python research/hello-interview/sdx/cross_dups.py [threshold]
"""
import sys
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

sys.path.insert(0, str(Path(__file__).parent))
from candidates import tokens  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
files = sorted((ROOT / "vault/domains/hello-interview/cards/premium/sdx").glob("*/*.md"))
texts = [f.read_text(encoding="utf-8") for f in files]
m = TfidfVectorizer(analyzer=tokens, sublinear_tf=True).fit_transform(texts)
s = linear_kernel(m, m)
th = float(sys.argv[1]) if sys.argv[1:] else 0.35
pairs = sorted(((s[i, j], i, j) for i in range(len(files)) for j in range(i + 1, len(files)) if s[i, j] >= th), reverse=True)
for v, i, j in pairs:
    print(f"{v:.2f}  {files[i].parent.name}/{files[i].stem}  <>  {files[j].parent.name}/{files[j].stem}")
print(len(pairs), "pairs at or above", th, "among", len(files), "cards")
