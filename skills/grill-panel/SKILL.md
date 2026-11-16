---
name: grill-panel
description: Grill a plan with a panel of subagents answering the rounds; you review one final ballot.
disable-model-invocation: true
---

Call the Skill tool for "grilling", "domain-modeling" and "fan-out". Grilling supplies the design tree, the frontier and the rounds; domain-modeling the domain discipline; fan-out model selection and dispatch. This skill changes who answers: a **panel** of subagents answers every round in the user's place, and the user's one decision is the verdict on the final **ballot**. Every question those skills would put to the user goes to the panel; every wait for the user is a wait for the panel. Glossary and ADR changes are queued for the ballot and written after the verdict.

## The panel

Brief each panelist with the round's questions, the facts with their sources, the decisions already settled and the user's own words. Send the questions without grilling's recommended answers, so the panel argues rather than confirms. Each panelist returns, per question: an answer, a one-line why, the alternatives it rejected, and every fact it had to assume.

- **Scouts** find the facts grilling assigns to sub-agents, and search closed issues, ADRs and the glossary for a **prior decision** on the same subject.
- **Routine** questions (mechanics, persistence, retries, error states, readiness, test seams, ticket cuts): one panelist answers the round's whole routine set.
- **Load-bearing** questions (product semantics and lifecycle, scope, UX against a reference, a new name, reversing a prior decision): three panelists from three distinct model families answer independently. A question settles only once all three answers are in; when fan-out cannot field a voice, the question stays open with the missing voice named. Unanimity settles it. Any split makes it **contested**: you pick the provisional answer and carry the dissent to the ballot.
- A fact only the user holds (their setup, their intent, a reference they have in mind): the panel proceeds on an explicit **assumption**, carried to the ballot.

## Steps

1. **Intake.** Invoked with no subject: ask, in one exchange, what to grill and how the user sees it working. Invoked with an idea, a bug or an issue: start from it. Done when the subject is the root of the design tree.
2. **Rounds.** Run grilling's rounds against the panel; panel answers settle decisions provisionally and push the frontier outward. When the user gave the subject but not how it works, the panel's model of it is decision **D0**, load-bearing. Done when the frontier is empty, or after 4 rounds with the remainder listed as open.
   Interrupt the rounds only for a contested question at the root of the tree, D0 included, since every round built on it would be rebuilt by the user's answer: put that one question to the user in grilling's format, then resume.
3. **Red team.** A red team selected through fan-out reads the full decision set, the prior decisions and the queued docs, and flags contradictions, unvisited branches and unearned assumptions. Route each proposed fix by the panel rules: load-bearing to three panelists, routine to one. The fixes get one round. Done when every flag is fixed, rejected with a reason, or listed as open.
4. **Ballot.** Present it in the format below. Done when the user replies.
5. **Verdict.** "ok" accepts everything. A correction reopens only the decisions that depend on it: run the panel there and present a ballot holding just the changed answers. Done when the user accepts; then write the queued glossary and ADR changes, tell the user in one line what was written, and continue as after any grill.

## Ballot

The ballot is a short summary of what the grill made of the user's idea: a person reads it in a minute and replies. Write it in the user's language, headings included. Every item is one plain statement about how the app will behave, never a question; name code only where the user named it. Every item carries one running number across all sections, so the user corrects anything by its number. The questions, the rounds and the internal machinery (panel tiers, decision codes, models, red-team flags, queued docs) stay in your notes. Omit empty sections.

<ballot-template>
## <subject>

**From:** <the user's idea, in their words, one line>
**To:** <two to four sentences: what the app will do after this change, as the user will experience it>

### Assumptions
1. <what the panel took as true without the user, one sentence>

### Decisions
Most important first, smaller details last.

2. <the decision, one sentence> _(panel split: <the other view>)_ ← only when the panel disagreed
3. <the decision, one sentence>

### Still open
4. <what is undecided, and why, one sentence>

Reply **ok**, or correct by number: `1: …, 3: …`.
</ballot-template>
