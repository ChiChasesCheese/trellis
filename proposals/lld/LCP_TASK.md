You write one problem leaf of the low-level-design domain in /Users/chiserver/sessions/trellis: `lcproject.lcp-{NAME}`.

Read /Users/chiserver/sessions/trellis/proposals/lld/LCP_AGENT.md first and follow it; it tells you to follow
proposals/lld/PROBLEM_AGENT.md with its changes, and proposals/WRITING_RULES.md overrides both.

The real workspace is in sources/local/lc-project/workspaces/{NAME}/files/ (README.md is the contract; OVERVIEW.md the
task; the template and any provided modules; the public tests if the project ships any; REFLECTION.essay the written
questions). Read every file first and decide the kind (build / repair / incident) from the README. If the workspace
ships no public test file, your own suite is the only check: make it cover every README rule and every example the
README gives, and run the README's examples as tests. Your solution must pass the official public tests, if any, in a
scratch copy (LCP_AGENT.md §4). Look in vault/domains/low-level-design/problems/ for a classic problem the project
extends (LCP_AGENT.md §9) and link it.

Resume rule first: run `uv run python scripts/check_lld_problems.py --branch lcproject lcproject.lcp-{NAME}`; if it
prints ok, stop and report; otherwise do only what it lists as missing and never rewrite a file that already passes.

Do not run git. Do not start other agents. Touch only this leaf's files (and /tmp scratch copies). Your final message
is the report LCP_AGENT.md describes, plus the official public test summary line (or "no public tests shipped").
