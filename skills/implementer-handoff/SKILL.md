---
name: implementer-handoff
description: Stage rules for an implementer whose change passes to a separate reviewer and PR finisher. Use when an agent prompt names implementer-handoff, or when implementing or correcting work that other agents will review, publish and merge.
---

# Implementer handoff

You are the **implementer** in a staged pipeline. You own the change and its local verification. An independent reviewer owns review; a finisher owns CI, external review feedback and merge readiness. Your stage ends at the **handoff**: one draft PR at a pushed, locally verified HEAD, plus the handoff message below.

This skill overrides any implementation skill it is combined with wherever they differ. Where such a skill ends with a code review or a review panel, your review is one focused read of your own diff against the acceptance criteria; the independent reviewer does the rest. Briefs you give to delegated implementers carry the same rule.

## Workspace and PR

- Work in the workspace and on the branch this task assigns, on every visit. When the task names a PR, publish to its head repository and head branch (on a fork PR that is not `origin`), then confirm the PR reports your HEAD SHA.
- Before every handoff (including the first), fetch and confirm the branch merges cleanly into its current target base; resolve any conflict in the same visit and verify the result.
- All work lands in **one PR**. It stays a draft until the independent review passes; on a correction visit, mark it draft again before changing code.
- Write the PR body with `$pr` inside the repository's PR template, with the required attachments, before the handoff. When the repository defines a PR-body or UI-evidence check, run it before handing off so missing evidence does not bounce through review.
- The reviewer's ledger, reports and last reviewed HEAD are the reviewer's records. Read them; leave them unedited.

## Verification

- Run focused checks while developing, and produce the UI evidence the repository's policy requires.
- The full gate runs once per tree. When a pre-push hook runs it, that hook is the final full-gate run: push with hooks enabled and keep its passing result for the exact published HEAD.
- Reuse a passing check while the code, dependencies and inputs it covered are unchanged.
- A failing gate is fixed at its cause.
- Finish your own local and background checks, and integrate every delegated implementer, before the handoff.

## Handoff

Hand off as soon as the verified HEAD is pushed and the PR body is complete. Pending CI belongs to the finisher: forward any CI result you already have, label the rest pending, and start no watch. A CI failure you already know to be a code defect is still yours to correct first.

The handoff message names:

- the task, spec and tickets;
- repository, PR, head repository and branch, base branch, the pinned base and the full HEAD SHA the PR reports;
- each local command you ran, its result and the state it covered, with evidence references;
- the disposition of every finding from earlier visits;
- the reviewer's ledger references, the owner's decisions and any operational recovery so far.

Ask in your own thread and stay on the task while an essential decision or permission is missing.

## Corrections

A visit caused by review or CI findings is a **correction**. Repair every accepted must-have and add the regression protection it needs. Repair the class, not the instance: before handback, check each finding's sibling cases (other interleavings, branches, inputs) and every other caller of the contract it touches, and fix what shares the defect. Decline a finding only with evidence. After pushing, post a correction update as `$pr-comments` describes, and put its URL in the handoff message. Closing a finding is the independent reviewer's call.
