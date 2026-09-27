# Changelog

## 2026-09-27

### Review workflow

- Added evidence-based routing for unclear authority, missing observations, confirmed defects, uncertain causes, repair handoffs, and closure. Reviewer judgment and implementation authorization remain separate.
- Kept the routing as guidance within the existing coding-review loop. It is not a HEXIS-style executable state-machine runtime.

### Optional Jev screen

- Added optional, evidence-addressed `claims` questions alongside the five standing repair-plan questions. Each claim names a focus and cited evidence IDs; the claim text stays in request data rather than the question instruction.
- Bumped the receipt rubric identifier to `repair-screen-v2`. Existing packets without `claims` still validate and generate the same five questions; their receipt version changes. Packets with more than 16 claims now fail explicitly to bound request amplification and potential provider cost.
- Created result files exclusively with owner-only `0600` permissions. This protects local prepared requests and receipts that may contain source or log excerpts on file systems honoring POSIX modes.

### Tests and evidence

- Added nine self-authored adversarial review cases, executable probes for selected observations, and regression checks for legacy packets, the 16/17-claim boundary, malformed responses, and non-approval despite a confident wrong label.
- Verified 24 standard-library tests and the skill structure validator before publication. Independent read-only reviews reproduced the request-size and local permission risks, then checked their targeted repairs. The review cases and replay fixtures do not measure Jev accuracy or real-world review efficacy; no live Jev call was made.
