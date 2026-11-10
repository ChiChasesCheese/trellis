#!/bin/sh
# Install the private-material guard as pre-commit and pre-push hooks in a checkout (default: this one).
set -e
repo="${1:-$(git rev-parse --show-toplevel)}"
for hook in pre-commit pre-push; do
  mode=staged; [ "$hook" = pre-push ] && mode=push
  f="$repo/.git/hooks/$hook"
  [ -e "$f" ] && ! grep -q private_guard "$f" && mv "$f" "$f.before-guard"
  printf '#!/bin/sh\nexec python3 "%s/scripts/private_guard.py" %s\n' "$repo" "$mode" > "$f"
  chmod +x "$f"
done
echo "private guard installed in $repo"
