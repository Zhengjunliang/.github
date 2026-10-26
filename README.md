# Zhengjunliang/.github

Defaults that GitHub applies to every repository of this account that has no file of the same kind, the account's Renovate preset and its label manifest. How GitHub picks them up: "Creating a default community health file" in GitHub's documentation.

| File | GitHub uses it as | A repository replaces it with |
| --- | --- | --- |
| `CODE_OF_CONDUCT.md` | the code of conduct linked from issues, pull requests and the About box | its own `CODE_OF_CONDUCT.md` in `.github/`, the root or `docs/` |
| `CONTRIBUTING.md` | the "contributing guidelines" link shown when someone opens an issue or a pull request | its own `CONTRIBUTING.md`, same places |
| `SECURITY.md` | the policy on the Security tab | its own `SECURITY.md`, same places; a `docs/security.md` counts |
| `.github/ISSUE_TEMPLATE/` | the issue forms and the chooser | **any** valid template or `config.yml` in its own `.github/ISSUE_TEMPLATE/`, which replaces this whole folder |
| `.github/pull_request_template.md` | the body of a new pull request | its own pull request template |
| `default.json` | nothing: Renovate reads it, for a repository whose config extends `local>Zhengjunliang/.github` | the rules its own Renovate config adds after that `extends` |
| `labels/` | nothing: GitHub does not read it | — |

- This repository must stay public, or the defaults stop applying.
- A repository finds its own file first (`.github/`, then the root, then `docs/`), and this repository's file only when it has none.
- Defaults are not in a repository's clones or history, and there is no default licence: each repository holds its own `LICENSE`.
- A label an issue form sets must exist here and in the repository that uses the form; the label sync below keeps both.

## Renovate

`default.json` is the preset a repository extends from its own `.github/renovate.json`:

    { "extends": ["local>Zhengjunliang/.github"] }

It runs once the hosted Renovate app is installed on that repository with read access to Dependabot alerts. Every update waits for the monthly run and for seven days after its release, except a security fix from those alerts, which opens at once. Everything arrives as a pull request: minor and patch updates in one, each major and each minor below 1.0 in its own. No Dependency Dashboard issue is opened, as nothing here waits for an approval given there.

## Labels

Every in-scope repository has exactly the labels of `labels/labels.json`: the `default` list, plus the repository's own list under `repos`, if it has one.

Six labels. A personal account has no issue types, so the type is a label: every open issue carries exactly one of the first four, and the type is not repeated anywhere else.

| Label | Meaning |
| --- | --- |
| `bug` | The system behaves differently from what is expected |
| `feature` | A new capability, or an improvement to an existing one |
| `task` | Work that changes no behaviour: maintenance, tooling, documents, decisions, delivery phases; a parent issue is a `task` whose parts are its sub-issues |
| `security` | An internal security finding. A vulnerability someone could exploit is reported privately instead, as SECURITY.md says |
| `blocked` | Waiting for a person, a decision or an external fact. An issue waiting for another issue uses GitHub's *Blocked by* relationship instead |
| `dependencies` | Updates a dependency; Renovate sets it |

Sync, from any directory, in Git Bash or cmd.exe, with `gh` logged in:

    gh api -H "Accept: application/vnd.github.raw" repos/Zhengjunliang/.github/contents/labels/sync.py | python - Zhengjunliang/.github Zhengjunliang/multilingual-course-assistant

Add `--dry-run` to see the steps without making them. A repository joins the scope when its name is added to this line (and, if it needs its own labels, to `repos` in the manifest). School-exercise and private repositories stay out.
