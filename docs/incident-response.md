# AI incident response

An AI incident is any event where an AI system produced or contributed to harm, a data exposure, a serious error reaching people, or behaviour outside its approved scope, including near-misses.

## Severity

`aigov incident` classifies using four facts: did harm reach people, was data exposed, did it repeat, is it contained.

| Severity | Typical trigger | Response |
|---|---|---|
| **SEV1** | Data exposure, or harm to people that is not contained | Pause the system now. Notify governance board and legal within 1 hour. Preserve the audit trail. |
| **SEV2** | Harm that is contained, or repeated errors not yet contained | Pause or restrict. Notify the process owner the same day. Root cause within 5 working days. |
| **SEV3** | Repeated but contained, no harm | Fix in backlog, add a test or control, review at the next board meeting |
| **SEV4** | One-off, contained, no harm | Log and watch the trend |

## First hour (SEV1 and SEV2)

1. **Contain.** Kill switch holder pauses the system or the affected path. Do not wait for the cause.
2. **Preserve.** Freeze logs and the tamper-evident audit trail. Record who did what and when.
3. **Assess.** Who is affected, what data, how many, is it still happening?
4. **Notify.** Owner, approver, governance board. Legal and the data-protection lead for any data exposure, who decide on regulatory and customer notification.
5. **Communicate.** One accurate internal message. Nothing external until legal agrees the wording.

## After the incident

Within 5 working days, a blameless review that answers:

- What happened, and how was it detected? How long did detection take?
- Which control should have caught it, and why did it not?
- What changes: a new test in the golden set, a tighter autonomy level, a new input check, a threshold change?
- Does the tier of this use case, or the intake weights, need to change?

Every incident ends with a control change or a recorded decision not to change one. Track repeat causes in a Pareto chart across incidents; recurring causes are governance defects.

## Detect early

- Control charts on first-pass yield and override rate catch drift before clients do.
- Make reporting easy and safe: a single channel, no penalty for raising a near-miss.
- Test the kill switch, and run a tabletop exercise for one SEV1 scenario each year.
