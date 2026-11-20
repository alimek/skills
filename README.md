# skills

Agent skills I use, kept in one place so their history is tracked.

| Skill | What it does |
| --- | --- |
| `fan-out` | Selects models and effort, and delegates scoped work in T3 Code. |
| `grill-panel` | Grills a plan with a panel of subagents; you review one final ballot. Builds on the `grilling` and `domain-modeling` skills from [mattpocock/skills](https://github.com/mattpocock/skills) and on `fan-out`. |
| `pr-completion` | Monitors a pull request, addresses review feedback and verifies the current HEAD before reporting it ready. |
| `pr-comments` | Rules for the comments an agent posts on a pull request: review summaries, correction updates and replies. |
| `source-review` | Independent source-only review against the accepted requirements: two reviewers from different model families, a must-have gate, a ledger and a receipt. |
| `implementer-handoff` | Stage rules for an implementer whose change passes to a separate reviewer and PR finisher. |
| `design-prototype` | Prototypes a UI change in Figma as lettered variants on a WIP page, then promotes the accepted one. |
| `takeover` | Finishes a PR, branch or agent thread someone else started. |
| `spec-run` | Orchestrates a spec's tickets onto one integration branch through delegated implementers and mergers, with delta re-review after corrections. Replaces `implement-spec` from mattpocock/skills. |

## Install

```bash
npx skills add alimek/skills --global
```

Add `--skill <name>` to install a single skill.

## Requirements

These skills build on [mattpocock/skills](https://github.com/mattpocock/skills) and call some of them by name, so install those as well:

```bash
npx skills add mattpocock/skills --global
```

| Skill here | Needs from mattpocock/skills |
| --- | --- |
| `grill-panel` | `grilling`, `domain-modeling` |
| `implementer-handoff` | `pr` |
| `takeover` | `pr` |
| `spec-run` | `tdd` |

`fan-out`, `implementer-handoff`, `source-review`, `pr-comments` and `pr-completion`, which other skills here call, are part of this repository.

## Credits

`pr-comments` and `takeover` are adapted from [t3dotgg/tstack](https://github.com/t3dotgg/tstack) (MIT).
