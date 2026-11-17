# Governance operating model

## Roles

| Role | Responsibility |
|---|---|
| **Use-case owner** | Accountable for outcomes, completes the intake, keeps the register entry current |
| **Approver (by tier)** | Process owner (low), department head (medium), governance board (high) |
| **Governance board** | Small, cross-functional (operations, security, legal or compliance, data, a business lead). Meets monthly, plus ad hoc for SEV1 and SEV2. Decides high-tier approvals and policy changes |
| **Kill-switch holder** | One named person per system who can pause it without a deployment |
| **Reviewers** | Sample outputs and record defects; calibrated against each other |

## Approval matrix

| Decision | Low | Medium | High | Blocked |
|---|---|---|---|---|
| Start building | Owner | Owner | Owner, with design review | Not allowed |
| Launch | Process owner | Department head | Governance board | Legal and compliance, then board |
| Material change (new data, new model, wider audience) | Owner | Department head | Governance board re-approval | n/a |
| Pause | Anyone with the kill switch | same | same | n/a |
| Retire | Owner | Owner | Board informed | n/a |

## Cadence

- **Per use case:** annual (low), quarterly (medium), monthly (high) review of metrics, incidents, overrides and changes.
- **Governance board, monthly:** new high-tier requests, incident review, metrics across the portfolio, policy updates.
- **Quarterly:** recalibrate the intake weights against incidents and near-misses. Publish the register summary to leadership.

## The register

One row per use case: name, owner, tier, approver, date approved, model and provider, data used, controls in place, review date, status. If a system is not in the register it is not approved. The register is the single source for audits.

## Keeping it adoptable

- Intake takes ten minutes. Low-tier approval is a same-day decision by the process owner.
- Publish approved patterns (for example "internal summariser with a third-party model") so teams can reuse them without a full review.
- Track time-to-approve per tier. If it grows, governance is becoming the bottleneck and teams will route around it.
