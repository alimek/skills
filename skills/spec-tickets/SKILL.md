---
name: spec-tickets
description: Break a plan, spec, or conversation into tracer-bullet tickets with blocking edges and a recommended implementation model from fan-out.
disable-model-invocation: true
---

# Spec tickets

Break a plan, spec, or conversation into **tickets**: tracer-bullet vertical slices, each declaring its **blocking edges** and a recommended **implementation model** chosen with `$fan-out`.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Process

### 1. Gather context

Work from the current conversation context. If the user passes a reference (a spec path, an issue number or URL), fetch it and read its full body and comments. Done when you hold the full requirements and any linked decisions.

### 2. Explore the codebase (optional)

Explore the codebase when you have not already done so. Use the project's domain glossary vocabulary and respect ADRs in the area you touch. Look for prefactoring opportunities ("make the change easy, then make the easy change"). Done when you know the current architecture and any prefactoring needed first.

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow, complete path through every layer (schema, API, UI, tests): vertical, not a horizontal slice of one layer.
- A completed slice is demoable or verifiable on its own.
- Each slice fits in a single fresh context window.
- Any prefactoring comes first.
- As a secondary size check, when a slice looks likely to exceed ~1000 LOC, look for natural sub-slices that stay vertically complete and let smaller models execute the tighter parts cleanly. Keep a larger slice intact when splitting would break cohesion or force horizontal cuts.

</vertical-slice-rules>

Give each ticket its **blocking edges**: the tickets that must complete before it can start. Tickets with no blockers form the initial **frontier** and can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (renaming a column, retyping a shared symbol) whose blast radius fans across the codebase so a single edit breaks many call sites at once and no vertical slice can land green. Sequence it as **expand–contract**: first expand (add the new form beside the old so nothing breaks), then migrate call sites in batches sized by blast radius (per package or directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch, and finally contract (delete the old form once no caller remains), blocked by every migrate batch. When batches cannot stay green alone, keep the sequence on a shared integration branch where all batches block a final integrate-and-verify ticket.

Done when every requirement is covered by a slice and every blocking edge is explicit.

### 4. Assign implementation models

Call `$fan-out` and check live capabilities to pick a recommended **model ID** and **effort** for implementing each ticket.

- Route by remaining **judgment**, complexity, and scope tightness, using estimated size as a secondary signal: tight, well-bounded slices get smaller/cheaper execution models; ambiguous or high-judgment slices get stronger models.
- Record only the model ID and effort (e.g., `gpt-6.1-sol (low)` or `claude-sonnet-5-5 (medium)`), never a provider instance name, which is resolved live at run time.
- Treat the recorded model as an optional hint for downstream runners (`$spec-run`): if a model is omitted or unavailable at run time, `$spec-run` falls back to `$fan-out` defaults.

Done when every ticket has a model and effort assignment grounded in live capabilities.

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **Model**: recommended model ID and effort, with a short reason
- **What it delivers**: the end-to-end behaviour this ticket makes work

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct: does each ticket only depend on tickets that genuinely gate it?
- Do the model assignments fit each ticket's complexity?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 6. Publish the tickets to the configured tracker

Publish the approved tickets in dependency order (blockers first). How you publish depends on the tracker `/setup-matt-pocock-skills` configured:

- **Local files** → write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01` in dependency order. Each file's "Blocked by" lists the numbers/titles it depends on. Write one ticket per file, never a combined file.
- **A real issue tracker (GitHub, Linear, …)** → publish one issue per ticket in dependency order so blocking edges reference real identifiers. Use the platform's native blocking relationship where available; otherwise list blocking issues under "Blocked by". If the source was an existing issue, attach each ticket as its sub-issue. Apply the `ready-for-agent` triage label unless instructed otherwise. Leave any parent issue open and unchanged.

Done when every approved ticket is published with its blocking edges and model recommendation.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

**Blocked by:** the numbers/titles of the tickets that gate this one, or "None (can start immediately)".

**Model:** `<model-id>` (`<effort>`)

**Status:** ready-for-agent

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Model

`<model-id>` (`<effort>`)

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when blockers were set as native edges.

</issue-template>

In either form, avoid specific file paths or code snippets that go stale fast. Exception: if a prototype produced a decision-rich snippet (state machine, reducer, schema, type shape) that is clearer than prose, inline only the decision-rich parts and note briefly that it came from a prototype.
