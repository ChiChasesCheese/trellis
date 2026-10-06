# INSIDER-340: Google Workspace onboarding

We are onboarding a customer on Google Workspace. Add Google Drive audit logs as a source. Sample
exports from their admin console are in `fixtures/raw/gdrive/`. It should show up in
`python -m insiderwatch replay <raw_dir> --json` under the source name `gdrive`.
