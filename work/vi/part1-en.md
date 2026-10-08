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

**Part II** (sections 9–16) is for the Tech teams. It refines the PRD and specifies the architecture, data flows, genealogy model, backlog, launch gate and responsibilities.

**The appendix** holds evidence links, assumptions, unresolved details and questions for providers.

Labels used throughout:

| Label | Meaning |
|---|---|
| **Verified** | Read in the provider's own documentation, API specification, contract source or pricing page on 8 October 2026 (links in Appendix A). |
| **Correspondence** | Stated in provider correspondence supplied by Business; not independently verified. |
| **Recommended** | Cyclone's proposed design or default. Not yet approved. |
| **TBD** | Assumption or open item. Needs a decision or provider confirmation. |

The stack is confirmed: **PillarsHub** (MLM core), **Privy** (login and wallets), **Enzyme Onyx** (vault infrastructure), **Chatwoot** (support), Cyclone's **Tap Prediction game and points**, and a custom **Helm Web App** with its backend. This document does not compare or reselect providers. Terrel's requirements (HELM Community Technology Requirements v0.2, 6 October 2026) are traced in section 9.

# Part I: Business and client {.unnumbered}

# Executive overview

**Goal of Phase 0:** capital is waiting to be deployed, so the MVP is cut to the fastest path that lets Business **onboard Members, let them join the vault (referred to by Business as "staking"), capture the genealogy correctly, and pay a simple referral Commission**. Everything else waits.

**The confirmed stack can deliver this.** Each capability is available from a confirmed provider or needs only configuration and a contained amount of Cyclone integration work. No evidenced blocker requires changing a provider. Terrel's requirements (v0.2, 6 October 2026) have been mapped to this scope in section 9.

**What Members will be able to do at launch:**

1. Join Helm through an invite link, or be imported from the alpha community, with their referral history kept.
2. Log in with email or social login and receive a Helm wallet automatically. Only the Member can move its funds.
3. Fund that wallet by sending USDC on one network from any exchange or wallet.
4. Read the vault terms, deposit into the approved vault, see their confirmed position, and request a Redemption.
5. See their direct team and referral link, and, as Builders, see Commissions as pending, held or paid.
6. Receive Commission payouts in USDC directly to their Helm wallet, in batches approved by Finance.
7. Play the existing Tap Prediction game and earn Points, which have no cash value.
8. Chat with support from inside the app; support sees who they are and their status, never their keys.

**Why this is the fastest credible path:**

- **Cyclone builds only the glue:** the member experience, one backend that connects the providers, a ledger of identities, referrals and events, the payout executor, and the reconciliation and admin views that make every money flow auditable.
- **Each provider does what it already does:** Privy runs login and wallets; PillarsHub stores the genealogy and calculates Commissions with its existing Unilevel plan; Onyx issues vault shares and runs deposit and redemption queues; Chatwoot handles conversations.
- **MLM screens are reused, not rebuilt.** Genealogy browsing, Sponsor and placement edits, plan configuration, bonus review, period close and bonus release are done in the PillarsHub Portal. Builders get the essentials in Helm plus an "Open full back office" link into PillarsHub's back office through single sign-on. Verified (SSO). Helm builds only what PillarsHub does not have.
- **Payouts reuse PillarsHub's batch mechanism.** PillarsHub sends approved payout batches to a merchant endpoint that Helm builds; Helm pays USDC from a Business-controlled multisig treasury and reports the result back. Verified. No payment provider is needed.
- **Direct crypto funding** keeps payment-provider onboarding off the critical path.

**What can start immediately (no provider or legal answer needed):** the Helm Web App shell, Privy login and wallets, the member, referral and event data model, the PillarsHub staging sync, alpha-import tooling (once sample data arrives), the payout executor on testnet, the Chatwoot widget, chain indexing, and the full deposit and redemption journey on Enzyme's Sepolia test network.

**What gates live funds and payouts** (none of these blocks the build):

1. **The vault strategy and its Manager.** Onyx is vault infrastructure, not a strategy. Someone must run the strategy, report the vault's value and return liquidity for Redemptions. Verified.
2. **Vault ownership and Enzyme's upgrade rights.** The vault Owner and Admins are fully trusted by the protocol, and Enzyme can upgrade vault contracts. The owning entity, a multisig and the upgrade terms in the licence agreement must be settled. Verified.
3. **Enzyme's licence agreement (MLA) and commercial terms.** Production use requires a commercial agreement. Verified.
4. **The Commission basis for the simple payout.** Which event pays (for example, a confirmed vault deposit, or vault fee revenue), the three level rates, period, hold and minimum must be approved by Owen, Finance and counsel. Terrel's requirements are explicit that "a raw deposit … must not silently replace approved eligible activity".
5. **Legal applicability review** of the operating entity, launch countries, KYC tier, vault terms and the referral payout model.
6. **Provider acceptance of the business model**, in writing, from Privy, Enzyme and PillarsHub.

**Earliest credible schedule (estimate, not a commitment):** an end-to-end test slice including a test payout about 3 weeks after kickoff; a controlled launch with deposits in about **8–12 weeks**, provided vault, licence, Commission-basis and legal answers arrive by around week 6. The first live payout follows the first approved period close and hold. Section 6 gives the assumptions, and section 6.1 sets out what is achievable within 30 days.

# Confirmed stack: what each system provides

```{.mermaid #fig-capabilities caption="Business capabilities, the platform that provides each, and what Cyclone builds."}
flowchart TB
  subgraph Member capabilities
    A[Join with referral] --- B[Wallet] --- C[Fund wallet] --- D[Vault deposit and redemption] --- E[Commission payout] --- F[Games, Points, support]
  end
  A --> PH[PillarsHub: genealogy]
  B --> PV[Privy: login and wallets]
  C --> CH[Blockchain: USDC transfer]
  D --> ON[Enzyme Onyx: vault shares and queues]
  E --> PC[PillarsHub calculates, Helm pays from treasury]
  F --> CW[Cyclone game; Chatwoot]
  PH & PV & CH & ON & PC & CW --> HB[Helm Web App and backend, built by Cyclone]
```

| Capability | Provided by | Cyclone builds | Status |
|---|---|---|---|
| Join and log in; one stable Helm identity | Privy (login, identity token) | Member record with Customer and Builder status, Privy mapping | Feasible |
| Wallet | Privy embedded wallet, owned by the Member; gas sponsored by Helm | Wallet screens; balance display | Feasible |
| Referral, genealogy and alpha import | PillarsHub (customer with enroller, Unilevel tree, full-tree export, dated placements) | Referral capture and validation, sync, alpha import and reconciliation | Feasible with configuration |
| Wallet funding | Blockchain (USDC transfer to the Member's address) | Address display, confirmation tracking, screening | Feasible |
| Vault deposit and redemption | Enzyme Onyx (allowlisted deposit queue, redemption queue, shares, public read API) | Terms screens, transaction flows, status tracking, allowlist updates | Feasible with configuration; **live use blocked** pending strategy, MLA and ownership |
| Simple Commission payout | PillarsHub (real-time calculation, bonus release, payout batches to a custom merchant) | Eligible-event posting, payout executor, treasury proposals, status callback, statements | Feasible with configuration and custom work; **blocked** pending approved Commission basis |
| Team view and Builder back office | PillarsHub back office (tree, reports, bonus detail) through SSO | Essentials in Helm (referral link, team counts, earnings summary, payouts) and the SSO hand-off | Feasible |
| MLM administration | PillarsHub Portal (genealogy, placements, plan, bonuses, period close, release) | Deep links by Member ID; change detection and reconciliation | Feasible |
| Games and Points | Cyclone Tap Prediction and points service | Account linking, verified events, Points display | **Feasible pending** game API documentation |
| Support | Chatwoot Cloud (web widget with identity validation) | Widget, identity signing, agent context view in Helm admin | Feasible |
| Operations | Provider dashboards (Onyx Admin App, PillarsHub Portal, Chatwoot) | Helm admin: exceptions, approvals, reconciliation, audit log | Feasible |

# The Member journey

```{.mermaid #fig-journey caption="Main Member journey. Wallet funding, vault deposit and Commission are separate events; Points are separate from money."}
flowchart LR
  I[Invite link] --> S[Sign up and log in] --> W[Wallet created] --> F[Fund wallet with USDC] --> T[Read vault terms] --> V[Deposit request] --> P[Position confirmed] --> C[Sponsor earns Commission] --> R[Payout to wallet]
```

1. **Invite and signup.** The Member opens a Sponsor's invite link and logs in with Privy. Helm records the Referral Request and confirms it once PillarsHub accepts it. Alpha-community Members are imported with their existing Sponsor.
2. **Wallet.** Privy creates an embedded wallet. Only the Member can sign with it; Helm and Privy cannot move its funds.
3. **Wallet funding.** Helm shows one supported network and asset (recommended: USDC on Arbitrum) and the Member's address. Funding moves money into the Member's own wallet; it is **not** an investment and creates no Commission.
4. **Vault deposit.** The Member reads the vault terms, fees and risks, then signs two transactions: permission for the vault to take the amount, and the deposit request. The request is pending until vault operations process it at the next valuation. Only then does the Member hold vault shares.
5. **Position.** Helm shows the confirmed share balance and its value as of the vault's last valuation, with the valuation date.
6. **Commission.** If the approved basis is met, PillarsHub calculates the Sponsor's Commission (up to three levels). Builders see it as pending, held and then payable.
7. **Payout.** After the period closes and the hold passes, Finance approves the batch. Helm pays USDC from the treasury to each Builder's Helm wallet; the Builder sees it as paid, with the transaction reference.
8. **Redemption and engagement.** Members can request a Redemption, processed when liquidity is available with each stage shown, and play Tap Prediction for Points.

# Phase 0 scope

| In scope (Pilot) | Deferred; stays disabled until approved |
|---|---|
| One network and one funding asset (recommended: USDC on Arbitrum One) | Integrated purchase or top-up (Paymenture or similar) |
| One approved Onyx vault, asynchronous deposits, queued Redemptions | Additional chains, assets or vaults; instant deposits |
| Privy embedded wallets with sponsored gas | Server wallets, automated strategies, policies |
| Referral capture, Customer and Builder status, full genealogy in PillarsHub, alpha import | Self-service or bulk placement moves; the governed placement window (GEN-04 to GEN-06) |
| **Simple Commission:** existing three-level Unilevel plan, one approved eligible event, USDC payout in Finance-approved batches | Ranks, qualification rules, matching or leadership bonuses, campaigns, contests |
| Referral link, team counts, earnings summary and payouts in Helm; full back office in PillarsHub via SSO | Custom Helm versions of PillarsHub screens; deep team analytics, leader contact tools, CRM |
| Existing Tap Prediction game and Points (no cash value) | Points redemption for value, new games, tokens |
| Chatwoot web chat with agent context; FAQ and runbooks | Telegram and WhatsApp support; AI agent |
| Sanctions screening of wallet addresses; country eligibility; Member terms | Full KYC unless counsel requires it (decision D6) |

# Feasibility summary

| Area | Verdict | Key evidence | What remains |
|---|---|---|---|
| Login and identity | **Feasible** | Privy issues verifiable identity tokens; one Privy user maps to one Helm member. Verified. | Confirm Privy accepts the business model. |
| Wallet | **Feasible** | User-owned embedded EVM wallet; Arbitrum supported; native gas sponsorship; key export. Verified. | Losing the only login method loses the wallet; offer a second login method. |
| Genealogy and alpha import | **Feasible with configuration** | Customer records take a Helm-defined ID, signup date and enroller at creation; the whole tree can be listed with an as-of date; placements are dated. No bulk import API. Verified. | Alpha records; auto-placement, depth limits and correction method in staging. |
| Commission calculation | **Feasible** | Payable depth is set in the plan; custom volume sources carry an external ID; calculation is real time. Verified. | Approved basis, rates, period and hold; plan configured by PillarsHub. |
| Commission payout | **Feasible with custom work** | PillarsHub sends release batches to a custom merchant endpoint authenticated by a callback token; the merchant reports "Success", "Failure" or "Pending" per payment; custom currency codes are allowed. Verified. | Helm builds the merchant endpoint and treasury executor; Finance approval flow. |
| Wallet funding | **Feasible** | Standard USDC transfer; Helm indexes the chain. | Choose network and asset. |
| Vault deposit and redemption | **Feasible with configuration; live use blocked** | Allowlisted deposit queue; Member must sign; admin executes after valuation; queued Redemptions; read-only API. Verified. | Strategy and Manager, MLA, ownership, upgrade terms, operating process. |
| Games and Points | **Feasible pending evidence** | No game documentation supplied. | API documentation, event verification and abuse controls. |
| Support | **Feasible** | Web widget with signed identity; Cloud plans from $19 per agent per month. Verified. | Agent context view; FAQ and runbooks (SUP-04 to SUP-06). |
| Compliance tooling | **Gap within the stack** | No confirmed provider offers usable KYC or screening for this model. | Counsel decision; add a screening service at the Helm backend if required. |

# MVP delivery plan

Delivery is organised so that engineering never waits for provider or legal answers. Those answers gate **live funds and payouts**, not the build.

| Stage | Duration (estimate) | Outcome | Gate to next stage |
|---|---|---|---|
| 0 – Access and decisions | Week 1 | Meeting decisions recorded; PillarsHub staging, Privy, Chatwoot, Onyx Sepolia vault, game docs and alpha sample data in hand | Access confirmed |
| 1 – Thin end-to-end slice | Weeks 1–3 | On test networks: invite → signup → wallet → referral accepted → funding → deposit → executed position → test Commission → test payout batch → Redemption | Slice demonstrated |
| 2 – MVP build | Weeks 3–8 | Member UI with team view and statements, admin approvals, alpha import rehearsal, reconciliation, screening, terms, support context, monitoring | Feature-complete on test networks |
| 3 – Production readiness | Weeks 6–10 (overlaps) | Production vault deployed and handed over; plan configured and proven with Finance examples; treasury multisig set up; security review; legal sign-off; alpha import and payout rehearsal | Launch gate (section 15) passed |
| 4 – Controlled launch | From about week 8–12 | Invitation-only cohort with exposure limits; first payout after first period close and hold | Agreed checks pass, then expand |

## 30-day plan

What can realistically be in place 30 days after kickoff, by how much depends on engineering alone and how much on decisions outside it. All items are estimates for a team of five to six engineers with provider access in week 1.

| Tier | What is live at day 30 | Depends on |
|---|---|---|
| **1. Certain** (engineering only) | Full journey on test networks: signup → wallet → referral → USDC funding → Vault Deposit → position → Commission calculation → **test payout batch from the treasury Safe** → Redemption. Alpha import tool run and reconciled on sample data. Admin roles, maker-checker, daily reconciliation, Chatwoot | Provider test access; alpha sample data |
| **2. Likely, if Business decides in week 1** | **Preregistration live with real users, no money yet:** signup, wallet, referral link, genealogy in PillarsHub production, alpha community imported with original Sponsors and dates, direct-team view, support. Matches Terrel's release sequence and ID-04: preregistered people keep attribution and cannot earn | Member terms and privacy notice; allowed countries; alpha records; PillarsHub production slot (Tuesday to Thursday) |
| **3. Possible around day 30–35, only if every external item lands on time** | **Capped real-funds pilot:** an invited cohort (for example alpha leaders) with per-Member and total limits deposits into the production vault | See the conditions below |
| **4. Not realistic within 30 days** | First real Commission payout; placement window, ranks and campaigns; full KYC if counsel requires it (adds about 1–2 weeks) | Payout needs an approved basis plus one period close and hold: about **day 45–60** with a weekly period and a short hold |

**Conditions for tier 3:**

| Condition | Needed by |
|---|---|
| Vault strategy and Manager appointed; Owner multisig set up | Week 1 |
| Enzyme MLA signed; production vault deployed and handed over | Signed in weeks 1–2; deployed by week 3 (Enzyme publishes no lead time) |
| Counsel confirms entity, launch countries, KYC tier and vault terms | Week 3 |
| Focused security review of vault configuration, keys and integration | Week 4 |
| Operations rehearsal with a small operator-funded amount | Week 4 |

**Week by week:**

| Week | Engineering | Business, Finance and counsel |
|---|---|---|
| 1 | Access, environments, Privy login and wallet, member and referral model, PillarsHub staging sync, Onyx Sepolia deposit | Decisions D1–D13; vault strategy and Manager; MLA; alpha records; Commission basis drafting; counsel engaged |
| 2 | Thin slice on test networks; alpha import dry run; event pipeline; payout endpoint and Safe proposals on testnet | Member and Builder terms; allowed countries; MLA signature |
| 3 | Builder essentials and PillarsHub SSO, admin approvals, screening, support context; preregistration release candidate | Counsel answers; production vault deployment; Commission basis approved |
| 4 | Preregistration go-live; alpha cutover; load and recovery checks; security review fixes; real-funds rehearsal | Security review; operations rehearsal; go/no-go for the capped pilot |

**Recommended day-30 milestone for the meeting:** *preregistration live, alpha community imported, genealogy locked, vault and payout proven on test networks.* Run the tier-3 conditions in parallel so real deposits open as soon as they clear, and approve the Commission basis early so the first payout is not delayed further.

## Assumptions and running costs

**Assumptions behind these ranges:** a Cyclone team of about five to six engineers plus QA and a delivery lead; provider access and alpha sample data in week 1; game API documentation by week 2; vault strategy, MLA, ownership, Commission basis and legal answers by around week 6. PillarsHub only launches clients Tuesday to Thursday, 9:00–16:00 US Mountain Time. Verified. No date in this table is a commitment.

**Indicative running costs** (USD per month unless stated; prices verified on 8 October 2026 where marked):

| Item | Cost | Status |
|---|---|---|
| Privy | Free up to 499 monthly active users; $299 up to 2,499; $499 up to 9,999. The free tier includes $1M of transaction volume per month. | Verified; overage and paid-tier volume limits TBD |
| Gas | Sponsored Member transactions plus treasury payout transactions | TBD (usage-based) |
| Enzyme Onyx | Public page: $2,000 per month, or 20% of vault fees with a $6,000 annual minimum. Correspondence: $5,000 deployment plus 0.25% of AUM, or 20% revenue share. | Verified (public) vs correspondence; **reconfirm in the MLA** |
| PillarsHub | Not published | TBD |
| Treasury multisig | Safe contracts (gas only) | Recommended |
| Chatwoot Cloud | $19 or $39 per agent (Startups, Business); $99 for Enterprise with audit logs and SSO | Verified |
| Sanctions address screening | Free Chainalysis sanctions API at pilot scale | Verified (discovery research) |
| KYC service, if counsel requires it | About $0.33–$1.85 per check at published prices | Verified (discovery research) |
| Security review of Helm's deployment | Quotation needed | TBD |

# Security and compliance summary

- **Custody.** Member wallets are self-custodial: only the Member signs. Neither Cyclone nor Privy can move Member funds. Verified (Privy). The vault is different: its Owner and Admins can set the share value and withdraw vault assets to the strategy wallet, and Enzyme can upgrade the contracts. Who holds those roles, under what controls, is the main custody question for Business and counsel.
- **Payout treasury.** Commissions are paid from a Business-owned multisig treasury. Helm's backend can only propose payout transactions; Finance signers approve them. Payouts go only to the Builder's own Helm wallet, so no one can redirect a payment by changing a destination (PAY-01).
- **Admission to the vault can be controlled on-chain.** Onyx lets only allowlisted wallet addresses deposit. Helm adds a Member's address only after its eligibility checks pass. Verified.
- **No provider in the stack supplies usable KYC or sanctions screening for this model.** Privy's KYC runs on Bridge, whose terms prohibit MLM. If counsel requires identity checks, a screening service is added at the Helm backend.
- **Minimum before real funds or payouts, whatever counsel concludes:** screening of every Member wallet, funding source and Redemption destination; country eligibility; Member and Builder terms, risk, fee and earnings disclosures, and a privacy notice; a written procedure for flagged users and transactions; payee status required for payouts (PAY-04).
- **Referral payouts on vault activity are the most sensitive legal point.** Paying Commissions on deposits ties rewards to new money coming in; counsel must approve the basis before the first payout. Points have no cash value and are kept separate from money and Commissions.
- **Provider audits do not cover Helm's deployment.** Helm's vault configuration, keys, valuation process, payout executor and integrations need their own security review before funds.

# Decisions needed at the meeting

| # | Decision | Recommended answer | Why it matters |
|---|---|---|---|
| D1 | Network and funding asset | Arbitrum One, native USDC; test on Ethereum Sepolia | Fixes wallet, vault, payout and indexing work |
| D2 | Commission basis for the simple payout | One approved eligible event (confirmed vault deposit or vault fee revenue), three Unilevel levels, period, hold and minimum approved by Owen, Finance and counsel; engineering builds the event pipe now | Payout cannot go live without it; the basis drives legal risk |
| D3 | Vault strategy, Manager and ownership | Business appoints the Manager; vault Owner is a multisig controlled by Business | Gates live funds |
| D4 | Redemption service level | Publish an operational target (for example, within 5 business days, subject to liquidity) | Members see stages, not a guarantee |
| D5 | Integrated top-up at launch | No; direct crypto funding | Removes a provider from the critical path |
| D6 | Identity checks | Counsel decides the tier; build the gates now; screen addresses from day one | Avoids rework if KYC is required |
| D7 | Points rules | No cash value, not transferable, not awarded for deposit amounts | Keeps Points separate from investment activity |
| D8 | Members without a valid Sponsor | Attach to a company root account, flagged for review | Keeps the genealogy complete |
| D9 | Alpha community import | Import before launch with original Sponsors and dates; reconcile counts and edges (GEN-03) | Existing capital and relationships arrive with history intact |
| D10 | Placement window promised in the field call | Not in the Pilot; publish the policy first, then enable the governed workflow (GEN-04 to GEN-06) | Avoids building moves before the rules exist |
| D11 | Payout treasury and approvers | Safe multisig owned by Business; Finance approves each batch; payouts only to the Builder's Helm wallet | Payout controls (PAY-01 to PAY-04) |
| D12 | PillarsHub status | Confirmed per Business; validate it with Terrel's proof scenarios T01–T06 in staging, not a new selection | Reconciles Terrel's "candidate" wording with the confirmed stack |
| D13 | MLM admin and Builder back office | Use the PillarsHub Portal and back office (SSO) instead of building them in Helm; Helm shows essentials only | Saves weeks of UI work; needs PillarsHub's Portal approvals and SSO token handling confirmed |

