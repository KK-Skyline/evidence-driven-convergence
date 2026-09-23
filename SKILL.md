---
name: evidence-driven-convergence
description: Pre-review assurance for coding changes, and root-cause repair planning when review finds defects or repeated false greens. Strengthen the existing coding-review loop through runtime evidence, affected-path checks, and actionable repair criteria.
---

# Evidence-driven review assurance

Apply before a substantive review and when converting findings into repairs. Strengthen the existing coding-review loop; preserve its roles and approval boundaries. This skill provides decision guidance, not automatic enforcement or a reliability guarantee. A review request authorizes investigation, not implementation.

## 1. Establish the review boundary

Inspect the actual change, relevant project authority, tested checkout and dirty-file state. Identify claimed behavior, real entry points, direct callers, state owners, and downstream consumers.

Use two lenses:
- **Requirement correctness:** Does the change satisfy the current goal and product contract?
- **Engineering integrity:** Can affected paths violate existing invariants through interactions, failure handling, shared state, alternate callers, or misleading tests?

Follow concrete dependencies beyond the diff where necessary. Distinguish existing invariant violations from new product requests; general hardening belongs in recommendations unless evidence establishes an in-scope defect.

**Done when:** a few lines in the existing review record identify affected paths, relevant invariants, reasoned exclusions, and unresolved authority or evidence gaps.

## 2. Challenge the evidence before trusting green

Trace every material correctness claim from an authorized entry point through its decision to observable results. Use the component API when production integration is deliberately excluded.

For each claim identify:
- its requirement or invariant and an independently determined expected result;
- the test or observation exercising the real path;
- a plausible wrong implementation that the current check would miss;
- a distinguishing check and its result, or the explicit evidence gap.

Choose checks based on actual exposure: error precedence and ties; exact provenance; failed-operation side effects; aliases and later consumers; limits before expensive work; relevant exceptions, cancellation, and alternate paths. Inspect interactions that share state or decisions.

Counts, coverage, table presence, hashes, and source searches prove only their specific structural claims. Expectations computed from production policy cannot independently validate that policy. Inspect mocks for bypassed decisions and failure assertions for outputs and state, not just error codes.

Prefer a small real-entry reproduction. For weak evidence on high-risk claims, use a targeted negative test or an authorized isolated production-only mutant with fixed tests. A valid mutant fails the intended behavior assertion; preserve baseline, exact change, and restored passing evidence. No universal test or mutant quota applies.

**Done when:** every material claim has inspected evidence or an explicit gap. Record already-correct behavior honestly; an unavailable reproduction is not fabricated into RED.

## 3. Produce causal repair instructions

Classify findings: existing missed defect, repair regression, changed requirement, faulty oracle, environment failure, or unresolved suspicion. Attach trigger, expected versus observed behavior, code location, impact, and evidence status. Source-level evidence can establish a defect when execution is unavailable; disclose unrun checks.

For confirmed findings, read [repair-plan.md](references/repair-plan.md) before issuing coding instructions. Investigate both:
- **Code cause:** the decision, data ownership, or ordering producing the failure.
- **Escape cause:** why previous tests or review could accept it.

Search callers and sibling implementations of the demonstrated mechanism, including relevant paths outside the diff. Record shared causes, inspected exclusions, and uncertain paths. Group symptoms by demonstrated cause, not merely similar wording.

An uncertain cause calls for a bounded diagnostic experiment with a discriminating outcome, rather than a speculative patch prescription.

**Done when:** every actionable finding has a causal repair plan and falsifiable acceptance criteria, or is explicitly an investigation. “Fix this case and add a test” is insufficient.

When Jev-assisted handoff screening is requested, read [jev-screening.md](references/jev-screening.md) before sending the plan to Coding. This optional advisory check does not replace this review or add an approval role; without Jev access, continue the existing review and record screening as unavailable.

## 4. Verify closure inside the existing review

When implementation is authorized, repair the shared mechanism and retain relevant tests. Reproduce the original defect, check mapped sibling paths, legitimate success cases, and failure side effects. Support oracle corrections with independent authority.

At re-review, compare the repair with its causal plan and inspect the new diff for introduced defects. The original reproduction passing cannot close a finding whose confirmed mechanism survives elsewhere. Record actual commands, exit codes, results, untested boundaries, and tested file identities.

Repeated failure of the same mechanism triggers call-chain and oracle reassessment before another similar patch. Classify new findings; discovering more defects alone does not prove review ineffective.

**Done when:** the causal mechanism and specified regression boundaries have evidence, with residual gaps explicit. Keep implementation complete, tests passed, review accepted, and release authorized separate. A turn ending is a handoff event, not acceptance.

## 5. Improve from observed escapes, then stop

For a defect escaping this process, locate the failed decision or missing check in the review record. Make a narrow skill correction only when editing is authorized; otherwise propose it. Check the observed case and a relevant countercase where extra work is unwarranted.

Separate evidence quality from efficacy: detecting a seeded bug proves detection for that case, not reduced cost. Where records exist, track repeated root causes, same-cause reopened repairs, and repair-plan omissions. Claim time or token savings only with reliable measurements and a meaningful comparison.

Stop at the authorized review or repair completion criteria. When requirements conflict or scope must change, pause affected work and continue independent authorized work. Preserve the normal coding-review process without another approval layer or endless self-criticism.

**Done when:** the existing review contains actionable findings, evidence gaps, and actual status. A no-finding outcome is legitimate; report inspected scope and limitations.

For provenance, experiments, and evaluation limits, read [retrospective-and-cases.md](references/retrospective-and-cases.md) only when evaluating or revising this skill.
