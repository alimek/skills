---
name: fan-out
description: "Select models and delegate scoped work in T3 Code. Use when a user, agent prompt or skill calls for delegation and needs model selection, effort, independence or escalation."
---

# Fan-out

Own model selection and delegation for the calling task. The caller owns the work: scope, number of workers, review criteria, approval gates and what happens after their results. Return results to that workflow; delegation adds no implementation, integration or review stages of its own.

## Brief and constraints

A task is **scoped** when its brief states the goal, inputs, permitted actions and completion criterion. It is **tight** when the approach is already decided. Clarify fuzzy scope in the parent or assign a strong model a bounded exploration before delegating dependent execution.

Carry the caller's worker count, model restrictions, independence, budget and workspace constraints into selection. Read-only reviewers and scouts get read-only briefs. Parallel writers need disjoint ownership; before retrying a writer, inspect its partial edits and include them in the replacement brief. Workspace and dispatch mechanics follow the current T3 orchestration rules.

## Model selection

This is the single source of model and effort preferences for callers. These are working preferences, not measured quality rankings or a promise of task cost. Choose the cheapest suitable model **and effort** that meet the brief and constraints; subscription availability, token use and retries affect actual cost.

Resolve provider instances, model IDs and supported options from live capabilities under T3's discovery rules. Provider instance names belong to that catalog, not saved prompts. Match the model's creator separately from its hosting provider: two Claude models through different providers are not independent model families.

| Model preference | Fit | Starting effort |
| --- | --- | --- |
| Callstack `callstack/Apex` | Tight React Native or Next.js implementation; unlimited allocation when available | Provider default |
| Cursor `composer-2.5` | Scoped implementation; subscription allocation when available | Provider default |
| `gpt-6.1-sol` | Fact gathering, scoped implementation, routine design questions | Low for tight work; medium when judgment is needed |
| `claude-haiku-5-5` | Bounded factual scouting and tight execution | Provider default |
| `claude-sonnet-5-5` | Scoped implementation and routine design alternative | Medium |
| `claude-opus-5-5` | Ambiguous design, hard debugging, independent review and red team | Medium, set explicitly |
| `gpt-6-astra` | Ambiguous design, hard debugging, independent review and red team | High for demanding review; medium otherwise |
| `grok-4.7` | An independent third design perspective; scoped work on subscription allocation | Provider default |

Select Fable (`claude-fable-5-2`) only when the user explicitly requests it for the task; this restriction also applies to escalation, retries and availability fallbacks.

For implementation, route by how much judgment remains in the brief, not code volume. For factual research, use a cheap scout; interpreting conflicting evidence is a judgment task. For review, consequential design or red team, use the strong judgment models rather than the cheap execution tier. A tight review brief can still require deep judgment.

When the caller requires two independent strong judgments, prefer Opus and Astra. For a three-family design panel, add Grok. For a red team independent of the parent, choose a strong model from another creator. Preserve the caller's required count and diversity when selecting from the live catalog; if they cannot be met, report the gap. A user-pinned unavailable provider/model or a failed dispatch follows T3's substitution rules, never a silent replacement.

## Dispatch and return

1. **Select.** Map each scoped task to a model, effort and available provider. Done when every assignment satisfies the caller's constraints; explain any unresolved gap before dispatching affected work.
2. **Dispatch.** Launch independent assignments together, with only the context each needs. Independent reviewers receive the same evidence and scope, without the sibling's current answer or the parent's correctness verdict. Follow each task's returned wait/resume instructions.
3. **Assess.** Check returned evidence against the completion criterion. Return completed results with model identities, limits and unresolved work. A missing answer remains missing, not agreement or a pass.

## Escalation

A wrong, stuck or incomplete answer needs a brief stating the specific gap, useful evidence and remaining work. Prefer higher effort on the same suitable model, then a stronger suitable model if needed, subject to T3's substitution rules and the caller's retry limit. For Opus, increase effort before changing models. Treat rate limits and exhausted quota as availability failures, not reasoning failures. If a retry adds no useful evidence, return the unresolved task to the caller instead of repeating it indefinitely.
