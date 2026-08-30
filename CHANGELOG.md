# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Changed

- Generalized the unverified-estimate protocol beyond quantitative reasoning to four more known LLM reliability limitations: traceable references (citations, statutes, clause and API names), current-state facts that may predate the knowledge cutoff, execution claims without an anchored tool result, and extracted detail from images, PDFs, tables, or long documents.
- The forwarding workflow now also checks that hedges and estimates survive the user's restatement.
- Added two worked cases to the runtime patterns reference: plausible but unverified citations, and unanchored execution claims.

### Evaluation

- Ran the required paired blinded evaluation for this runtime change (public regression suite, 23 cases × 2 repeats, both arms, codex-cli 0.147.0 as generation model and same-family blind judge, seed 20260829). Skill-arm primary score held at 0.970 with zero hard failures in both runs; the paired delta was +0.128 before and +0.095 after, with the post-change gate miss (+0.095 vs +0.10 threshold) traced by unblinding to control-arm variation on unchanged cases and judge wording variance, not to any behavioral regression. Per the standing decision above, this public suite records regression only; the five-category generalization still requires a newly created sealed holdout.

### Fixed

- Aligned the README revalidation triggers with the full list in SKILL.md (user contradiction and elapsed time or context, in addition to changed facts, assumptions, or required precision).
- Corrected the project-layout description of `docs/` to match its actual contents (value cases only).

## [0.2.0] - 2026-08-29

### Added

- Separated human understanding from underlying content validity.
- Required consequential model-derived numbers without reproducible calculation to remain labeled as unverified estimates, with a checkpoint on their intended use.
- Added two public regression cases for quantitative validity boundaries.

## [0.1.1] - 2026-08-29

### Changed

- Reframed the README benchmark section as a preliminary evaluation rather than efficacy evidence.
- Elevated the non-significant paired test and measurement limitations.
- Reclassified the now-public case suite as a regression set for future revisions.
- Documented stronger baselines, sealed holdouts, cross-family judging, human calibration, and participant studies needed for future claims.

## [0.1.0] - 2026-08-29

### Added

- Adaptive, always, and explicitly gated understanding-checkpoint modes.
- Semantic understanding states and conditional topic ledger.
- Forwarding workflow and domain-gate interoperability rule.
- Runtime checkpoint patterns and worked cases.
- Paired, blinded 21-case benchmark with development and held-out splits.
- Directional mixed and held-out pilot reports.
- English and Simplified Chinese project documentation.
- Self-contained validation, tests, and GitHub Actions workflow.
