# Obsidian setup (chi-mini as the always-on sync hub)

Flow: Claude sessions push to GitHub `main` → Obsidian on chi-mini runs the Git plugin on `~/Code/trellis/vault`, pulling
every 5 min → Obsidian Sync carries the vault to the phone and laptop → edits made on the phone come back through Sync and
are committed and pushed by the Git plugin every 10 min (vault folder only).

## Already done on chi-mini

- `brew install --cask obsidian` (Obsidian 1.14.5; listed in chifig `Brewfile.gui`).
- `~/Code/trellis` cloned (ssh remote, push works).
- `scripts/obsidian_setup.sh` run: Git plugin 2.42.0 installed with `obsidian/obsidian-git.data.json`
  (pull on start and every 5 min, commit+push every 10 min, rebase, vault folder only), the `no-wrap-code` CSS snippet
  enabled (code blocks scroll sideways instead of wrapping), the vault registered with the app, Obsidian started.

## State (2026-10-23)

- Remote vault **`Trellis_`** (the one the phone already used), device name `chi-mini`, conflict action *merge*.
  Selective sync: appearance + CSS snippets on (the phone gets `no-wrap-code`), community plugins off (only chi-mini runs Git).
- First connect pulled 81 pre-restructure copies (old `headlands/study/…`, `04_sd`, `catalog` paths) — deleted on chi-mini,
  so Sync removed them everywhere. Before connecting another git checkout to a Sync vault, pause the Git plugin's
  auto commit (`autoSaveInterval` 0), let Sync finish, compare `git status` with `main`, clean up, then turn it back on.
- Kept out of git through `~/Code/trellis/.git/info/exclude` (they still sync privately):
  `vault/interviews/core/leetcode/tops/` (2216 cards whose `skeleton/leetcode-tops.yaml` and `scripts/leetcode_tops/`
  exist only on another machine — commit all three together from there), and two personal notes
  (`core/踩过的坑.md`, `abnormal/study/20-cards/claude_prompts.md`; the repo is public).
- Obsidian CLI is on (`obsidian help`; `obsidian sync:status`).

## Left for Chi

1. **Start at login** on chi-mini: System Settings → General → Login Items → `+` → Obsidian (the mini must stay logged in
   for the Git plugin to run).
2. **Phone**: Settings → Appearance → CSS snippets → check `no-wrap-code` is on (it arrives through Sync).
3. **MacBook**: if it also runs the Git plugin on a Sync-connected checkout, set its auto commit to 0 — chi-mini is the only
   machine that commits Sync edits. Push `skeleton/leetcode-tops.yaml`, `scripts/leetcode_tops/` and the tops cards from there.

## Another machine with a git checkout

```bash
scripts/obsidian_setup.sh            # or: scripts/obsidian_setup.sh /path/to/trellis/vault
```

Only one machine should run the Git plugin's auto commit+push against a Sync-connected vault (chi-mini). On other
machines either use Sync alone or keep the checkout and turn the plugin's intervals to 0.
