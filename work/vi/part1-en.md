---
title: "Helm Phase 0: Solution Architecture & MVP Delivery Plan"
subtitle: "Client meeting, 9 October 2026"
author:
  - Cyclone
date: "Draft for discussion · v0.1 · evidence verified 8 October 2026"
lang: en
toc: true
toc-depth: 1
---

# How to read this document {.unnumbered}

**Part I** (sections 1–8) is for Business and the client. It explains what Members can do, which platform supplies each capability, what Cyclone builds, how fast an MVP can credibly launch and which decisions are needed at the meeting. It does not require the technical sections.

**Part II** (sections 9–15) is for the Tech teams. It refines the PRD and specifies the architecture, data flows, genealogy model, backlog, launch gate and responsibilities.

**The appendix** holds evidence links, assumptions, unresolved details and questions for providers.

Labels used throughout:

| Label | Meaning |
|---|---|
| **Verified** | Read in the provider's own documentation, API specification, contract source or pricing page on 8 October 2026 (links in Appendix A). |
| **Correspondence** | Stated in provider correspondence supplied by Business; not independently verified. |
| **Recommended** | Cyclone's proposed design or default. Not yet approved. |
| **TBD** | Assumption or open item. Needs a decision or provider confirmation. |

The stack is confirmed: **PillarsHub** (MLM core), **Privy** (login and wallets), **Enzyme Onyx** (vault infrastructure), **Chatwoot** (support), Cyclone's **Tap Prediction game and points**, and a custom **Helm Web App** with its backend. This document does not compare or reselect providers. Terrel's PRD was not available; requirements that could not be checked against it are listed in Appendix B.

# Part I: Business and client {.unnumbered}

# Executive overview

**The confirmed stack can deliver Phase 0.** Every capability the draft PRD asks for is available from a confirmed provider or needs only configuration and a small amount of Cyclone integration work. No evidenced blocker requires changing a provider.

**What Members will be able to do in the MVP:**

1. Join Helm through an invite link, with their Sponsor recorded permanently from day one.
2. Log in with email or social login and receive a Helm wallet automatically. Only the Member can move its funds.
3. Fund that wallet by sending USDC on one network from any exchange or wallet.
4. Read the vault terms, deposit into the approved vault, see their confirmed position, and request a Redemption.
5. Play the existing Tap Prediction game and earn Points, which have no cash value.
6. Chat with support from inside the app, with support seeing who they are but never their keys.

**Why this is the fastest credible path:**

- **Cyclone builds only the glue:** the member experience, one backend that connects the providers, a ledger of member identities, referrals and events, and the reconciliation and admin views that make money flows auditable.
- **Each provider does what it already does:** Privy runs login and wallets; PillarsHub stores the genealogy and later calculates Commissions; Onyx issues vault shares and runs deposit and redemption queues; Chatwoot handles conversations.
- **Direct crypto funding** avoids any payment-provider onboarding on the critical path.

**What can start immediately (no provider or legal answer needed):** the Helm Web App shell, Privy login and wallet creation, the member and referral data model, the PillarsHub staging sync, the Chatwoot widget, chain indexing, and the full deposit and redemption journey on Enzyme's Sepolia test network.

**What gates live funds** (none of these blocks the build):

1. **The vault strategy and its Manager.** Onyx is vault infrastructure, not a strategy. Someone must be appointed to run the strategy, report the vault's value and return liquidity for Redemptions. Verified.
2. **Vault ownership and Enzyme's upgrade rights.** The vault Owner and Admins are fully trusted by the protocol, and Enzyme can upgrade vault contracts. The owning entity, a multisig and the upgrade terms in the licence agreement must be settled. Verified.
3. **Enzyme's licence agreement (MLA) and commercial terms.** Production use requires a commercial agreement. The public price differs from the quoted terms. Verified.
4. **Legal applicability review** of the operating entity, launch countries, KYC tier and vault terms. No confirmed provider supplies usable KYC or screening for this model.
5. **Provider acceptance of the business model**, in writing, from Privy, Enzyme and PillarsHub.

**Earliest credible schedule (estimate, not a commitment):** a working end-to-end test slice about 3 weeks after kickoff, and an MVP ready for a controlled launch in about **8–12 weeks**, provided the vault, licence and legal answers arrive by around week 6. Section 6 gives the assumptions.

# Confirmed stack: what each system provides

```{.mermaid #fig-capabilities caption="Business capabilities, the platform that provides each, and what Cyclone builds."}
flowchart TB
  subgraph Member capabilities
    A[Join with referral] --- B[Wallet] --- C[Fund wallet] --- D[Vault deposit and redemption] --- E[Games and points] --- F[Support]
  end
  A --> PH[PillarsHub: genealogy]
  B --> PV[Privy: login and wallets]
  C --> CH[Blockchain: USDC transfer]
  D --> ON[Enzyme Onyx: vault shares and queues]
  E --> GM[Cyclone game and points]
  F --> CW[Chatwoot: conversations]
  PH & PV & CH & ON & GM & CW --> HB[Helm Web App and backend, built by Cyclone]
```

| Capability | Provided by | Cyclone builds | Status |
|---|---|---|---|
| Join and log in; one stable Helm identity | Privy (login, identity token) | Member record, Privy-to-Helm mapping | Feasible |
| Wallet | Privy embedded wallet, owned by the Member; gas sponsored by Helm | Wallet screens; balance display | Feasible |
| Referral and genealogy | PillarsHub (customer with sponsor, Unilevel tree, full-tree export) | Referral capture, validation, sync, reconciliation | Feasible with configuration |
| Wallet funding | Blockchain (USDC transfer to the Member's address) | Address display, confirmation tracking, screening | Feasible |
| Vault deposit and redemption | Enzyme Onyx (allowlisted deposit queue, redemption queue, shares, public read API) | Terms screens, transaction flows, status tracking, allowlist updates | Feasible with configuration; **live use blocked** pending strategy, MLA and ownership |
| Games and Points | Cyclone Tap Prediction and points service | Account linking, verified events, Points display | **Feasible pending** game API documentation |
| Support | Chatwoot Cloud (web widget with identity validation) | Widget embedding, identity signing | Feasible |
| Operations | Provider dashboards (Onyx Admin App, PillarsHub Portal, Chatwoot) | Helm admin: exceptions, reconciliation, audit log | Feasible |

# The Member journey

```{.mermaid #fig-journey caption="Main Member journey. Wallet funding and vault deposit are separate steps; Points are separate from money."}
flowchart LR
  I[Invite link] --> S[Sign up and log in] --> W[Wallet created] --> F[Fund wallet with USDC] --> T[Read vault terms] --> V[Deposit request] --> P[Position confirmed] --> G[Play and earn Points] --> R[Request Redemption]
```

1. **Invite and signup.** The Member opens a Sponsor's invite link and logs in with Privy. Helm records a pending referral and confirms it once PillarsHub accepts it.
2. **Wallet.** Privy creates an embedded wallet. Only the Member can sign with it; Helm and Privy cannot move its funds.
3. **Wallet funding.** Helm shows one supported network and asset (recommended: USDC on Arbitrum) and the Member's address. Funding moves money into the Member's own wallet; it is **not** an investment and creates no Commission eligibility.
4. **Vault deposit.** The Member reads the vault terms, fees and risks, then signs two transactions: permission for the vault to take the amount, and the deposit request. The request is pending until vault operations process it at the next valuation. Only then does the Member hold vault shares.
5. **Position.** Helm shows the confirmed share balance and its value as of the vault's last valuation, with the valuation date.
6. **Engagement.** The Member plays Tap Prediction and earns Points. Points have no cash value and do not affect vault positions or Commissions.
7. **Redemption.** The Member requests a Redemption. It is processed by vault operations when liquidity is available; Helm shows each stage. There is no protocol-guaranteed processing time, so Helm must publish an operational target.

# Phase 0 scope

| In scope | Deferred unless Business requires it at launch |
|---|---|
| One network and one funding asset (recommended: USDC on Arbitrum One) | Integrated purchase or top-up (Paymenture or similar) |
| One approved Onyx vault, asynchronous deposits, queued Redemptions | Additional chains, assets or vaults; instant deposits |
| Privy embedded wallets with sponsored gas | Server wallets, automated strategies, policies |
| Referral capture and full genealogy in PillarsHub | Commission accrual and payouts (decision D2) |
| Existing Tap Prediction game and Points | New games, tokens, Points redemption for value |
| Chatwoot web chat | Telegram and WhatsApp support |
| Helm admin for exceptions, reconciliation and audit | Duplicating provider dashboards |
| Sanctions screening of wallet addresses; country eligibility; Member terms | Full KYC unless counsel requires it (decision D6) |

# Feasibility summary

| Area | Verdict | Key evidence | What remains |
|---|---|---|---|
| Login and identity | **Feasible** | Privy issues verifiable identity tokens; one Privy user maps to one Helm member. Verified. | Confirm Privy accepts the business model. |
| Wallet | **Feasible** | User-owned embedded EVM wallet; Arbitrum supported; native gas sponsorship; key export. Verified. | Losing the only login method loses the wallet; offer a second login method. |
| Genealogy | **Feasible with configuration** | Customer records take a Helm-defined ID and the sponsor at creation; the whole tree can be listed with an as-of date. Verified. | Confirm auto-placement in the tree, depth limits, sponsor-correction method, token permissions. |
| Commissions (Phase 1 readiness) | **Feasible** | Payable depth is set in the plan, not the tree; custom volume types exist; payouts are a separate step. Verified. | Decide whether anything accrues in Phase 0. |
| Wallet funding | **Feasible** | Standard USDC transfer; Helm indexes the chain. | Choose network and asset. |
| Vault deposit and redemption | **Feasible with configuration; live use blocked** | Allowlisted deposit queue; Member must sign; admin executes after valuation; queued Redemptions; read-only API. Verified. | Strategy and Manager, MLA, ownership, upgrade terms, operating process. |
| Games and Points | **Feasible pending evidence** | No game documentation supplied. | API documentation, event verification and abuse controls. |
| Support | **Feasible** | Web widget with signed identity; Cloud plans from $19 per agent per month. Verified. | Choose plan; confirm US data hosting is acceptable. |
| Compliance tooling | **Gap within the stack** | No confirmed provider offers usable KYC or screening for this model. | Counsel decision; add a screening service at the Helm backend if required. |

# MVP delivery plan

Delivery is organised so that engineering never waits for provider or legal answers. Those answers gate **live funds**, not the build.

| Stage | Duration (estimate) | Outcome | Gate to next stage |
|---|---|---|---|
| 0. Access and decisions | Week 1 | Meeting decisions recorded; PillarsHub staging, Privy app, Chatwoot, Onyx Sepolia vault and game docs in hand | Access confirmed |
| 1. Thin end-to-end slice | Weeks 1–3 | On test networks: invite → signup → wallet → referral accepted in PillarsHub → funding → deposit request → executed position → Redemption; one game-to-Points flow | Slice demonstrated |
| 2. MVP build | Weeks 3–8 | Full member UI, admin and exception handling, reconciliation, screening, terms, support, monitoring | Feature-complete on test networks |
| 3. Production readiness | Weeks 6–10 (overlaps) | Production vault deployed and handed over, security review of Helm's deployment, legal sign-off, operations rehearsal | Launch gate (section 14) passed |
| 4. Controlled launch | From about week 8–12 | Invitation-only cohort with exposure limits | Agreed checks pass, then expand |

**Assumptions behind these ranges:** a Cyclone team of about five engineers plus QA and a delivery lead; PillarsHub, Privy and Chatwoot access in week 1; Enzyme's test vault available in week 1; game API documentation available by week 2; vault strategy, MLA, ownership decisions and legal answers by around week 6. PillarsHub only launches clients Tuesday to Thursday, 9:00–16:00 US Mountain Time, which constrains the go-live date. Verified. No date in this table is a commitment.

**Indicative running costs** (USD per month unless stated; prices verified on 8 October 2026 where marked):

| Item | Cost | Status |
|---|---|---|
| Privy | Free up to 499 monthly active users; $299 up to 2,499; $499 up to 9,999. The free tier includes $1M of transaction volume per month. | Verified; overage and paid-tier volume limits TBD |
| Gas sponsorship | Network gas plus a Privy fee | TBD (usage-based) |
| Enzyme Onyx | Public page: $2,000 per month, or 20% of vault fees with a $6,000 annual minimum. Correspondence: $5,000 deployment plus 0.25% of AUM, or 20% revenue share. | Verified (public) vs correspondence; **reconfirm in the MLA** |
| PillarsHub | Not published | TBD |
| Chatwoot Cloud | $19 or $39 per agent (Startups, Business); $99 for Enterprise with audit logs and SSO | Verified |
| Sanctions address screening | Free Chainalysis sanctions API at pilot scale | Verified (discovery research) |
| KYC service, if counsel requires it | About $0.33–$1.85 per check at published prices | Verified (discovery research) |
| Security review of Helm's deployment | Quotation needed | TBD |

# Security and compliance summary

- **Custody.** Member wallets are self-custodial: only the Member signs. Neither Cyclone nor Privy can move Member funds. Verified (Privy). The vault is different: its Owner and Admins can set the share value and withdraw vault assets to the strategy wallet, and Enzyme can upgrade the contracts. Who holds those roles, under what controls, is the main custody question for Business and counsel.
- **Admission to the vault can be controlled on-chain.** Onyx lets only allowlisted wallet addresses deposit. Helm adds a Member's address only after its eligibility checks pass. Verified.
- **No provider in the stack supplies usable KYC or sanctions screening for this model.** Privy's KYC runs on Bridge, whose terms prohibit MLM. If counsel requires identity checks, a screening service is added at the Helm backend. This adds a service; it does not change the stack.
- **Minimum before real funds, whatever counsel concludes:** screening of every Member wallet, funding source and Redemption destination address against sanctions lists; country eligibility; Member terms, risk and fee disclosures and a privacy notice; a written procedure for flagged users and transactions.
- **Points and referrals.** Points have no cash value and are kept separate from money and Commissions. The referral model and any link between Points and deposits still need counsel's review; non-cash status alone is not an exemption.
- **Provider audits do not cover Helm's deployment.** Helm's vault configuration, keys, valuation process and integrations need their own security review before funds.

# Decisions needed at the meeting

| # | Decision | Recommended answer | Why it matters |
|---|---|---|---|
| D1 | Network and funding asset | Arbitrum One, native USDC; test on Ethereum Sepolia | Fixes wallet, vault and indexing work |
| D2 | Commissions in Phase 0 | Record the genealogy and vault events, but no Commission accrual or payout | Avoids an implied payout obligation; Phase 1 can backfill from Helm's records |
| D3 | Vault strategy, Manager and ownership | Business appoints the Manager; vault Owner is a multisig controlled by Business | Gates live funds |
| D4 | Redemption service level | Publish an operational target (for example, within 5 business days, subject to liquidity) | Members see stages, not a guarantee |
| D5 | Integrated top-up at launch | No; direct crypto funding | Removes a provider from the critical path |
| D6 | Identity checks | Counsel decides the tier; build the gates now; screen addresses from day one | Avoids rework if KYC is required |
| D7 | Points rules | No cash value, not transferable, not awarded for deposit amounts | Keeps Points separate from investment activity |
| D8 | Members without a valid Sponsor | Attach to a company root account, flagged for review | Keeps the genealogy complete |

