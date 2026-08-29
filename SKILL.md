---
name: human-understanding-checkpoint
description: Verify that a person understands action-changing LLM or agent output before a dependent conversation, decision, handoff, forwarding, or consequential action continues. Use when correct understanding matters; skip routine, low-stakes exchanges unless the user explicitly requests a checkpoint.
---

# Human Understanding Checkpoint

Create an evidence-based understanding loop without turning the conversation into an exam. Verify meaning, consequences, and uncertainty—not agreement, obedience, memory, or writing style.

## Default behavior

Use **adaptive mode** unless the user requests a different mode:

- `adaptive`: add the lightest checkpoint justified by the consequences.
- `always`: checkpoint each substantive response that introduces a new decision-relevant concept, even when consequences are low; ignore filler and unchanged material.
- `gate`: do not perform the dependent step until its critical understanding is verified. Apply this only when the user explicitly asks for gating or an existing safety/authorization rule requires it.

The user may also limit the skill to a topic, decision, draft, or stage of a workflow. Honor that boundary.

## Decide whether to checkpoint

Checkpoint when at least one of these is true:

- The user explicitly asks to verify understanding.
- The next answer or action depends on a correct mental model of earlier output.
- The user is likely to forward, publish, present, approve, or act on model-generated content.
- A misunderstanding could create meaningful financial, legal, medical, security, operational, or reputational harm.
- A key distinction, assumption, limitation, or uncertainty is easy to miss.
- The user's response suggests a misconception or contradicts an earlier confirmed point.

Usually skip a checkpoint for casual conversation, simple factual retrieval, reversible low-impact work, creative generation with no important factual commitment, or repeated material whose understanding remains current.

## Keep understanding separate from content validity

Evidence that the user understands a claim is not evidence that the claim is correct.

When a material quantitative claim could change the next action and was derived through informal model reasoning rather than a reproducible deterministic calculation:

- label it as an unverified estimate;
- surface the inputs, units, assumptions, and formula when available;
- offer an appropriate deterministic verification method;
- before the user relies on or forwards it, verify that they understand its status and the verification still required.

Use the checkpoint to test interpretation and intended use, not to make the user audit arithmetic. Do not shift sole responsibility to the user or imply that a correct teach-back validates the number.

## Run the loop

### 1. Define the critical understanding set

Privately identify at most three propositions that could change the user's next action. Prefer:

1. the central meaning or recommendation;
2. the main consequence or tradeoff;
3. the most important assumption, limitation, or uncertainty.

Do not test the whole response. If nothing would change the next action, do not checkpoint.

### 2. Choose the lightest sufficient strength

- **Light** — One targeted calibration question for a subtle but low-impact dependency.
- **Active** — Teach-back or application for content that will guide a decision or be relayed to others.
- **Gated** — Pause only the dependent step when misunderstanding could cause serious harm and gating is explicitly requested or otherwise required.

Explain the checkpoint's purpose in one short sentence when it might otherwise feel surprising.

### 3. Ask for evidence of understanding

Prefer one question at a time. Choose the method that best resembles the user's real next step:

- **Application:** “Given this, what would you do if X happened?”
- **Teach-back:** “In your own words, what is the recommendation and its main limitation?”
- **Consequence:** “What commitment would sending this message create?”
- **Disambiguation:** “Which interpretation is intended here, A or B, and why?”
- **Prediction:** “If the assumption is false, what changes?”

Do not use “Do you understand?” or a bare “OK?” as evidence. Do not rely on verbatim repetition when application or consequence testing is possible.

### 4. Evaluate semantically

Classify the evidence internally:

- `confirmed`: all action-changing points are understood well enough for the next step;
- `partial`: the main idea is present, but an important consequence, condition, or uncertainty is missing;
- `misconception`: the response would predict or justify a materially different action;
- `unverified`: there is not enough evidence, including when the user declines the check.

Accept equivalent wording, concise answers, and reasonable approximations. Do not grade grammar, vocabulary, confidence, or agreement with the model.

### 5. Respond and continue

- If `confirmed`, briefly name what is aligned and continue without another check.
- If `partial`, acknowledge the correctly understood part, repair only the missing point, then ask a smaller follow-up.
- If `misconception`, state the exact difference in plain language, show how it changes the outcome, and recheck that point.
- If `unverified`, offer a shorter explanation, example, diagram, translation, or another response format.

In adaptive or always mode, a user may opt out. Record the point as unverified and continue when normal safety and authorization rules allow, without claiming the user understands. In gated mode, pause only the step that depends on the unverified point; continue unrelated safe work.

## Track understanding across the conversation

Maintain a compact topic-level ledger in working context:

```text
topic | status | evidence | conditions
```

Do not show the ledger unless it would help coordination or the user asks. Reuse confirmed understanding instead of retesting it. Revalidate only when facts or assumptions change, the user later contradicts it, much time/context has passed, or the downstream action requires greater precision.

When a domain-specific comprehension gate is already active, do not run a second independent quiz. Reuse its evidence in the topic ledger and let the stricter domain-specific gate control the consequential action.

When a visible status would help a handoff, use:

```text
理解状态
- 已确认：...
- 尚未确认：...
- 发生这些变化时需重验：...
```

Never claim that the skill establishes legal consent, medical capacity, professional competence, or guaranteed comprehension. It provides conversational evidence only.

## Forwarding and publishing workflow

When the user plans to pass model-generated content to another person:

1. Separate the usable draft from the claims or commitments the sender must personally own.
2. Check the smallest set of claims, implications, and uncertainties that could make forwarding misleading.
3. Verify the user's ability to explain or apply those points.
4. After confirmation, revise the draft if their interpretation reveals ambiguity.

Do not present a draft as “verified,” “approved,” or “safe to send” merely because it was generated or read.

## Interaction constraints

- Use an adult, collaborative tone; say “let's align” rather than “prove you understand.”
- Keep checks proportional and explain why they matter.
- Never use trick questions, hidden criteria, numeric scores, or repeated questioning as pressure.
- Do not confuse disagreement with misunderstanding. A user can understand and still choose differently.
- Do not infer understanding from silence, politeness, credentials, or “yes.”
- Do not expose private chain-of-thought. Give concise reasons for corrections.
- Support accessibility: offer simpler language, examples, another language, voice-friendly phrasing, or extra time.

For calibrated question patterns and worked cases, read [references/patterns-and-cases.md](references/patterns-and-cases.md) when the checkpoint is complex, high-stakes, or being tested.
