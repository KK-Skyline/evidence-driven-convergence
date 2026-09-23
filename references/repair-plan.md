# Root-cause repair plan

Read when turning confirmed findings into coding instructions. Keep this content in the existing review or handoff; simple fixes may use a short paragraph.

## Required evidence and decisions

1. **Failure and authority:** input or state, entry point, expected versus observed behavior, violated requirement or invariant, and impact. Link locations and available reproduction evidence. Distinguish observations from inference.
2. **Cause and escape:** explain the causal chain and the specific test assumption, mocked boundary, or unexamined consumer that hid it. “Insufficient testing” is not an explanation.
3. **Affected mechanism:** name the owning decision or state, callers and sibling paths inspected, justified exclusions, and remaining uncertainty. Bound any completeness claim by actual search scope.
4. **Repair direction:** state the smallest change removing the cause while preserving established semantics. Include dependencies when necessary; allow implementation freedom where evidence does not select a design.
5. **Acceptance:** specify the original regression, a discriminating sibling or boundary case where the cause applies, a valid success case, and relevant failure side effects. Explain inapplicable categories. Determine expected results independently of production logic.
6. **Closure:** identify required checks, unavailable evidence, and authorization scope. The coding agent returns actual evidence; proposed checks are not completed verification.

A special case for the reported input is insufficient if a confirmed sibling retains the defect. Prescribe a shared helper only when semantics are shared, not merely syntax.

## Worked example: shared mutable state

A sorted-list goal passes, but mutating a returned dictionary changes stored state. Establish the existing snapshot ownership contract from documentation or callers before calling this a defect.

Code cause: sorting copies the list but retains internal dictionaries. Escape cause: tests compare values immediately, never after mutation.

Inspect both list and single-item APIs against the shared store. Record whether both expose aliases; exclude an immutable count API after inspection.

Repair direction: enforce snapshot ownership at exposed boundaries. A shallow copy is sufficient only if the supported schema has no mutable nested values. Preserve storage, sorting, and public types unless the cause requires changing them.

Acceptance: mutate the list result and read through the single-item API; check the reverse direction if its ownership contract is the same. Preserve sorted output and ordinary updates. Include nested-value behavior only if the supported schema permits it.

The plan remains incomplete if ownership is assumed, the sibling API was not inspected, or deep copying is prescribed without establishing the data shape.

## Unknown cause

Use a diagnostic instruction: snapshot internal state before retrieval, after retrieval, and after mutation of the returned value. Identify which transition changes state and whether the change is intended. Attach available observations and a stop condition; label the cause unconfirmed until the experiment distinguishes it.
