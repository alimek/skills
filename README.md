# skills

Agent skills I use, kept in one place so their history is tracked.

| Skill | What it does |
| --- | --- |
| `fan-out` | Selects models and effort, and delegates scoped work in T3 Code. |
| `grill-panel` | Grills a plan with a panel of subagents; you review one final ballot. Builds on the `grilling` and `domain-modeling` skills from [mattpocock/skills](https://github.com/mattpocock/skills) and on `fan-out`. |
| `pr-completion` | Monitors a pull request, addresses review feedback and verifies the current HEAD before reporting it ready. |

## Install

```bash
npx skills add alimek/skills --global
```

Add `--skill <name>` to install a single skill.
