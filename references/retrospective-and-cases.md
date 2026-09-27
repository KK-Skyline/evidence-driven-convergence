# Provenance and evaluation limits

## Source and user intent

The initial source was a private engineering retrospective. It reported disconnected runtime rules despite correct table counts, order-dependent errors, generic provenance, cache violations, and fragmented dispatch. These are reported observations; historical source code and logs were not independently audited here.

The user clarified that repeated coding-review ultimately completed the code. The concern is avoidable rework and superficial repairs. This skill provides preparation before review and causal repair guidance inside that loop; it neither replaces review nor adds an approval role.

Reported resource consumption was not independently measured. Contract size, test counts, and eventual completion cannot establish which scheduling decisions caused cost or success. Fixed node counts, mutant quotas, and project-specific cache rules are not universal requirements.

## Factual self-criticism behind this revision

| Observed weakness | Correction |
| --- | --- |
| Discovery emphasized goal setup and diagnosis after repeated failure. | Explicit pre-review and repair-planning triggers. |
| Root-cause advice lacked a checkable handoff standard. | Require code cause, escape cause, affected paths, repair direction, and acceptance evidence. |
| Review boundaries could remain dominated by the goal. | Follow engineering invariants through actual callers, ownership, failure paths, and consumers; separate new requirements. |
| The experiment measured defect detection only. | Preserve that narrow result; repair-plan quality remains a separate evaluation target. |
| General governance obscured repair instructions. | Keep the review sequence inline and disclose finding-specific guidance when findings exist. |

## Executed mechanism experiment

On 2026-09-21, a self-authored order validator exercise produced:
- Three deliberately weak tests accepting the seeded defective version.
- Eight behavioral tests and 4,374 bounded exact-output comparisons passing after one implementation edit.
- Four seeded single-fault variants passing weak tests and failing behavioral assertions.
- Frozen tests and a final passing rerun of the unchanged repaired implementation.

The experiment's raw commands and receipts are retained privately. They are not distributed as public evaluation data and are not a runtime dependency.

This demonstrates selected fault detection, not improved review handoffs, less long-term rework, or token savings. The author knew the faults and wrote the tests. It was neither blind nor a comparison against competent normal review.

## Executed repair-plan experiment

A second self-authored exercise on 2026-09-21 tested two APIs sharing a tier-insensitive price cache. A plan clearing the reported API's cache passed the original reproduction but failed four of seven frozen checks: three sibling/path-order defects remained and cache reuse regressed. A causal plan traced both APIs to the shared lookup and changed its key to include the tier; all seven checks passed with one implementation-line change. The plans were recorded before implementing the repairs, and test identities were preserved.

The private repair-plan report retains scope, plans, commands, and receipts. This demonstrates that the specified causal acceptance can reject a superficial repair in this case. It does not independently validate Agent handoffs or measure actual rework reduction: one author knew the seeded cause, and the comparator was deliberately incomplete. No additional mandatory rule was justified by this run.

## Evaluation cases for the revised workflow

These are prospective behavioral criteria, not independent Agent test results.

| Case | Observable acceptable behavior |
| --- | --- |
| Goal satisfied but returned values corrupt shared state | Establish ownership authority; inspect aliases and consumers beyond output assertions. |
| Two APIs expose the same mutable store | Inspect both and propose causal repair with cross-API acceptance, not just a patch to the reported API. |
| Cause remains uncertain | Specify a discriminating experiment rather than a guessed fix. |
| Reviewer requests a new feature | Separate the proposal from contract violations and preserve scope. |
| Small unrelated text edit | Use proportionate checks without a mutation quota or architecture audit. |
| Original regression passes but confirmed sibling remains broken | Keep the finding open and identify missing causal coverage. |
| Review criteria satisfied | Deliver and stop. |

A stronger future evaluation holds the coding-review loop constant and compares repair plans with and without this guidance on unfamiliar tasks. Assess verified causal coverage, missed affected paths, and same-cause reopenings. Follow delegation authorization, preserve failed cases, and use reliable measurements for cost claims.

## 2026-09-26 evidence routing and claim screening exercise

The [HEXIS preprint](https://arxiv.org/html/2609.30123) motivated separating local evidence judgments from review continuation rules. This revision adds explicit evidence-based routes to the skill and optional evidence-addressed claim questions to the existing Jev packet. These textual routes are not an executable state-machine runtime. Claim answers remain advisory, and the reviewer retains scope and closure decisions.

Nine self-authored adversarial cases in `tests/test_hard_cases.py` cover a one-caller symptom patch and its causal countercase, a circular test oracle, failed-operation side effects, nested aliasing, a documented live view, uncertain concurrency scope, superficially similar failures with different causes, and a trivial text edit. Six case probes execute code; two reuse the same shared-cache implementation. Frozen oracle labels are withheld from requests but were authored by the same person as the cases. Replay fixtures exercise response handling, not Jev judgment.

On this date, 22 unit tests and the skill validator passed. No Jev credential or callable Jev tool was available, so live requests, independent model decisions, blinded reviewer trials, and downstream repair comparisons remain at zero. This exercise supports packet construction, citation validation, advisory-only behavior, and selected runtime observations; it does not establish higher defect detection, fewer reopenings, calibrated probabilities, or token savings. The next efficacy test needs unfamiliar cases, independently adjudicated labels, a frozen holdout by cause family, and actual Jev calls where authorized.

An independent, read-only review after this exercise reproduced a request-amplification risk: a valid packet with 1,000 claims expanded to 1,005 questions and about 1.05 MB. It also identified an existing output-permission risk when default `umask 022` creates world-readable preparation receipts. A follow-up capped claims at 16 and created receipts with mode `0600`; the large packet now fails locally, a CLI receipt was observed at mode `600`, and 23 unit tests passed. The reviewer also noted that response validation accepts confidence values inconsistent with a flat probability distribution. Confidence is not an approval input and the provider's exact mapping is undocumented, so no numeric constraint was added. These findings and repairs concern operational boundaries, not Jev semantic efficacy.

A later compatibility audit checked the existing on-disk example, its pre-revision copy, this exercise's saved packet and three prepared receipts, the legacy packet generated by tests, and each of the nine generated case packets. All remained valid under the 16-claim limit, so no old packet needed rewriting. A permanent test now loads the on-disk legacy example, and the 16/17-claim boundary is exercised; 24 unit tests and skill validation passed. The audit covers discovered artifacts in relevant skill, workspace, and temporary locations, not an unrestricted filesystem inventory.
