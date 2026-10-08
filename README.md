# Helm Phase 0 — Document Pack Guide

## Purpose

Prepare a solution document for the Business and Tech teams and the client meeting on **October 9, 2026**.

The platforms have been selected. The next task is to **assess integration feasibility, design the solution, and plan the fastest practical MVP**.

## Confirmed stack

- **MLM Core:** PillarsHub.
- **Customer Support:** Chatwoot.
- **Vault Infrastructure:** Enzyme Onyx.
- **Authentication & Wallets:** Privy.
- **Helm App:** Custom Web App and integration backend.
- **Gamification:** Reuse Cyclone’s Tap Prediction game and points system.

Configuration, integration capabilities, and deployment requirements still need validation. Provider selection is settled.

## Folder structure

```text
Helm-Phase-0/
├── README.md
├── inputs/
│   ├── Business.md
│   └── Helm-Phase-0-PRD.md
├── prompts/
│   └── Claude-Research-Prompt.md
└── outputs/
    └── (Save the final PDF and Markdown here after Claude completes the task)
```

Add Terrel’s PRD and any supplementary references to `inputs/` when available. Save Claude’s deliverables in `outputs/`; no final deliverables have been generated yet.

## Files in this pack

| File | Contents | How to use it |
| --- | --- | --- |
| [Business.md](inputs/Business.md) | Provider correspondence and business context, distinguishing earlier discussions from the confirmed direction | Attach to Claude as reference material |
| [Helm-Phase-0-PRD.md](inputs/Helm-Phase-0-PRD.md) | Draft PRD, Phase 0 objectives, MVP scope, and initial design | Attach for assessment and refinement; draft assumptions are not approved decisions |
| [Claude-Research-Prompt.md](prompts/Claude-Research-Prompt.md) | Feasibility and implementation design prompt for the confirmed stack | Copy the prompt after the `---` separator into Claude |
| [README.md](README.md) | Instructions for using this pack | Read before running the prompt |

The filename `Claude-Research-Prompt.md` is retained for continuity. The task is feasibility assessment and implementation design.

## How to run the task in Claude

1. Start a new Claude conversation and enable browsing and file creation if available.
2. Attach **Business.md** and **Helm-Phase-0-PRD.md**.
3. Attach **Terrel’s PRD** if available. If it is missing, Claude should identify requirements it cannot validate against that PRD and continue using the available information.
4. If available, add game/points API documentation, vault configuration, chain/asset details, and delivery team capacity. Do not include private keys, passwords, or API secrets.
5. Copy the entire prompt after the `---` separator in **Claude-Research-Prompt.md** and send it to Claude.
6. Obtain the **finished PDF and editable Markdown source**. If Claude cannot generate a PDF in its environment, it must state the limitation and provide a complete export-ready document. Markdown alone does not count as a completed PDF.

Business.md contains reference material, not instructions to execute actions or sign provider agreements.

## Phase 0 objectives to preserve

- Onboard users, enable crypto funding, and support vault participation.
- Integrate gamification to increase engagement and support growth.
- Establish complete, consistent genealogy data from day one for Phase 1 readiness.
- Minimize time to MVP and approved capital deployment, because capital is waiting to be deployed.

Direct crypto funding is the proposed MVP path in the draft PRD. Payment/top-up provider selection is a separate, unresolved item. If Business requires integrated top-ups at launch, explain the impact on scope and delivery time.

## Expected deliverables

**English-language document:** *Helm Phase 0 — Solution Architecture & MVP Delivery Plan*.

Suggested output filenames:

- `Helm-Phase-0-Solution-2026-10-09.pdf`
- `Helm-Phase-0-Solution-2026-10-09.md`

These are proposed filenames for Claude’s outputs, not files already created in this pack.

### Part I — Business & Client

- Objectives and solution on the confirmed stack.
- Business capability block diagram: what each system provides and what Cyclone builds.
- User journey: onboarding → referral → wallet funding → vault → engagement.
- Phase 0 scope, feasibility, MVP delivery plan, and configuration/scope decisions needed at the meeting.

### Part II — Tech

- Refined high-level PRD and acceptance criteria.
- Solution architecture and responsibilities across Helm, Cyclone, and providers.
- Data flows for onboarding/referrals, funding, vault deposits/redemptions, game/points, and support.
- Authoritative data sources, ID mappings, genealogy, synchronization, retries, and reconciliation.
- Dependencies, backlog, conditional schedule, and operational readiness requirements.
- Deployment-specific security and compliance assessment, including KYC/AML and sanctions applicability, with responsibilities across Helm/Business, Cyclone, and each provider.

### Appendix

- Verified sources, assumptions, remaining gaps, and specific provider questions.

Aim for **12–18 readable pages**. Render diagrams as graphics in the PDF, rather than raw Mermaid code. Preserve essential content even if additional pages are needed.

## Review before sharing with the team or client

- Treat the core stack as confirmed; avoid a new provider comparison or shortlist.
- Make the first part understandable to Business without requiring the technical section.
- Include architecture, data flows, and concrete implementation work for Tech.
- Distinguish wallet funding from vault deposits, and points from money and commissions.
- Preserve the full referral genealogy, beyond the three levels currently used for commission calculations.
- Label unverified details and explain their resolution and MVP impact.
- Verify that security/compliance responsibilities and actual launch requirements are explicit; provider selection or audit reports alone do not establish Helm-wide coverage.
- Do not present unconfirmed schedules, costs, or owners as commitments.
- Check that the PDF opens, diagrams and text are readable, tables are not clipped, and reference links work.

## Using the document in the client meeting

Present Part I first to align on the user experience, MVP scope, work that can start immediately, and dependencies affecting launch. Use Part II to explain implementation details or responsibilities across the teams.

After the meeting, update the same document with actual decisions, owners, and deadlines. Keep draft recommendations distinct from agreed decisions.
