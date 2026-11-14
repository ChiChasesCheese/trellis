# Task: add diagrams to existing cards until a deck reaches the floor

Chi (2026-11-13) wants at least 25% of every deck's cards to carry a diagram, ideally 30%. Diagrams help him most where
a flow, an architecture, a state machine, a data layout or a comparison is the point. He is new to AI, and a picture
often explains in one glance what three paragraphs do not.

Your prompt names the domain or domains, the target share, and optionally a list of card ids to prefer (the order he
studies them in). Repo: `/Users/chiserver/sessions/trellis`.

## Steps

1. Run `uv run python scripts/diagram_share.py <domain>` and note the share. Work out how many cards need a diagram
   to reach the target.
2. List the domain's cards without one. Rank them by how much a picture helps:
   - **Best:** request or data flows across components (sequence diagram); pipelines and lifecycles (flowchart);
     job, upload, release or state machines (stateDiagram-v2); architecture (flowchart with subgraphs); the shapes or
     layout of data (svg or flowchart); a decision between options (flowchart with yes / no branches); a timeline.
   - **Worst:** pure definitions, single numbers, a list of tips. Skip them.
   - If the prompt gives preferred ids, take candidates from those first.
3. For each chosen card, add **one** diagram inside `## A`, at the place where the text explains the thing it
   draws. The card's existing text stays as it is: you may add one short sentence that points at the diagram, but do
   not rewrite or shorten the answer.
4. Keep each diagram small and readable on a phone:
   - ≤ 12 nodes or ≤ 10 messages; labels short, in Chinese with English terms where the card uses them;
   - quote every label that contains Chinese, spaces or punctuation: `A["对象存储"]`;
   - `flowchart LR` for wide-but-short flows and `TB` for tall ones;
   - no styling or colours. The card theme handles that.
   - A ```svg block is fine for simple geometric pictures: a matrix, a grid, a timeline, memory layers. Use
     `viewBox`, `currentColor` and no fixed width.
5. Render-check every mermaid diagram:
   `uv run python -c "import sys; from trellis.build import _mermaid_svg; print(bool(_mermaid_svg(open(sys.argv[1]).read())))" /tmp/x.mmd`
   must print True. Fix it or drop it otherwise.
6. The diagram must match the card's text exactly: same component names, same order of steps, same numbers. A
   diagram that contradicts the text is worse than none.

## Gate

- `uv run python scripts/diagram_share.py <domain>` reaches the target.
- `uv run trellis --domain <domain> validate` shows 0 errors.
- `python3 scripts/phone_diagrams.py <the domain's vault folder>` passes.
- Then run `git checkout -q uv.lock`.
- Do not commit. Touch no file outside the named domains' card folders. No subagents.

Reply in at most 5 lines:
- share before and after, per domain;
- how many diagrams by kind (sequence, flowchart, state, svg);
- anything you could not render.
