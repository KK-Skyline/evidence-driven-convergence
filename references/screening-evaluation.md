# Evaluating and improving the handoff screen

The unit tests validate the adapter, not the model. Until Jev is configured, report live calls and evaluated model cases as zero. The development example is deliberately incomplete and must not be called a holdout.

## Collect before changing the rubric

Use actual repair proposals and their code/test evidence. Keep the original coding-review path. First run screening in shadow mode: its advice is logged separately and is not shown to the coding/review participants until they finish, so its predictions can be compared with what happened without changing that outcome. Obtain the user's agreement before withholding advice on live consequential work; isolated evaluation tasks are preferable.

Have a reviewer label plan gaps from independent inspection and later results, not from agreement with Jev. Labels may be gap, supported, not_applicable, or unresolved per question. Preserve disagreement instead of forcing a label. Existing documentation and required behavior define correctness; no model vote creates authority.

Keep one record per plan in an evaluation JSONL outside the packet:

```json
{"case_id":"case-001","split":"development","packet_sha256":"digest from result","request_sha256":"digest from result","rubric_version":"repair-screen-v1","model":"actual returned model","mode":"live","result_path":"local receipt","labels":{"affected_paths":"gap"},"label_evidence":["test or source reference"],"downstream":{"same_cause_reopened":null,"regression_introduced":null,"repair_batches":null},"review_seconds":null,"provider_input_tokens":null,"provider_output_tokens":null}
```

Null means unavailable, not zero. Use actual receipt usage; include failed or unavailable requests separately. In a future comparison with advice enabled, include screening, reading, verification and extra coordination in total cost, not just Jev request cost.

## Separation and freeze

Choose development and holdout cases by root-cause family before tuning; near-duplicate symptoms of one bug belong in the same split. Include adequate plans, uncertain evidence, out-of-scope suggestions and misleading claims, not only incomplete plans. Freeze case identities, labels, question text, script/skill hashes, and an available model version. No universal case-count quota makes a small sample sufficient.

Change a question or skill instruction only for a verified miss or false alarm in development cases. Retain a countercase where the old behavior was appropriate. Compare the old and new versions on the same untouched holdout. Once holdout feedback influences a revision, those cases become development data; reserve new holdouts. Do not use the existing self-authored toy cases as evidence of unfamiliar-task performance.

## Report denominators and abstentions

- Among adjudicated true gaps: counts of gap alerts, unknown/abstentions, and missed gaps (supported or not_applicable). Report all three; abstentions are not correct detections.
- Among adjudicated adequate aspects: false gap alerts and unknown answers separately.
- Unresolved reference labels and unavailable model responses remain outside accuracy calculations but visible in the totals.
- Record whether the alerted gap later caused a same-cause reopening, and whether acting on a confirmed alert changed that outcome in an authorized comparison. Prediction alone does not establish avoided rework.
- Report actual added review effort, total repair effort, and regressions. A reduction in visible repair batches can hide extra pre-review effort.

A new rubric is a candidate improvement until it performs acceptably on the declared holdout and preserves important countercases. On regression, retain the prior version and record the failed candidate. Publication of a new skill version is distinct from a positive evaluation result. No autonomous repeated tuning or scheduled monitoring is implied by this skill.
