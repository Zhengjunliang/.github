# Zhengjunliang/.github

Defaults that GitHub applies to every repository of this account that has no file of the same kind, and the account's label manifest. How GitHub picks them up: "Creating a default community health file" in GitHub's documentation.

| File | GitHub uses it as | A repository replaces it with |
| --- | --- | --- |
| `CODE_OF_CONDUCT.md` | the code of conduct linked from issues, pull requests and the About box | its own `CODE_OF_CONDUCT.md` in `.github/`, the root or `docs/` |
| `CONTRIBUTING.md` | the "contributing guidelines" link shown when someone opens an issue or a pull request | its own `CONTRIBUTING.md`, same places |
| `SECURITY.md` | the policy on the Security tab | its own `SECURITY.md`, same places; a `docs/security.md` counts |
| `.github/ISSUE_TEMPLATE/` | the issue forms and the chooser | **any** valid template or `config.yml` in its own `.github/ISSUE_TEMPLATE/`, which replaces this whole folder |
| `.github/pull_request_template.md` | the body of a new pull request | its own pull request template |
| `labels/` | nothing: GitHub does not read it | — |

- This repository must stay public, or the defaults stop applying.
- A repository finds its own file first (`.github/`, then the root, then `docs/`), and this repository's file only when it has none.
- Defaults are not in a repository's clones or history, and there is no default licence: each repository holds its own `LICENSE`.
- A label an issue form sets must exist here and in the repository that uses the form; the label sync below keeps both.

## Labels

Every in-scope repository has exactly the labels of `labels/labels.json`: the `default` list, plus the repository's own list under `repos`.

| Dimension | Labels | Rule |
| --- | --- | --- |
| type | `type: bug` · `type: feature` · `type: task` · `type: epic` · `type: question` | exactly one on every open issue; none on pull requests |
| area | `area: …`, per repository | one or more where the repository defines them |
| severity | `severity: critical` · `high` · `medium` · `low`, per repository | exactly one on a security bug |
| status | `status: blocked` · `status: idea` | at most one |
| contributors | `good first issue` · `help wanted` | GitHub's own names, which feed its contributor pages |
| automation | `dependencies` | set by Dependabot only |

Sync, from any directory, in Git Bash or cmd.exe, with `gh` logged in:

    gh api -H "Accept: application/vnd.github.raw" repos/Zhengjunliang/.github/contents/labels/sync.py | python - Zhengjunliang/.github Zhengjunliang/multilingual-course-assistant

Add `--dry-run` to see the steps without making them. A repository joins the scope when its name is added to this line (and, if it needs its own labels, to `repos` in the manifest). School-exercise and private repositories stay out.
