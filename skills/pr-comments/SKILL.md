---
name: pr-comments
description: Rules for comments an agent posts on a pull request - review summaries, correction updates and replies to reviewers or review bots. Use before posting or editing any PR, MR or linked-issue comment.
metadata:
  credits:
    skill: leaving-pr-comments
    author: Theo Browne
    url: "https://github.com/t3dotgg/tstack/blob/main/skills/leaving-pr-comments/SKILL.md"
---

# PR comments

A comment is the public record of a review or a correction. Post on the PR or MR, drafts included. When the repository's review surface is the linked task in its tracker, post there.

## Every comment

- **Read first.** Read the existing comments before writing, so a retry updates your earlier comment instead of adding a second one.
- **Lead with the conclusion**, then cite the code, check or reproduction behind it. Separate what you verified from what you judge.
- **Stable finding IDs.** A finding keeps the ID its first review gave it in every later comment.
- **Public-safe.** The text, its quotes and its attachments hold only what may be published: repository-relative paths, public links, and nothing from private logs or credentials. Write in the language the repository requires.
- **Verify the post.** A comment is posted once the host returns its URL. On a failed write, check whether the comment already exists before retrying. After two failures from the same cause, report the delivery failure and the recovery it needs, and keep the completed review or code work.

## Review summary

One comment per review pass, keyed by PR, reviewed HEAD and scope.

- Name the reviewed HEAD and scope. For each finding give its ID, a link to the affected code, the concrete impact and the supporting evidence.
- Post accepted findings as they arrive, and label the comment **incomplete** until every required review and your own verification finish. Post the final outcome even when no finding remains.
- On a re-review, state for each earlier finding whether it is **verified fixed**, **still open** or **declined**, with evidence, and link the correction comments and commits. An implementer's claim of a fix is pending until you verify it.
- Earlier passes stay as history. Posting a summary is separate from marking a draft ready or submitting a formal approval.

## Correction update

One comment per published HEAD and finding set, posted after the push.

- Link the review summary it answers and use its finding IDs.
- Give each finding one status: **fixed, pending independent verification**, **still open**, or **declined** with evidence. Add the commit links and the verification results that matter.
- A new correction round gets a new comment linked to the previous one.

## Replies and threads

Reply in the thread the finding came from. Resolve a thread after your reply is posted and the finding is addressed or withdrawn with a written reason.
