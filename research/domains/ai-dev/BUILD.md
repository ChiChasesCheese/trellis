# ai-dev — build record

## Sources surveyed (step 1)

Surveyed 2026-11-20. GitHub search hit the API rate limit partway.

| # | Source | URL | Licence | Covers |
|---|---|---|---|---|
| 1 | Claude Code docs, Best practices (authoritative, vendor official) | https://code.claude.com/docs/en/best-practices | free-online | tell the agent what it cannot see, CLAUDE.md, skills, give it a check to run, hooks and permissions, subagent cost, parallel sessions, headless runs |
| 2 | METR, early-2025 AI and experienced open-source developers | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ | free-online | RCT: 16 developers, 246 tasks, 19% slower with AI, expected 24% speed-up, caveats; METR says results are out of date and published newer data in 2026-02 |
| 3 | DORA 2025 State of AI-assisted Software Development | https://dora.dev/research/2025/dora-report/ | free-online (full report on cloud.google.com/dora) | AI as amplifier of organisational strengths and weaknesses; AI capabilities model. Detail numbers NOT read |
| 4 | Stack Overflow Developer Survey 2025, AI section | https://survey.stackoverflow.co/2025/ai | free-online | 84% use or plan to; 51% of professionals daily; 33% trust accuracy, 46% distrust; 66% "almost right" frustration; ~31% use agents |
| 5 | Simon Willison, The lethal trifecta | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | free-online | security model for tool-using agents |
| 6 | Anthropic engineering blog | https://www.anthropic.com/engineering | free-online | effective harnesses for long-running agents, context engineering, permission design, parallel agents |
| 7 | OWASP Top 10 for LLM Applications 2025 | https://genai.owasp.org/llm-top-10/ | free-online | supply chain, excessive agency, injection |
| 8 | hesreallyhim/awesome-claude-code; ai-boost and walkinglabs awesome-harness-engineering (CC0) | https://github.com/hesreallyhim/awesome-claude-code | various | workflow, skills, subagents, hooks, spec-driven development, orchestration, observability categories |
| 9 | Not fetched (named in the brief; cite from the originals when writing cards): OpenAI Codex docs, Cursor docs, Addy Osmani, Kent Beck, GitHub Copilot research | | | tool docs and practitioner essays |

Authoritative outline: source 1 (official docs ToC) with source 2 to 4 for evidence. Three independent outlines: met (1, 6/8, and the evidence trio).

## Ledger
| Step | State |
|---|---|
| 1 survey | done 2026-11-20; Codex, Cursor, Osmani, Beck, Copilot research not opened |
| 2 outline draft | done, 69 leaves, 39 core; skeleton YAML not written |

## Not confirmed
- DORA 2025 specifics (adoption percentage, throughput vs instability, seven capabilities, archetypes): the page fetched had only the headline. Leaf names the finding only at "amplifier" level.
- Stack Overflow and METR numbers above come from the fetched pages (via a summarising fetch tool), not the raw documents; re-read before they go on a card.
- "slopsquatting" naming and the "comprehension debt" term are from memory; find a source.

## Next action
Chi reviews outline.md; then skeleton/ai-dev.yaml.
