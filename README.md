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

## Install

```bash
npx skills add alimek/skills --global
```

Add `--skill <name>` to install a single skill.

## Credits

`pr-comments` and `takeover` are adapted from [t3dotgg/tstack](https://github.com/t3dotgg/tstack) (MIT). Several skills call skills from [mattpocock/skills](https://github.com/mattpocock/skills): `pr`, `grilling`, `domain-modeling`.
