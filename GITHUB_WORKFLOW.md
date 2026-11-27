# GitHub identity & workflow — Extract Point (Policy A)

**Repository class:** Tutorial source (`monsun-labs/extract-point`)  
**Policy:** A — Tutorial source repositories

This document is **repository-specific**. Do not apply it to `monsun-labs.github.io` or unrelated Monsun repos.

## Roles

| Role | Account |
|------|---------|
| Developer | **monsunic** |
| Commit author | **monsunic** (verified noreply identity) |
| Git push authentication | **monsunic** |
| Pull Request creator | **monsunic** |
| Reviewer | **tyorus** |
| Approver | **tyorus** |
| Merger | **tyorus** |
| Auto-merge | **Disabled** |

## Local Git identity (already configured in this clone)

```text
user.name  = monsunic
user.email = 241242318+monsunic@users.noreply.github.com
```

Configured with `git config --local` only (never `--global`).

Shared with all worktrees of this repository.

## Authentication switching

Current machine state at policy setup:

- Default `git@github.com` SSH key authenticates as **tyorus**.
- `gh` active account is **tyorus**.
- Dedicated `monsunic` SSH key may still need to be created and registered.

### Intended SSH remotes (after monsunic key exists)

```bash
# Inspect before any write:
git remote -v
git rev-parse --show-toplevel

# Example push URL using host alias from ~/.ssh/config:
git remote set-url --push origin git@github.com-monsunic:monsun-labs/extract-point.git
```

Host aliases (user SSH config):

- `github.com-tyorus` → `~/.ssh/id_ed25519`
- `github.com-monsunic` → `~/.ssh/id_ed25519_monsunic` (create + upload to monsunic account)

### gh CLI

```bash
gh auth status
# When monsunic is added as a second account:
gh auth switch --user monsunic   # before PR create as developer
gh auth switch --user tyorus     # before review / approve / merge
```

## Pre-flight checklist (every remote write)

1. Confirm repo: `git remote -v` shows `monsun-labs/extract-point` (or intentional fork).
2. Confirm identity: `git config --get user.name` → `monsunic`.
3. Confirm auth account matches Policy A developer for push/PR create.
4. Do **not** merge your own PR as monsunic — hand off to **tyorus**.

## Out of scope

- Website repo `monsun-labs/monsun-labs.github.io` (Policy B — tyorus only).
- Other Monsun product repos unless explicitly classified.
