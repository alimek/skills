---
name: source-review
description: Independent source-only review of a change against its accepted requirements, with two reviewers from different model families, a must-have gate, a ledger and a receipt. Use when asked to review a PR or branch before merge, when an agent prompt names source-review, or to check a review receipt.
---

# Source review

You coordinate an independent **source review** of one change. Reviewers read; they run nothing. The outcome is a **receipt** that later stages can check against the exact HEAD.

## Steps

1. **Pin.** Record repository, PR, target branch, base or merge-base and the full HEAD SHA. Done when every later statement can name the SHA it is about.
2. **Requirements.** Find what the change was accepted to do: the spec or tickets when they exist, otherwise the issue, the PR description and the task you were given. Record which source you used. A change without a spec is reviewed against its stated intent. Done when the accepted requirements fit in a few lines you can paste into a brief.
3. **Scope.** Choose one, before any dispatch:
   - **FULL**: no trustworthy coverage of this PR exists. Review the whole accepted change.
   - **DELTA**: a completed review exists and HEAD moved. Review `git diff <last reviewed HEAD>..<HEAD>`, the earlier required findings and the paths and invariants the change causally affects. A merge from the target branch means reviewing the conflict resolutions and the integration, not the imported code.
   - **REUSE**: HEAD and effective scope are unchanged. Reuse the reports and assess only new concrete evidence.

   A new SHA alone keeps existing coverage. Go back to FULL only when coverage is missing or unverifiable, the accepted scope materially changed, or a rewrite cannot be reconciled with the reviewed code; write down why.
4. **Dispatch.** For FULL and for a DELTA that touches code, use `$fan-out` for two reviewers on strong models from different model families. For a DELTA limited to prose documentation or comments, with no executable, configuration, dependency, generated or contractual change, one fresh reviewer is enough; record why the reduced scope applies. REUSE dispatches nobody. Give each reviewer the brief in [REVIEWER-BRIEF.md](REVIEWER-BRIEF.md), filled in, and nothing about the other reviewer's answer or the implementer's own verdict. For DELTA add that reviewer's previous report, the ledger and the correction references. Done when every reviewer the scope requires has reported; a missing or timed-out report is missing, never a pass.
5. **Verify.** Check each finding against the source and the must-have gate yourself, deduplicate, and keep earlier justified dispositions unless new evidence changes them. You validate and consolidate; the reviewers did the reviewing. Re-read the PR's actual HEAD and scope before deciding. Done when every finding is accepted or declined with a reason.
6. **Record.** Write the ledger. Done when it holds this pass, including on a failing verdict.
7. **Publish.** Post the review summary as `$pr-comments` describes and put its URL in the ledger.
8. **Verdict.** Changes are required only for accepted must-haves. With none left and coverage complete, issue the receipt.

## Source only

This applies to you and to every reviewer. Read source, diffs, requirements, documentation and existing evidence; read-only file, Git and hosting queries are allowed to fetch them. Repository code, tests, builds, package managers, linters, formatters, diagnostic scripts, browsers and servers stay unexecuted, and nothing is installed. Source evidence can establish a defect; label a reproduction you did not execute as unexecuted. When runtime evidence is missing, ask for it through a finding or in the handoff to the implementer.

## Must-have gate

A finding is a **must-have** when it is one of:

- a concrete defect this change introduced or made reachable;
- an accepted requirement the change does not meet;
- a violation of an explicit mandatory repository rule.

Each must-have states its trigger, its concrete impact or the exact rule, the changed-code location and the source evidence. A severity label alone does not qualify. Preferences, speculative improvements, refactors, extra coverage without an important missing protection and unrelated baseline issues are declined, and a complete review may find nothing. Only must-haves go to the implementer.

## Ledger

Keep the ledger and the reviewers' reports where the caller says. Without that, use `source-review/pr-<number>/` under `git rev-parse --git-common-dir`, which is local and shared by every worktree. The ledger records:

- PR and scope identity, the baseline SHA and the latest reviewed SHA;
- each reviewer's model, report reference and coverage;
- every required finding with its stable ID, status and evidence, and every declined finding with its reason;
- the chain of reviewed deltas and the URLs of the published summaries.

The next pass starts from the last **reviewed** commit, whether or not that pass succeeded.

## Receipt

The receipt is the part of the ledger that certifies one HEAD: the ledger reference, the baseline-to-current coverage chain, the latest reviewed HEAD, the reviewers and their reports, each finding's status and the limits of what was verified.

A receipt is **valid** for a HEAD when the chain reaches exactly that SHA and:

- the code is covered by two completed FULL baselines plus two-reviewer DELTAs for every later code change; and
- each documentation-only DELTA has one reviewer and its recorded reason, appended as shared coverage without claiming the other model reviewed it; and
- no accepted must-have is open.

Later stages check the receipt against the current HEAD. A valid receipt needs no fresh pair of reports per commit. An uncovered change goes back to this review at the scope the ledger supports.
