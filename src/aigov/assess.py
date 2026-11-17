"""Risk-tier an AI use case from a short intake form and list the controls it needs.

This is a triage tool, not legal advice. It turns a conversation ("what could go wrong
and who signs off?") into a repeatable, auditable answer.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

# question -> weight. Yes-answers add the weight; weights reflect harm potential.
QUESTIONS = {
    "personal_data": 2,             # processes information about identifiable people
    "sensitive_data": 3,            # health, financial, biometric, children, etc.
    "affects_individuals": 3,       # output influences a decision about a person
    "customer_facing": 2,           # output reaches clients or the public unreviewed
    "no_human_review": 3,           # no person checks output before it takes effect
    "irreversible_action": 3,       # sends, pays, deletes, publishes
    "regulated_domain": 3,          # employment, credit, health, legal, insurance
    "third_party_model": 1,         # data leaves the organisation to a model provider
    "high_volume": 1,               # many decisions, so errors scale
}
# Block rule (in assess): a regulated-domain decision about people with no human review
# does not proceed without legal/compliance sign-off, whatever the score.

TIERS = [  # (minimum score, tier)
    (0, "low"), (5, "medium"), (10, "high"),
]

CONTROLS = {
    "low": ["Name an owner", "Register the use case", "Log inputs and outputs", "Annual review"],
    "medium": ["All low-tier controls", "Human review of a sample of outputs", "Defined escalation path",
               "Data-protection check on inputs", "Quarterly review", "Evaluation on a golden set before launch"],
    "high": ["All medium-tier controls", "Human approval before output takes effect",
             "Documented risk assessment and mitigation plan", "Bias and error analysis by segment",
             "Tamper-evident audit trail", "Incident runbook and kill switch with a named owner",
             "Monthly review and re-approval on material change"],
}
APPROVER = {"low": "Process owner", "medium": "Department head", "high": "AI governance board",
            "blocked": "Legal and compliance, then governance board"}

# NIST AI RMF core functions, as used in docs/nist-ai-rmf-mapping.md
RMF = {"GOVERN": "ownership, policy, accountability", "MAP": "context and risk identification",
       "MEASURE": "evaluation and monitoring", "MANAGE": "mitigation and incident response"}


@dataclass(frozen=True)
class Result:
    name: str
    score: int
    tier: str
    approver: str
    controls: list[str]
    reasons: list[str] = field(default_factory=list)


def assess(name: str, answers: dict[str, bool]) -> Result:
    unknown = set(answers) - set(QUESTIONS)
    if unknown:
        raise ValueError(f"unknown question(s): {sorted(unknown)}")
    missing = set(QUESTIONS) - set(answers)
    if missing:
        raise ValueError(f"unanswered question(s): {sorted(missing)}")  # no silent defaults
    if not all(isinstance(v, bool) for v in answers.values()):
        raise ValueError("all answers must be true or false")
    score = sum(w for q, w in QUESTIONS.items() if answers[q])
    reasons = [q for q in QUESTIONS if answers[q] and QUESTIONS[q] >= 3]
    tier = [t for lo, t in TIERS if score >= lo][-1]
    if answers["regulated_domain"] and answers["affects_individuals"] and answers["no_human_review"]:
        reasons.insert(0, "automated decision about people in a regulated domain with no human review")
        return Result(name, score, "blocked", APPROVER["blocked"],
                      ["Do not proceed until a human-in-the-loop design is approved by legal and compliance"], reasons)
    return Result(name, score, tier, APPROVER[tier], CONTROLS[tier], reasons)


def load(path: str | Path) -> list[Result]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [assess(item["name"], item["answers"]) for item in data]


# --- incident severity -----------------------------------------------------

def severity(harm_reached_people: bool, data_exposed: bool, repeated: bool, contained: bool) -> str:
    """SEV1 (act now) to SEV4 (log and learn)."""
    if data_exposed or (harm_reached_people and not contained):
        return "SEV1"
    if harm_reached_people:
        return "SEV2"
    if repeated and not contained:
        return "SEV2"
    return "SEV3" if repeated else "SEV4"


RESPONSE = {
    "SEV1": "Pause the system now (kill switch), notify the governance board and legal within 1 hour, preserve the audit trail.",
    "SEV2": "Pause or restrict the system, notify the process owner the same day, root-cause within 5 working days.",
    "SEV3": "Fix in the normal backlog, add a test or control, review at the next governance meeting.",
    "SEV4": "Log it and review in the periodic trend check.",
}
