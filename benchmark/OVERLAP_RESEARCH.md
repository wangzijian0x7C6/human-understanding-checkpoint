# Related Skill and Overlap Research

Research date: 2026-08-29

## Conclusion

`human-understanding-checkpoint` is not a wholly new category. Public skills already implement substantial parts of the same idea, especially for risky software actions and educational mastery. No reviewed candidate combines the same general-purpose scope, adaptive triggering, topic-level understanding ledger, disagreement-versus-misunderstanding distinction, forwarding workflow, and dependent-step-only gating.

The closest prior art is `the-standard-comprehension-gate`. If both are installed, they should not independently quiz the user: use the domain-specific gate for consequential code actions and use `human-understanding-checkpoint` for general dialogue state, forwarding, and non-code decisions.

## Sources searched

- skills.sh leaderboard and Skills CLI searches for `human understanding`, `comprehension verification`, `teach back`, `socratic`, `teach to mastery`, and `comprehend`.
- Original GitHub repositories and `SKILL.md` files, pinned to the inspected commits.
- Adjacent human-in-the-loop and Socratic skills surfaced by skills.sh.

Install counts below are dynamic skills.sh figures observed on the research date. Repository stars are also snapshots, not quality guarantees.

## Mechanism comparison

| Candidate | Observed adoption | Overlap | What is shared | Material difference |
|---|---:|---|---|---|
| [The Standard Comprehension Gate](https://github.com/hassanhabib/the-standard-skills/blob/81ea651e83d9314029c1e791f49b79109a2f96e3/.skills/the-standard-comprehension-gate/SKILL.md) | 15 installs; repo 19 stars | High | “Understanding must be demonstrated, not asserted”; 1–3 risk-scaled questions; correct/partial/wrong assessment; repair and re-probe; proceed/hold/redesign; deliberate override | Restricted to hard-to-reverse software actions; questions must be codebase-anchored and deliberately resistant to copy-paste; no general conversation ledger, forwarding workflow, informed-disagreement handling, or adaptive non-gated mode |
| [comprehend](https://github.com/broomva/skills/blob/021001d99c74795ae1b982e5aeb7aa646f4a0412/skills/knowledge/comprehend/SKILL.md) | skills.sh adoption not captured | Medium–high | Agent-to-human mastery loop; human restates first; active recall; correct explained answer required; persistent checklist; re-teach and re-probe | A deep, interactive teaching workflow for existing code/session knowledge; intentionally cannot finish until every item is mastered; much heavier than a proportional checkpoint and not aimed at forwarding or ordinary decisions |
| [Teach-Back Evaluator](https://github.com/GarethManning/education-agent-skills/blob/6bbbce418f82e11044009c9f3b7373a354de5bd0/skills/student-learning/teach-back-evaluator/SKILL.md) | 78 installs; repo 506 stars | Medium | Teach-back, mechanism/example/contrast questions, misconception detection, repair and retry, explicit pass condition | Student-learning mode initiated by a learner; long novice-role session with numeric scoring; does not decide when normal agent output needs a checkpoint or govern downstream actions |
| [GodMode comprehension-check](https://github.com/NoobyGains/godmode/blob/441103a010f6d49d5fc26a0f4f2c6782a9d3dcff/skills/comprehension-check/SKILL.md) | 44 installs; repo 93 stars | Medium | Prevent cognitive debt from AI-generated code; explain what/why/context/hazard; require comprehension before commit | Code-only and walkthrough-first; its explicit confirmation step can still accept a self-report, so the verification loop is less rigorous than its stated indicators |
| [comprehension-review](https://github.com/danballance/agent-skills/blob/9d64b96993e1ea2b210de7080e56f4022885d4c1/skills/comprehension-review/SKILL.md) | 3 installs; repo 1 star | Low–medium | Code-grounded walkthrough, application/risk questions, non-trivia quiz, anti-infantilizing tone | Produces a self-contained HTML learning artifact with answers; it does not semantically assess the human's reply, maintain an understanding state, or gate a dependent action |
| [Cloud Byte comprehension-gate](https://github.com/cloud-byte-consulting/plugins/blob/bff0061865c1d299fc9bd8376626213bbd5572a9/prompt-workflows/skills/comprehension-gate/SKILL.md) | 2 installs; repo 0 stars | Low–medium | Blast-radius, assumptions, risks, and “questions before merging” | Primarily assesses whether a code change is comprehensible and produces CLEAR/REVIEW/HOLD; it does not verify the individual user's understanding through a response loop |

## Adjacent but not substitutes

- [Socratic Tutor](https://www.skills.sh/belsrc/skills/socratic-tutor) refuses to accept “I understand” without application or explanation, but it is an always-on zero-to-mastery teaching system and had 7 observed installs.
- [Checking for Understanding Protocol Designer](https://github.com/GarethManning/education-agent-skills/blob/6bbbce418f82e11044009c9f3b7373a354de5bd0/skills/explicit-instruction/checking-for-understanding-protocol-designer/SKILL.md) designs classroom-wide diagnostic questions and proceed/re-teach decisions; it is for teachers planning lessons, not an agent checking one collaborator.
- [loop-me](https://www.skills.sh/mattpocock/skills/loop-me) uses human checkpoints in workflow specifications, but its checkpoint asks a person to verify or decide; it does not require evidence that the person understood. It is highly adopted but solves governance and workflow placement rather than comprehension.

## What remains distinctive in this skill

1. **General interaction scope:** applies to decisions, forwarding, explanations, and dependent conversation—not only code or education.
2. **Adaptive proportionality:** light, active, and explicitly requested gated modes; low-stakes exchanges are normally left alone.
3. **Critical-understanding set:** limits verification to at most three action-changing propositions.
4. **Semantic state model:** confirmed, partial, misconception, and unverified, tracked by topic with conditions for revalidation.
5. **Disagreement separation:** explicitly treats “understands but chooses differently” as confirmed rather than failed.
6. **Forwarding workflow:** checks claims, commitments, and uncertainty before model-authored content is passed onward.
7. **Narrow progression control:** pauses only the step that depends on unverified understanding.
8. **Scope disclaimer:** does not claim legal consent, medical capacity, professional competence, or guaranteed comprehension.

## Recommended positioning

Keep the skill, but position it as a **general-purpose comprehension-state and interaction protocol**, not as the first comprehension gate in the ecosystem.

Add a future interoperability rule:

> When a domain-specific comprehension gate is already active, do not run a second independent quiz. Reuse its evidence in the topic ledger, and let the stricter domain-specific gate control the consequential action.

Consider acknowledging the related implementations in a `related-skills` reference. No inspected text needs to be copied into this skill; the current design can remain independently worded.
