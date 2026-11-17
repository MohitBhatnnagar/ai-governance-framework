# Mapping to the NIST AI Risk Management Framework

The [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) organises AI risk work into four functions: **Govern, Map, Measure, Manage**. This framework implements a small, concrete slice of each. The mapping is a guide to where each practice sits; it is not a claim of conformance.

| RMF function | Intent | What this framework provides | Where |
|---|---|---|---|
| **GOVERN** | A culture and structure of accountability | Named owner per use case, tiered approvers, governance board, review cadence, kill-switch holder | `operating-model.md`, `CONTROLS`, `APPROVER` in `assess.py` |
| **MAP** | Understand context and identify risk | Nine-question intake covering data, affected people, customer exposure, reversibility, regulated domain, third-party model, volume | `QUESTIONS` in `assess.py` |
| **MEASURE** | Evaluate and monitor | Golden-set evaluation before launch (medium and up), output sampling, error analysis by segment (high), control charts on yield and override rate | `ai-quality-and-evals` |
| **MANAGE** | Prioritise and respond | Control sets per tier, block rule, incident severity and response times, post-incident review | `incident-response.md`, `severity()` |

## Practices by lifecycle stage

| Stage | Practice | RMF |
|---|---|---|
| Idea | Intake form completed by the proposer; tier assigned | Map |
| Design | Human-in-the-loop design agreed for medium and high; data-protection check | Map, Govern |
| Build | Evaluation on a frozen golden set; tests for guardrails | Measure |
| Launch | Approver sign-off recorded; kill switch tested; audit trail on | Govern, Manage |
| Operate | Sampling, drift monitoring, monthly or quarterly review by tier | Measure |
| Incident | Severity classification, response, root cause, control update | Manage |
| Retire | Decommission checklist, data deletion, register updated | Govern |

## Trustworthiness characteristics

The RMF describes trustworthy AI as valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias managed. How this framework addresses them:

- **Valid and reliable:** pre-launch evaluation and ongoing statistical monitoring.
- **Safe:** autonomy limits, human approval for irreversible or high-impact actions, kill switch.
- **Secure and resilient:** tool allow-listing, input validation and untrusted-output handling (see `ops-mcp-server`, `agentic-ai-patterns`).
- **Accountable and transparent:** named owners and approvers, audit trail, register of use cases.
- **Privacy-enhanced:** data-protection check; minimising what is sent to third-party models.
- **Fair:** bias and error analysis by segment for high-tier systems.
- **Explainable:** decision logs that show inputs, confidence and who approved.
