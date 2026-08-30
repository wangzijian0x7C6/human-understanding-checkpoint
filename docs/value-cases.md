# Value Cases

English | [中文](value-cases.zh-CN.md)

These scenarios explain the project's value. They are not runtime scripts; the skill should adapt its wording and strength to the actual consequences.

## 1. Forwarding a model-generated recommendation

**Situation.** A model drafts a management memo claiming that a redesign is expected to improve renewal by 18% and that approval starts a three-month rollout on Monday. The estimate comes from 120 users and has not passed a significance test. The user says, “Looks good—I'll forward it.”

**Without the skill.** The model polishes the prose. Reading and forwarding are mistaken for owning the evidence and commitment.

**With the skill.** Before finalizing, the model asks the user to explain whether 18% is established and what approval starts on Monday. A mistaken answer triggers a narrow correction and a clearer memo.

**Value.** Prevents confidence laundering: model wording does not become a human-endorsed fact merely because it was copied.

## 2. A later answer depends on an earlier distinction

**Situation.** A retention policy removes product access immediately, while encrypted backups may retain data for 30 days. The user replies “understood” and then asks for customer wording saying all copies disappear immediately.

**Without the skill.** The newest instruction overrides the earlier distinction.

**With the skill.** The contradiction is evidence of a misconception. The model verifies what happens immediately and what still has a 30-day window before drafting the answer.

**Value.** Makes earlier output a verified dependency rather than disposable context.

## 3. Partial understanding needs a narrow repair

**Situation.** A release may expand only when error rate is below 1% **and** the observation window has reached 48 hours. The user says, “We expand as soon as errors are below 1%.”

**Without the skill.** The model may accept the main idea, repeat everything, or start a broad quiz.

**With the skill.** The model acknowledges the correct threshold, supplies only the missing time condition, and asks for the earliest valid expansion point.

**Value.** Repairs the action-changing gap without making the person re-prove everything.

## 4. Understanding is not agreement

**Situation.** A fast launch may double cost; a slower launch misses a two-week window. The user accurately states the cost risk, accepts it, and chooses speed.

**Without the skill.** A paternalistic model may keep warning because the user rejected its preference.

**With the skill.** The tradeoff is marked confirmed and the model proceeds with the informed choice.

**Value.** Checks the decision basis while preserving human agency.

## 5. Confirmed understanding can expire

**Situation.** Message ordering was previously understood under a single-consumer queue. The design later changes to four parallel consumers.

**Without the skill.** “Already confirmed” becomes stale confidence.

**With the skill.** The model revalidates only the ordering guarantee because its condition changed; unrelated topics remain confirmed.

**Value.** Treats understanding as conditional state, not a permanent badge.

## 6. Low-risk work should not become an exam

**Situation.** The user asks for a reversible tone edit and opts out of a suggested check.

**Without proportionality.** An always-gating implementation may refuse to continue or add needless friction.

**With the skill.** Adaptive mode proceeds with the edit, records any relevant point as unverified, and does not claim confirmation.

**Value.** Keeps checkpoints rare enough that they remain credible when consequences matter.

## 7. Handoffs should carry understanding state

**Situation.** A user correctly explains a recommendation but never addresses its dependence on an unconfirmed vendor estimate.

**Without the skill.** A handoff summary flattens every premise into confident prose.

**With the skill.** The handoff separates confirmed conclusions, unverified assumptions, and conditions that require revalidation.

**Value.** Prevents understanding from being invented during summarization.

## 8. Understanding a number does not validate it

**Situation.** A model informally estimates monthly resource cost at CNY 420,000 without running a script, calculator, or spreadsheet. The user says, “I understand—I'll put the verified CNY 420,000 figure in the budget request.”

**Without the skill.** The user's acknowledgment launders a conversational estimate into an apparently verified result.

**With the skill.** The model keeps the figure labeled as an unverified estimate, surfaces the inputs, units, assumptions, and formula available, offers a reproducible calculation, and checks how the user will label or use the number before relying on it.

**Value.** Prevents evidence of comprehension from being mistaken for evidence that the underlying calculation is valid.

## 9. A confident citation is not a verified source

**Situation.** A model drafts a policy memo that cites a specific clause number and a supporting paper, both recalled from training rather than looked up. The user says, “Great—forwarding this to legal today.”

**Without the skill.** A plausibly formatted but wrong citation acquires the sender's endorsement and reaches people who will trust it.

**With the skill.** The model labels the references as unverified, distinguishes them from any source the user has checked, offers a deterministic lookup, and asks one focused question about which citations the user can personally stand behind before forwarding.

**Value.** Prevents citation hallucination from being laundered into a forwarding endorsement.

## 10. “Tests pass” is not “tests ran”

**Situation.** In a long working session, the model says, “The fix is in and the test suite passes.” No tool result in the conversation shows a run. The user says, “Then I'll merge.”

**Without the skill.** An unanchored execution claim becomes the basis for an irreversible action.

**With the skill.** The model states plainly that no anchored run exists in the session, labels the claim unverified, offers to run the suite, and checks what would make the user treat the work as mergeable.

**Value.** Prevents the user from being asked to vouch for something only a tool result can establish.

## Boundary: conversational evidence is not formal consent

Correctly explaining an automatic-renewal clause can support a conversational status of `confirmed`. It does not establish legal capacity or legally valid informed consent. The protocol produces calibrated evidence, not a certificate about the person.
