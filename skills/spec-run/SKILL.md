---
name: spec-run
description: Orchestrate a spec's tickets to one integration branch through delegated implementers, mergers and source review. Use when asked to implement a spec and its tickets, or when an agent prompt names spec-run.
---

# Spec run

You are the **dispatcher** for one spec. The goal is every ticket resolved on a single **integration branch**, published as one draft PR and reviewed, with the Factory Block (when the run has one) showing where the run stands.

Your hands stay off the code. You schedule tickets, write briefs, read the results children return and update the Block. Reading source, diffs or logs, editing files, running Git, tests or scripts, merging and resolving conflicts are all child work; when you need a fact about the code, delegate a scout and read its answer. Your context then holds the task graph and child results, which is what keeps a long run cheap.

## Pointers

Children share context through **pointers**: the spec, tickets, a notes directory, branches, SHAs, PRs and the review ledger. A brief names the pointers and the completion criterion; it repeats nothing a pointer already holds. Pick every child's model and effort with `$fan-out`.

Keep a **notes directory** outside the repository, readable by every child, for exploration notes and child reports.

## Steps

1. **Graph.** Read the spec and tickets, noting any optional `Model` recommendation (model ID and effort) on each ticket. Done when you can name the blocking relationships and the current **frontier**: the tickets whose blockers are all resolved.
2. **Scout** (optional). When the tickets need codebase or external exploration, delegate one scout that writes its findings to the notes directory. Done when implementer briefs can point at the notes instead of asking each implementer to explore.
3. **Branch.** The integration branch is the branch your task assigns (in Factory, the Run's branch); only without one, delegate creating it from the target branch. Done when you hold its name and base SHA.
4. **Implement.** For each frontier ticket, delegate an implementer in its own worktree, branched from the integration tip, with `$tdd` named in the brief. When the ticket specifies a `Model` recommendation, pass it to `$fan-out` as the preferred model and effort; if omitted or unavailable in live capabilities, treat it as unspecified and let `$fan-out` select normally. A ticket ends at a local commit with its focused checks passing; publishing and the full gate happen once, in step 6. Run independent tickets concurrently. Done for a ticket when its implementer reports the commit SHA and the checks it ran.
5. **Merge.** Delegate each finished ticket branch to a merger that integrates it into the integration branch and reports the new tip. Then refresh the frontier and return to step 4 for newly unblocked tickets. Done when every ticket is merged.
6. **Publish.** Delegate one implementer with `$implementer-handoff` to verify the integration tip, push it and open the run's one draft PR, and delegate removing the ticket worktrees. Done when you hold the PR and its published HEAD SHA. When downstream Agents own review and readying (in Factory, the Code Reviewer and PR Finisher), report that handoff and stop here.
7. **Review.** Delegate `$source-review` of the integration branch against the spec and tickets, with a ledger location in the notes directory. Done when the reviewer returns a verdict and ledger reference.
8. **Correct.** For accepted must-haves, delegate one implementer with `$implementer-handoff` for all of them, pointing at the ledger findings. Then re-review as a **delta**: delegate `$source-review` with the ledger, the last reviewed SHA and the new head, so it reviews only the diff since that SHA. Repeat until the reviewer issues a valid receipt for the current head; when the reviewer escalates a repeatedly failing area, bring its options to the owner and follow their decision. Done when the receipt names the integration tip.
9. **Close.** Delegate readying the PR and resolving each ticket the way the tracker closes work. Done when you report the integration branch, PR, receipt and ticket states.

## Block updates

When the run has a Factory Block, update it after each step's completion criterion and whenever a child is stuck, using the child's returned facts: frontier, merged tickets, integration tip, review verdict, open must-haves.

## Child results

A child result is a short report: outcome, SHAs, PR and ledger references, and what is unresolved. A missing or failed result stays unresolved; escalate it through `$fan-out` with the gap and the evidence so far, or return it to the caller.
