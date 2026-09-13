#!/usr/bin/env python3
"""Assemble reports/stripe-oa-report.html from CATALOG.md, TEST_SUMMARY.md, REVIEW_FINDINGS*.md."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "stripe-oa-report.html"


def md_table(text: str) -> str:
    """Convert a markdown pipe table (already isolated) into an HTML table."""
    rows = [r for r in text.strip().splitlines() if r.startswith("|")]
    if len(rows) < 2:
        return ""
    cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    def inl(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(https?://[^\s,)]+)", r'<a href="\1">\1</a>', s)
        return s
    h = "".join(f"<th>{inl(c)}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{inl(c)}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="scroll"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def section_table(md: str, heading: str, limit: int | None = None) -> str:
    m = re.search(rf"^## {re.escape(heading)}.*?\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    if not m:
        return ""
    block = m.group(1)
    lines = [ln for ln in block.splitlines() if ln.startswith("|")]
    if limit:
        lines = lines[: 2 + limit]
    return md_table("\n".join(lines))


def md_list(md: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}.*?\n(.*?)(?=^## |\Z)", md, re.S | re.M)
    if not m:
        return ""
    items = re.findall(r"^\d+\.\s+(.*)$", m.group(1), re.M)
    def inl(s):
        s = html.escape(s)
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return "<ol class='drill'>" + "".join(f"<li>{inl(i)}</li>" for i in items) + "</ol>"


def review_summary() -> str:
    parts = []
    for name in ["REVIEW_FINDINGS.md", "REVIEW_FINDINGS_2.md"]:
        p = ROOT / "reports" / name
        if not p.exists():
            continue
        txt = p.read_text()
        for m in re.finditer(r"^##+\s*(q\d+\S*).*?\n(.*?)(?=^##+\s*q\d|\Z)", txt, re.S | re.M):
            body = m.group(2)
            v = re.search(r"(SOUND|BUG FOUND|SPEC AMBIGUITY)", body)
            hi = len(re.findall(r"\bhigh\b", body, re.I))
            me = len(re.findall(r"\bmedium\b", body, re.I))
            lo = len(re.findall(r"\blow\b", body, re.I))
            parts.append((m.group(1), v.group(1) if v else "—", hi, me, lo))
    if not parts:
        return "<p class='muted'>Adversarial review in progress — see reports/REVIEW_FINDINGS*.md when it lands.</p>"
    rows = "".join(
        f"<tr><td><code>{html.escape(d)}</code></td><td><span class='pill {v.split()[0].lower()}'>{v}</span></td>"
        f"<td>{hi}</td><td>{me}</td><td>{lo}</td></tr>" for d, v, hi, me, lo in parts)
    return ("<div class='scroll'><table><thead><tr><th>problem</th><th>verdict</th><th>high*</th><th>medium*</th><th>low*</th></tr></thead>"
            f"<tbody>{rows}</tbody></table></div><p class='muted'>* keyword counts in the findings text — read the file for the actual items.</p>")


def main() -> None:
    catalog = (ROOT / "catalog" / "CATALOG.md").read_text()
    summary = (ROOT / "reports" / "TEST_SUMMARY.md").read_text()
    tot = re.search(r"\*\*(\d+) problems · (\d+) tests\*\* \(edge (\d+) · fmt (\d+) · perf (\d+) · io (\d+)\)", summary)
    n_prob, n_tests, n_edge, n_fmt, n_perf, n_io = tot.groups() if tot else ("?",) * 6
    n_a = len(re.findall(r"^\| A\d+ \|", catalog, re.M))
    n_b = len(re.findall(r"^\| B\d+ \|", catalog, re.M))
    n_c = len(re.findall(r"^\| C\d+ \|", catalog, re.M))
    summary_table = md_table("\n".join(l for l in summary.splitlines() if l.startswith("|")))

    page = f"""<title>Stripe OA Drill Kit</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--bg:#F4F5F9;--surface:#FFFFFF;--ink:#1B1F2B;--muted:#5B6275;--line:#D9DCE6;--accent:#4B45B5;--accent-ink:#FFFFFF;--good:#1F7A4D;--warn:#A8701A;--bad:#B23A3A;--code:#EEF0F7}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#121420;--surface:#1A1D2B;--ink:#E7E9F1;--muted:#A0A6BA;--line:#2C3044;--accent:#8C86EE;--accent-ink:#121420;--good:#5CC98F;--warn:#E0B060;--bad:#E27979;--code:#232739}}}}
:root[data-theme="dark"]{{--bg:#121420;--surface:#1A1D2B;--ink:#E7E9F1;--muted:#A0A6BA;--line:#2C3044;--accent:#8C86EE;--accent-ink:#121420;--good:#5CC98F;--warn:#E0B060;--bad:#E27979;--code:#232739}}
body{{background:var(--bg);color:var(--ink);font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.55;margin:0}}
main{{max-width:72rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}}
h1{{font-size:2rem;font-weight:700;letter-spacing:-.01em;margin:0 0 .25rem;text-wrap:balance}}
h2{{font-size:1.25rem;font-weight:600;margin:2.75rem 0 .75rem;padding-top:.75rem;border-top:1px solid var(--line);text-wrap:balance}}
p{{max-width:68ch}} .muted{{color:var(--muted);font-size:.9rem}}
.eyebrow{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.75rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(10rem,1fr));gap:.75rem;margin:1.5rem 0}}
.stat{{background:var(--surface);border:1px solid var(--line);border-radius:6px;padding:.9rem 1rem}}
.stat b{{display:block;font-size:1.75rem;font-weight:600;font-variant-numeric:tabular-nums;line-height:1.1}}
.stat span{{color:var(--muted);font-size:.85rem}}
code{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.86em;background:var(--code);padding:.1em .35em;border-radius:3px}}
pre{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.85rem;background:var(--code);padding:1rem;border-radius:6px;overflow-x:auto}}
.scroll{{overflow-x:auto;border:1px solid var(--line);border-radius:6px;background:var(--surface);margin:.75rem 0}}
table{{border-collapse:collapse;width:100%;font-size:.88rem}}
th,td{{text-align:left;padding:.5rem .65rem;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-weight:600;white-space:nowrap;position:sticky;top:0;background:var(--surface)}}
td{{font-variant-numeric:tabular-nums}} tr:last-child td{{border-bottom:0}}
a{{color:var(--accent)}} a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
ol.drill{{padding-left:1.4rem;max-width:70ch}} ol.drill li{{margin:.35rem 0}}
.pill{{display:inline-block;padding:.05em .55em;border-radius:999px;font-size:.78rem;font-weight:600;border:1px solid var(--line)}}
.pill.sound{{color:var(--good);border-color:var(--good)}} .pill.bug{{color:var(--bad);border-color:var(--bad)}} .pill.spec{{color:var(--warn);border-color:var(--warn)}}
ul{{max-width:72ch}} li{{margin:.25rem 0}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:1rem 2rem}}
</style>
<main>
<div class="eyebrow">Stripe · 60-min HackerRank · multi-part</div>
<h1>Stripe OA Drill Kit</h1>
<p class="muted">Everything found online about Stripe's coding screens, deduped and rebuilt as runnable Python drills with full test suites. Repo: <a href="https://github.com/ChiChasesCheese/stripeoa">ChiChasesCheese/stripeoa</a> · local <code>~/Code/ITV/stripe-oa</code> · 2026-08-26</p>
<div class="stats">
<div class="stat"><b>{n_prob}</b><span>problem sets (40 bespoke + 13 LeetCode-tag)</span></div>
<div class="stat"><b>{n_tests}</b><span>tests, all green</span></div>
<div class="stat"><b>{n_edge}</b><span>edge-case tests · {n_fmt} format · {n_perf} perf · {n_io} stdin/stdout</span></div>
<div class="stat"><b>{n_a + n_b}</b><span>catalogued problems with sources ({n_a} bespoke · {n_b} algo · {n_c} title-only)</span></div>
</div>

<h2>What the OA actually is</h2>
<ul>
<li>HackerRank, <strong>60 minutes, one bespoke problem in 3–5 parts</strong> that unlock in sequence; every part extends the same program, so an early shortcut costs you the later parts.</li>
<li><strong>~17–25 hidden tests.</strong> Reported: 14/20 rejected; 18/20, 22/25, 16/19 advanced. Partial credit moves you on.</li>
<li><strong>Not LeetCode.</strong> Parse stdin/CSV → dict-of-records state → business rules → byte-exact stdout. Stripe employee on Blind: "input parsing, creating classes, proper data structures, business logic".</li>
<li>Any language; Stripe engineers advise against Java for speed. Browser IDE, print-debug only, tab focus logged, paste/similarity detection — <strong>type from scratch in the real thing.</strong></li>
<li>The bank is <strong>small and recycled</strong> (≈3 problems rotating per cycle; "Stripe has a small fixed set of questions"), and OA problems reappear in the 45–60 min phone screen.</li>
</ul>

<h2>Drill these first</h2>
<p class="muted">Ranked by OA stage × recency × independent references (from <code>catalog/CATALOG.md</code>). Run <code>python drill.py start q01</code>.</p>
{md_list(catalog, "Top 10 to drill first")}
<p>Next: <code>q04</code> card ranges · <code>q13</code> ledger · <code>q05</code> Luhn · <code>q06</code> Atlas names · <code>q10</code> payment intents. Phone-screen set: <code>q22</code> shipping · <code>q21</code> currency · <code>q19</code> Accept-Language · <code>q25</code> invoices · <code>q32</code> money transfer. Algorithms: <code>qA01–qA13</code>.</p>

<h2>Catalog — bespoke problems (Table A, top rows)</h2>
<p class="muted">Full table with all {n_a} rows, aliases and footnoted URL lists: <code>catalog/CATALOG.md</code>. #refs counts independent reports only.</p>
{section_table(catalog, "Table A", 15)}

<h2>Catalog — LeetCode Stripe-tag problems (Table B)</h2>
{section_table(catalog, "Table B")}

<h2>Skills the OA tests, and where each is drilled</h2>
<div class="two">
<div><p><strong>Decide pass/fail most often</strong></p><ul>
<li>S01 read all parts before coding; shape the state for the <em>last</em> part</li>
<li>S04 aggregate once per group, never per row</li>
<li>S05 strict vs non-strict thresholds; count vs ratio; minimum-volume gates</li>
<li>S06 integer minor units, one explicit rounding rule</li>
<li>S08 deterministic tie-breaks · S09 byte-exact output</li>
<li>S10 reversals in event streams · S11 idempotent repeats</li></ul></div>
<div><p><strong>Also graded</strong></p><ul>
<li>S02 delimiter parsing with malformed lines · S03 records + dicts by id</li>
<li>S07 tiered/metered/prorated math · S12 dates, offsets, hour buckets</li>
<li>S13 inclusive intervals and gap filling · S14 string canonicalization</li>
<li>S16 sliding windows / token bucket · S17 ledgers and reserves</li>
<li>S18 validation paths · S19 parse→model→compute→render split</li>
<li>S20 self-testing per part · S24 payments vocabulary</li></ul></div>
</div>
<p class="muted">Full mapping (24 bespoke targets S01–S24, 16 algorithm targets A01–A16, problems, JD lines): <code>skills_matrix.md</code>.</p>

<h2>Adversarial review of the top OA problems</h2>
<p class="muted">Independent brute-force oracle vs the reference on ≥2000 random inputs, every listed edge case, byte-diff of the stdin/stdout path, quadratic check. Files: <code>reports/REVIEW_FINDINGS.md</code>, <code>reports/REVIEW_FINDINGS_2.md</code>.</p>
{review_summary()}

<h2>Test inventory</h2>
<p class="muted">Per problem: tests by part, edge/format/perf/io counts, measured perf-test cost, and the last full run. Budgets: 2 s and 256 MB on the largest plausible input.</p>
{summary_table}

<h2>The 60-minute protocol</h2>
<pre>python drill.py start q01         # prints the WHOLE statement, resets starter.py, starts the timer
python drill.py test q01 -k part1  # lock part 1 before touching part 2
python drill.py test q01           # edge + fmt + perf + io against YOUR starter.py
python drill.py time q01           # minutes left
python drill.py ref q01            # the reference solution passes everything</pre>
<ul>
<li><strong>0–5 min</strong> read every part; pick the data shape the last part needs.</li>
<li><strong>5–45</strong> code part by part; lock each with its tests before moving on.</li>
<li><strong>45–55</strong> boundary sweep: empty · single · duplicate · out-of-order · zero · negative · exact threshold.</li>
<li><strong>55–60</strong> output format only. Debug prints go to stderr and get deleted.</li>
</ul>

<h2>Caveats</h2>
<ul>
<li>1point3acres threads and 题库 full texts are paywalled; their content came from snippets and first screens. Five threads listed in <code>catalog/raw/cn_sources.md</code> §5 (e.g. thread-1145788 "stripe OA 彙整 2026") deserve a manual read with your account.</li>
<li>Parts marked <strong>(reconstructed)</strong> in a problem.md were designed from a title only — practice material, not the exact hidden tests.</li>
<li>Aggregator numbers (rates, thresholds) were only trusted when corroborated; each problem.md names the trusted source per number and keeps alternatives under <em>Variants</em> (often behind a flag with its own tests).</li>
</ul>
</main>
"""
    OUT.write_text(page)
    print(OUT, len(page))


if __name__ == "__main__":
    main()
