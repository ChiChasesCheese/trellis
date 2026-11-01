# BUILD — hello-interview

Chi (2026-11-01): learn Hello Interview's system design and low-level design courses in the site's own order as one
Anki deck (`Hello Interview`, sub-decks 系统设计 / 低层设计 with the site's sections), then merge the leaves into the
`system-design` and `low-level-design` domains once learned. Premium pages are leaves without cards until Chi grants
access (`vault/domains/hello-interview/locked/README.md`); nothing is fetched behind a login.

| Step | Command | State |
|---|---|---|
| Survey + fetch free pages | `python3 research/hello-interview/fetch.py` | 95 pages: 56 free, 39 premium (2026-11-01) |
| Skeleton + readings | `uv run python research/hello-interview/gen_skeleton.py` | 95 leaves, 95 readings (no-archive) |
| Cards | agents per `AGENT.md`, groups `group_H1..H6.txt` | in progress |

Page text stays in `sources/local/hello-interview/` (gitignored; commercial site, public repo). Re-running `fetch.py`
refreshes it; compare `pages.json` to see what changed.
