# cb03_vetting · what you are handed at minute 0

`vetting` is a small Python service a security team uses to review job applicants before an
account is ever provisioned for them. It reads applications from an applicant tracking system and
pre-boarding sign-ins from an identity provider, runs a set of checks on each person, and shows a
human reviewer a ranked list with an evidence trail. Each customer organization is a separate
tenant. It is a security tool: it never decides anything about hiring.

The repository is `starter/`. It has a README, a CONTRIBUTING file, sample data in `fixtures/`, a
CLI (`python -m vetting ...`) and a test suite (`python -m pytest`). You will be given one ticket
from `tickets/` in the room. Nobody wrote the ticket with your codebase in mind; ask what you need.
