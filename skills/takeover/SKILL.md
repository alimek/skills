---
name: takeover
description: Finish work someone else started. Use when the user asks to take over a PR, a branch or another agent's thread.
metadata:
  credits:
    skill: takeover
    author: Theo Browne
    url: "https://github.com/t3dotgg/tstack/blob/main/skills/takeover/SKILL.md"
---

# Takeover

You now own the original goal. The inherited implementation is evidence of one attempt, to keep where it serves the goal and to replace where it does not.

## Steps

1. **Read the source.** Read the PR, branch or thread, its review findings and the user's later corrections. Resolve the handoff to the actual code at its current head, and account for uncommitted work. Done when you can state the goal, what exists, and what is still open.
2. **Check it still belongs.** Fetch the target branch and compare it with the point the work diverged from: has the problem been solved elsewhere, or have the APIs and boundaries it touches moved? Done when you can say the work is current, needs rework, or is obsolete. Report obsolete work to the user and stop there.
3. **Continue on the original commits.** Continue in place when the user asks for that; otherwise import the original commits onto a new branch and add your changes as separate commits. Git authorship of the inherited commits stays as it is, and the PR description credits the original contributors and links the original PR. Leave the original PR and unrelated work untouched unless the user authorised changing them.
4. **Finish the same goal.** Rework what the goal needs and simplify without dropping intended behaviour. Verify the original failure and the realistic workflow yourself, following the repository's rules; passing mocked tests alone leave the user-facing behaviour unverified.
5. **Publish and follow through.** When the finish includes a PR, write it with `$pr`, then carry it to readiness with `$pr-completion`. Replies follow `$pr-comments`.
6. **Report** what you inherited, what you changed, how you verified it, how credit was kept, what stays unverified, and any decision left to the user.
