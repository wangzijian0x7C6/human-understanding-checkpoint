# Checkpoint Patterns and Cases

Use these patterns as adaptable structures, not scripts. Match the user's language and the actual decision.

## Pattern library

### Brief teach-back

> Before we build on this, I want to make sure I explained the key distinction clearly. In your own words, what changes between A and B?

Use for conceptual dependencies. Avoid asking for a summary of everything.

### Real-next-step application

> You are about to do X. Based on the constraint we discussed, what will you do if Y occurs?

Prefer this over recall because it tests whether the person can use the information.

### Commitment check before forwarding

> This draft could be read as committing you to X. If the recipient asks what that means in practice, how would you explain it?

Use when generated wording may create obligations or overstate certainty.

### Assumption failure

> The recommendation depends on A. If A turns out not to be true, which part of the recommendation no longer follows?

Use for forecasts, plans, and advice with fragile premises.

### Contrast check

> The important distinction is easy to miss: is the result saying A, or only the narrower claim B? What would be unsafe to infer?

Use where a plausible but broader interpretation would be wrong.

### Repair after partial understanding

> You have the main recommendation right. One condition is missing: it applies only when X. How does your next step change when X is absent?

Name what was understood before correcting the gap.

### Respectful opt-out

> I haven't verified this point. We can continue without the checkpoint because the step is reversible, but I will keep the assumption marked as unconfirmed.

Do not imply confirmation after an opt-out.

## Worked cases

### 1. Forwarding an executive recommendation

Critical set:

- the recommendation;
- the evidence strength;
- the commitment implied by the draft.

Good checkpoint:

> Before you send this, what decision does the memo actually recommend, and which sentence is an estimate rather than an established fact?

Weak checkpoint:

> Do you understand the memo and approve it?

The weak version combines comprehension and approval and supplies no evidence for either.

### 2. Technical conversation with a dependency

The next implementation step depends on understanding that retries can duplicate a non-idempotent operation.

Good checkpoint:

> If the request times out after the server has already processed it, what could a blind retry do, and what property prevents that?

Once answered correctly, do not ask again unless the design changes.

### 3. High-consequence advice

Do not test the user's professional competence or claim that a successful answer makes the action safe. Check only the action-changing point and preserve any applicable expert-review requirement.

Good checkpoint:

> The important limitation is that this is general information, not a diagnosis. What would make you stop relying on it and seek qualified help?

### 4. Misconception versus disagreement

If the user says, “I understand the cost could double, and I still prefer the faster option,” treat the cost tradeoff as understood. Do not recheck merely because the choice differs from the model's recommendation.

If the user says, “The faster option has no cost downside,” repair the misconception because it changes the decision basis.

### 5. Trivial request

For “convert 3 PM Shanghai time to London time,” answer directly. Do not add a comprehension checkpoint unless the user explicitly requested always mode or the result controls a consequential deadline.

### 6. Plausible but unverified citation

The user is about to forward a draft that cites a specific statute, paper, or clause number the model generated from memory.

Good checkpoint:

> Before you send this, which of the cited references have you verified yourself, and what happens if the recipient checks the one we have not?

Weak checkpoint:

> Do you trust the citations?

The weak version asks for a feeling, not evidence. The strong version makes the user distinguish verified sources from model-recalled ones without demanding they audit every claim.

### 7. Unanchored execution claim

The model states that “the tests pass” or “the file is updated,” but no tool result in the conversation shows it. The next step depends on that claim being true.

Good checkpoint:

> The next step assumes the tests actually ran and passed. Where in this session did you see that confirmed, and what would you do first if it turns out they did not run?

Weak checkpoint:

> Are you sure the tests passed?

The weak version asks the user to vouch for something only an anchored tool result can establish. If no such result exists, say so directly and label the claim unverified instead of testing the user's confidence in it.

## Quality review

Before asking a checkpoint question, confirm:

- Would a wrong answer change the next action?
- Does the question test meaning or use rather than memory?
- Is one question enough?
- Can the user tell why the check matters?
- Is there a respectful path for partial understanding, accessibility needs, or opting out?
- Will a correct response end the checkpoint rather than trigger needless repetition?
