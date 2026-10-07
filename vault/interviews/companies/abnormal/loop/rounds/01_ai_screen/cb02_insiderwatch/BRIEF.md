# insiderwatch (brief you get at minute 0)

You have joined the Insider Risk team. `insiderwatch` is our detection backend: it ingests audit logs
from customers' SaaS tools, builds a per-user picture of what is normal, and raises alerts when
someone's behaviour looks like an insider threat (data exfiltration, account misuse, sabotage).
It is a small Python codebase with no third-party dependencies; the tests are in `tests/`, sample
data is in `fixtures/`, and the CLI is `python -m insiderwatch`.

You will be given one ticket. You have an AI coding assistant, a terminal and about 60 minutes:
roughly 10 to understand the codebase, 35 to ship a first version of the ticket, and the rest to walk
us through what you did. The ticket is written the way a product manager would write it. Ask
questions, state your assumptions, and decide what a good first version is.
