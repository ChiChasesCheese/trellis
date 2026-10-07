# INSIDER-318: Data theft on the way out

Most insider data theft happens in the weeks before someone leaves. Customers want us to flag
employees who are taking data on their way out, and they want analysts to be able to trust the
flags rather than get buried in noise from people who simply work with a lot of data.

After `python -m insiderwatch replay fixtures/raw --until 2026-09-30`, the right people should show
up in `python -m insiderwatch alerts --user <email>` (add `--json` for machine-readable output).
