# AI Governance Framework

A practical, lightweight governance model for AI use cases in a delivery organisation: **how to tier risk, who signs off, which controls apply, and what to do when something goes wrong**. It is built to be adopted by a real operations team, not to sit in a policy folder.

> This is an operating framework and a triage tool. It is not legal advice and does not by itself make a system compliant with any regulation. Use it to structure the conversation with legal, security and compliance.

## The model in one page

```
Use case intake (9 yes/no questions)
        |
   risk score ---- block rule (regulated decision about people, no human review) --> BLOCKED: legal + board
        |
   tier: LOW / MEDIUM / HIGH
        |
   controls for the tier  +  named approver  +  review cadence
        |
   run with monitoring --> incident? --> severity SEV1..SEV4 --> response
```

| Tier | Typical example | Approver | Key controls |
|---|---|---|---|
| Low | Internal meeting summariser | Process owner | Owner, register, logs, annual review |
| Medium | Onboarding assistant, client reply drafting | Department head | Output sampling, escalation path, data-protection check, evaluation before launch |
| High | Anything touching sensitive data or irreversible actions at volume | AI governance board | Human approval before effect, risk assessment, audit trail, kill switch, monthly review |
| Blocked | Automated shortlisting of candidates with no recruiter review | Legal and compliance first | Redesign with a human in the loop |

## Try it

```bash
pip install -e .
aigov assess examples/use_cases.json
aigov incident --harm --contained        # -> SEV2 and the response
```

```
Onboarding knowledge assistant: tier=medium score=5 approver=Department head
Candidate shortlisting agent: tier=blocked score=13 approver=Legal and compliance, then governance board
Candidate shortlisting with recruiter review: tier=high score=10 approver=AI governance board
```

Adding a recruiter review moves the same use case from *blocked* to *high*: governance pushes designs toward human oversight rather than just saying no.

## Design principles

1. **Risk-based, not blanket.** A meeting summariser and a hiring agent do not need the same process. Over-governing low-risk work kills adoption; under-governing high-risk work causes incidents.
2. **No silent defaults.** An unanswered intake question is an error, not "no". People who are unsure must find out.
3. **Governance should make good designs easier.** Human review removes the block, so teams are rewarded for building oversight in.
4. **Named humans.** Every tier has a named approver and every system has an owner and a kill-switch holder.
5. **Evidence over assertion.** High-tier systems keep a tamper-evident audit trail (see [`agentflow-hitl`](https://github.com/MohitBhatnnagar/agentflow-hitl)) and evaluation results (see [`ai-quality-and-evals`](https://github.com/MohitBhatnnagar/ai-quality-and-evals)).

## Documents

- [docs/nist-ai-rmf-mapping.md](docs/nist-ai-rmf-mapping.md): how each part maps to the NIST AI Risk Management Framework functions.
- [docs/operating-model.md](docs/operating-model.md): roles, the governance board, review cadence, and the approval matrix.
- [docs/incident-response.md](docs/incident-response.md): severity levels, first-hour actions, and post-incident review.

## Tests

18 tests cover tier boundaries, the block rule, validation, the example use cases and incident severity.

```bash
python -m unittest discover -s tests -v
```

## Limits

- The weights are a starting point. Calibrate them against your own incident history and review them yearly.
- A questionnaire cannot find risks nobody thought to ask about. Pair it with a short design review for medium and high tiers.
- Regulatory duties (for example data protection law, sector rules, or the EU AI Act's risk categories) depend on jurisdiction and facts. Treat the tiers as a prompt for legal review, not a determination.

## License

MIT
