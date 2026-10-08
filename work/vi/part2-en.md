# Part II: Technical implementation {.unnumbered}

# Refined high-level PRD

## Objectives

1. Onboard Members with one stable identity and a usable, self-custodial wallet.
2. Enable direct crypto Wallet Funding and participation in one approved vault, including a practical Redemption journey.
3. Reuse the existing Tap Prediction game and Points to drive engagement.
4. Capture the complete, portable genealogy from the first signup, so Phase 1 Commissions need no identity rebuild.

## Personas

- **Member:** joins through a referral, funds a wallet, deposits, plays, redeems, asks for support.
- **Operations administrator:** reviews referral and funding exceptions, maintains the vault allowlist, monitors queues and reconciliation, handles escalations. Uses Helm admin plus provider dashboards.
- **Vault operator** (Business-appointed): updates the vault valuation, executes deposit and redemption queues, manages liquidity. Uses the Onyx Admin App.
- **Support agent:** answers Members in Chatwoot; cannot move funds, change Sponsors or award Points.
- **Business reviewer:** reads funnel, participation, referral and engagement reports.

## Functional requirements and acceptance criteria

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-1 | Authenticate with Privy and resolve one Helm member | Repeat logins with any linked method resolve to the same Helm member ID; the backend verifies every Privy token; duplicate-person cases go to an admin queue |
| FR-2 | Create one embedded EVM wallet per Member | Wallet exists after first login; address is read from Privy server-side; the Member can sign a test transaction; recovery and export behaviour is explained in the app |
| FR-3 | Capture a Referral Request at signup | Invite code or link is captured before login and bound to the new member; self-referral is rejected; missing or invalid Sponsor follows rule D8 |
| FR-4 | Accept the Sponsor Edge in PillarsHub | Customer created with the Helm-defined ID and Sponsor; node read back with the expected upline; edge marked accepted only after read-back; retries never create duplicates |
| FR-5 | Show supported funding network and asset | Only one network and asset are offered; wrong-network warning is shown; funding moves through submitted → confirmed (N blocks) → credited; failed or unsupported transfers go to exceptions |
| FR-6 | Screen addresses | Member wallet on creation, each funding source and each Redemption destination are screened; a hit blocks the vault allowlisting or the action and opens a case |
| FR-7 | Gate vault access | Member must accept current vault terms (versioned) and pass eligibility checks; only then is the wallet added to the Onyx allowlist |
| FR-8 | Vault deposit | Member signs exact-amount approval and deposit request; Helm tracks approval → request → pending → executed or cancelled; position counts only after execution |
| FR-9 | Position display | Shares and value as of the vault's last valuation, with the valuation timestamp; matches chain state |
| FR-10 | Redemption | Member signs a redemption request; Helm shows pending, awaiting liquidity, executed, cancelled; asset arrives in the Member's wallet; position and business events adjust |
| FR-11 | Games and Points | Linked game account; verified events award Points once; rules and daily limits visible; Points shown separately from money |
| FR-12 | Support | Verified chat identity; agents see Helm member ID and non-sensitive status only; logout resets the chat |
| FR-13 | Admin and reconciliation | Daily reconciliation of genealogy, funding, vault positions and Points; mismatches appear in an exception queue with an audit trail |
| FR-14 | Reporting | Signups, funded Members, confirmed vault participation, referral completeness and engagement, with freshness shown and no double counting of funding and deposits |

**Three-level Commissions:** not required for launch unless Terrel's PRD says otherwise (decision D2). The genealogy is captured at full depth regardless.

## Operational requirements

- Every integration write is idempotent from Helm's side, retried with backoff and reconciled daily.
- No private key, seed phrase or privileged provider credential reaches the browser, logs or support payloads.
- Separate test and production environments for every provider, with separate credentials.
- Monitoring and alerts for: stale vault valuation, deposit or redemption requests pending beyond target, reconciliation breaks, sync failures, screening hits.

## Success metrics (targets TBD)

Time to first approved live deposit; signup completion; signup-to-funded and funded-to-deposited conversion; referral attribution completeness (target 100% of accepted signups); reconciliation exceptions per week; game participation and repeat engagement; support first-response and resolution time.

# Solution architecture

```{.mermaid #fig-architecture caption="Technical architecture and trust boundaries."}
flowchart TB
  subgraph Browser
    APP[Helm Web App + Privy SDK + Chatwoot widget]
  end
  subgraph Helm backend - Cyclone
    API[API and auth verification]
    DB[(Member DB, referral and event ledger)]
    INT[Integration workers: outbox, retries]
    IDX[Chain indexer]
    REC[Reconciliation and alerts]
    ADM[Admin console]
  end
  APP -->|Privy token| API
  APP -->|signs transactions| CHAIN[(Arbitrum: USDC, Onyx vault contracts)]
  API --> DB
  INT --> PH[PillarsHub API]
  INT --> GAME[Cyclone game and points API]
  INT --> SCR[Sanctions screening API]
  INT -->|allowlist update via list-owner key| CHAIN
  IDX --> CHAIN
  REC --> ONYXAPI[Onyx public read API]
  API --> PRIVY[Privy API]
  APP --> CW[Chatwoot Cloud]
```

## Components and why each is needed

| Component | Responsibility | Why custom |
|---|---|---|
| Helm Web App | Member and admin UI; Privy login; signing via the Member's embedded wallet; Chatwoot widget | One Member experience across providers |
| API and auth | Verifies Privy access tokens; resolves Helm member ID; serves the app | Providers cannot share one identity on their own |
| Member DB and ledger | Members, provider-ID mappings, wallets, Referral Requests, Sponsor Edges and corrections, business events, consent records, audit log | Single place to reconcile identities and money events |
| Integration workers | Outbox jobs to PillarsHub, game service, screening and allowlist; retries and dead letters | No provider offers idempotency keys across all calls |
| Chain indexer | Indexes USDC transfers to Member wallets and Onyx queue, shares and valuation events at confirmation depth | Privy production webhooks need Enterprise; Onyx has no webhooks. Verified |
| Reconciliation | Daily checks against chain, Onyx API, PillarsHub tree and Points | Provider data can drift; must be provable |
| Admin console | Exceptions, screening cases, allowlist status, Sponsor corrections with approval | Minimal; provider dashboards cover the rest |

## Data authority

| Object | Authoritative record | Helm keeps |
|---|---|---|
| Helm member identity and provider-ID mapping | Helm DB | Master |
| Login identity | Privy user (DID) | Mapping only |
| Wallet address | Privy (server-side read) and chain | Association with first-seen time |
| Accepted genealogy | **PillarsHub** tree (customer enroller plus node upline) | Pending requests, accepted-edge copy, audit log of corrections |
| Wallet funding | Blockchain | Indexed, confirmed events |
| Vault deposit requests, positions, Redemptions | Blockchain (Onyx contracts) | Indexed events; Onyx API as cross-check |
| Vault valuation | Onyx valuation contract (set by vault operator) | Displayed with timestamp |
| Points balance | Cyclone points service | Display copy |
| Conversations | Chatwoot | Link to member ID |
| Terms acceptance, screening results, eligibility | Helm DB | Master |

## Credentials, signing and custody boundaries

| Actor | Can sign or act | Cannot | Notes |
|---|---|---|---|
| Member | Wallet transfers, vault approval, deposit and redemption requests, cancellations | Admin actions | Privy embedded wallet; Onyx requires the Member's own address to sign its requests. Verified |
| Helm backend | PillarsHub writes (customers, nodes, sources) with a limited token; game API; screening API; vault allowlist updates through a list-owner key | Move Member funds; vault admin actions | List-owner key held in a key management service; owns only the allowlist contract (to confirm with Enzyme) |
| Vault Owner (Business) | Add and remove Admins; any admin action | — | Recommended: Safe multisig with Business signers |
| Vault Admin / operator (Business) | Update valuation; execute queues; move assets to the strategy wallet; set fees | — | Fully trusted by the protocol. Verified |
| Strategy Manager (Business-appointed) | Runs the strategy outside Onyx; returns liquidity | — | Custody of the strategy wallet sits outside Onyx. Verified |
| Enzyme | Deploys; upgrades contracts (global owner) | — | Upgrade governance must be in the MLA. Verified |
| Privy | Runs the signing enclave | Sign for the Member | Privy "is never an authorized signer". Verified |
| Support agent | Reply in Chatwoot; read-only member status | Funds, Sponsors, Points | Enforced in Helm admin |

PillarsHub tokens are environment-bound and do not expire; they can be made read-only. Recommended: a read-only token for reconciliation and a separate write token, with destructive areas denied if PillarsHub allows it (TBD). Payout, period and bonus-release endpoints must never be called by Helm in Phase 0.

# End-to-end data flows

Every flow distinguishes **submitted** (Helm has a request or transaction hash), **confirmed** (provider acknowledged or block confirmations reached) and **synchronised** (Helm's copy matches the authority after reconciliation). Webhooks are treated as hints; polling and indexing are authoritative.

```{.mermaid #fig-flow-signup caption="Invite, signup, wallet and accepted genealogy."}
sequenceDiagram
  participant M as Member app
  participant P as Privy
  participant H as Helm backend
  participant X as PillarsHub
  M->>M: store invite code
  M->>P: log in
  P-->>M: access token, embedded wallet
  M->>H: register(token, invite code)
  H->>P: verify token, read wallet address
  H->>H: create member, Referral Request (pending), screen address
  H->>X: find customer by Helm ID
  H->>X: create customer (id, externalIds, enrollerId)
  H->>X: read node and upline
  H->>H: Sponsor Edge accepted
  H-->>M: referral confirmed
```

```{.mermaid #fig-flow-funding caption="Direct wallet funding."}
sequenceDiagram
  participant E as Exchange or wallet
  participant C as Arbitrum
  participant I as Helm indexer
  participant H as Helm backend
  participant M as Member app
  E->>C: USDC transfer to Member address
  I->>C: Transfer event seen (submitted)
  I->>I: wait N confirmations
  I->>H: funding confirmed (chain, tx, log index)
  H->>H: screen source address, record event
  H-->>M: balance updated
```

```{.mermaid #fig-flow-deposit caption="Vault deposit, execution and position."}
sequenceDiagram
  participant M as Member app
  participant H as Helm backend
  participant C as Onyx contracts
  participant O as Vault operator
  M->>H: accept vault terms (version)
  H->>C: add wallet to allowlist
  M->>C: approve exact amount
  M->>C: requestDeposit
  C-->>H: DepositRequest(requestId) via indexer
  O->>C: update valuation, execute deposit requests
  C-->>H: DepositRequestExecuted(requestId, shares)
  H->>H: position confirmed, business event recorded
  H-->>M: position and valuation date shown
```

```{.mermaid #fig-flow-game caption="Game activity to Points."}
sequenceDiagram
  participant M as Member app
  participant G as Game and points service
  participant H as Helm backend
  M->>G: play (linked Helm member)
  G->>G: validate result, apply limits
  G->>H: signed event (event id, member, Points)
  H->>H: verify signature, dedupe on event id
  H-->>M: Points balance (from service)
```

```{.mermaid #fig-flow-redemption caption="Redemption request to settlement."}
sequenceDiagram
  participant M as Member app
  participant H as Helm backend
  participant C as Onyx contracts
  participant O as Vault operator
  M->>H: screen destination (own wallet)
  M->>C: requestRedeem(shares)
  C-->>H: RedeemRequest(requestId) via indexer
  O->>C: update valuation, ensure liquidity
  O->>C: execute redeem requests
  C-->>H: RedeemRequestExecuted(requestId, assets)
  H->>H: position reduced, business event recorded
  H-->>M: USDC in wallet, stages complete
```

```{.mermaid #fig-flow-support caption="Support and admin exception resolution."}
sequenceDiagram
  participant M as Member app
  participant H as Helm backend
  participant W as Chatwoot
  participant A as Agent
  participant D as Helm admin
  M->>H: request chat identity
  H-->>M: member ID + identity hash
  M->>W: open verified conversation
  W->>A: conversation with member ID
  A->>D: look up status (read-only)
  D->>D: ops resolves exception with approval and audit
  A->>W: reply to Member
```

## Flow matrix

| Flow | Origin → destination | Minimum data | Authoritative record | Deduplication key | Failure and retry | User sees |
|---|---|---|---|---|---|---|
| Signup and referral | App → Helm → PillarsHub | Privy DID, wallet address, invite code, Sponsor member ID | PillarsHub tree (accepted edge) | Helm member ID (PillarsHub customer ID) | Look up before create; backoff; dead letter to ops; nightly tree reconciliation | "Referral pending" then "confirmed" |
| Wallet funding | Exchange → chain → Helm indexer | Chain, tx hash, log index, amount, from, to | Chain | (chain, tx hash, log index) | Re-index from last safe block; reorg handling by confirmation depth | Pending → confirmed balance |
| Vault deposit | App → Onyx contracts; indexer → Helm | Request ID, amount, wallet, terms version | Chain (queue and shares) | (chain, queue address, request ID) | Reverted transactions shown with reason; stale pending alert; Onyx API cross-check | Approval → requested → processing → position |
| Eligible MLM volume (Phase 1 or if approved) | Helm → PillarsHub sources | Member node, executed amount, date | Helm business event; PillarsHub source | Source externalId = chain:tx:log | Look up by externalId on conflict or timeout | Not shown in Phase 0 |
| Game to Points | Game service → Helm | Event ID, member ID, Points, rule ID | Points service | Event ID | Signed events; replay protection; daily limits | Points balance and history |
| Redemption | App → Onyx; indexer → Helm | Request ID, shares, destination | Chain | (chain, queue address, request ID) | Awaiting-liquidity alert; cancellation after minimum duration | Requested → awaiting liquidity → paid |
| Support | App → Chatwoot; agent → Helm admin | Member ID, identity hash, non-sensitive status | Chatwoot (conversation); Helm (actions) | Conversation ID | Widget reset on logout; signed Chatwoot webhooks logged | Chat thread |

**Unavailable providers:** if PillarsHub is down, signups proceed with the referral pending and sync later. If the indexer lags, balances show "updating". If Onyx's API is unavailable, Helm relies on chain reads. If the game service is down, play is disabled and no Points are lost.

# Genealogy and Phase 1 readiness

## Minimum data model

| Table | Key fields | Purpose |
|---|---|---|
| member | helm_member_id, status, created_at, country attestation | Stable identity |
| provider_identity | helm_member_id, provider (privy, pillarshub, chatwoot, game), external_id, linked_at | Explicit mappings |
| wallet | helm_member_id, chain_id, address, source (embedded), first_seen_at, screening_status, allowlist_status | One vault wallet per Member |
| referral_request | id, helm_member_id, sponsor_member_id, invite_code, channel, captured_at, status, rejection_reason | Pending and rejected referrals |
| sponsor_edge | id, member_id, sponsor_member_id, effective_at, accepted_at, provenance (signup, import, correction), pillarshub_sync_status, superseded_by | Full graph at every depth |
| edge_correction | id, edge_id, old_sponsor, new_sponsor, reason, requested_by, approved_by, approved_at | Audited changes |
| business_event | id, type (funding, deposit_executed, redemption_executed, points_awarded), member_id, amount, asset, chain reference, occurred_at, idempotency_key | Phase 1 volume backfill and reporting |
| integration_outbox | id, target, payload hash, attempts, status, last_error | Reliable sync |

Only data with an identified purpose is collected. No Sponsor or member data is written on-chain.

## Rules

- **Self-referral:** rejected at capture (same member, same wallet, same verified email or phone).
- **Invalid or missing Sponsor:** attach to the company root account with provenance "no sponsor" and flag for review (decision D8).
- **Cycles:** impossible for new Members; checked on every correction and import.
- **Sponsor changes:** never self-service. Admin-only, with reason, second approval and audit entry, then a PillarsHub node update and read-back. Recommended: disable customer movements in the PillarsHub tree configuration so the two systems cannot drift.
- **Account merges:** admin process; keep the earliest accepted edge; re-point child edges with audit entries; retire the duplicate identity.
- **Existing-user import** (only if FirstAlphaWave or TaQUANT members must move): import Sponsors before children, with original signup dates and provenance "import"; there is no bulk API, so import record by record. Verified.

## Proving correctness

- **Full export:** page through every node of the tree with an as-of date, not the downline endpoint, which is capped at 10 levels. Verified.
- **Nightly reconciliation:** compare Helm's accepted edges with PillarsHub nodes (count, edge-by-edge upline match, checksum). Any mismatch is an exception.
- **Staging test before launch:** a synthetic tree at least 15 levels deep and wide enough to page, created, exported and compared.
- **Phase 1 snapshots:** PillarsHub accepts an as-of date and keeps dated placements, and Helm keeps effective timestamps, so historical genealogy can be reconstructed. No separate snapshot store is needed in Phase 0.

## Volume in Phase 0

PillarsHub calculates Commissions in real time from posted volume. Verified. Posting vault deposits into a commissionable volume type would show pending Commissions to Members. **Recommended:** record executed deposits and Redemptions as business events in Helm only; in Phase 1, backfill PillarsHub with the original dates once the plan is approved. Whether PillarsHub accepts backdated volume for closed periods is to be confirmed in staging.

# Backlog, dependencies and schedule

## Prioritised backlog

| Priority | Work items | Depends on |
|---|---|---|
| **Start immediately** | App shell and design system; Privy login and embedded wallet; member DB and ledger; referral capture and validation; PillarsHub staging sync with read-back; chain indexer (Sepolia); Onyx SDK deposit and redemption on Sepolia; Chatwoot widget with identity validation; admin skeleton; screening hook with free sanctions API; CI, environments, secrets | Provider test access |
| **Thin slice (weeks 1–3)** | End-to-end demo on test networks, including one game-to-Points flow | Game API docs |
| **Before live funds** | Vault terms and disclosures with versioned acceptance; allowlist automation; reconciliation jobs and alerts; exception queues; redemption stages and target; country eligibility; Member terms and privacy notice; production environments; security review fixes; operations runbook and rehearsal | Strategy, MLA, ownership, legal answers |
| **Deferrable** | Integrated top-up; additional chains and assets; Commission accrual and payouts; Telegram and WhatsApp; Chatwoot audit logs and SSO; commercial transaction monitoring; native mobile | Business demand |

## Critical path

1. Meeting decisions D1–D8.
2. **Vault readiness:** strategy and Manager → vault configuration (asset, async queue, external allowlist, non-transferable shares, fees) → MLA signature → production deployment → ownership handover to the Business multisig.
3. **Legal answers:** entity, launch countries, KYC tier, vault terms.
4. **Security review** of Helm's integration and vault configuration.
5. **Operations rehearsal:** valuation, queue execution and Redemption liquidity on a small amount.
6. PillarsHub production launch slot (Tuesday to Thursday).

Engineering work runs in parallel with items 2–3; the launch date is set by whichever of them finishes last.

# Launch and operational readiness

## Gate for accepting real funds

All must be true; none is waived to meet a date.

1. Vault strategy, Manager, fees and Member terms approved by Business and counsel.
2. MLA signed; deployed version and audit coverage confirmed by Enzyme; upgrade governance documented.
3. Vault Owner multisig in place; Admin and list-owner keys in managed custody; no Owner or Admin key in Helm's backend.
4. Deposits and Redemptions proven on production with a small operator-funded amount.
5. Daily reconciliation passing; monitoring and alerts live; incident contacts at each provider.
6. Screening and eligibility live for the counsel-approved tier.
7. Security review completed and high-severity findings fixed.
8. Written provider acceptance of the business model (Privy, Enzyme, PillarsHub).
9. Support runbook and escalation procedure, including handling of flagged users.

## Security boundaries

- **Audit coverage.** ChainSecurity audited the Onyx core (December 2025), the cross-chain wallet (May 2026) and the Chainlink compliance integration (July 2026). One deployment helper added after the last audit appears in no audit scope found. Verified. Enzyme must confirm which components Helm's vault uses and that they are covered.
- **Upgrade risk.** Enzyme's global owner can upgrade all vault contracts; the audit describes this role as able to "fully drain the system", and no timelock was found. Verified. The MLA must cover notice and governance.
- **Gas sponsorship.** Privy's native sponsorship upgrades Member wallets with EIP-7702; the delegation contract is part of the security review. Verified.
- **Unsigned PillarsHub webhooks.** Treat them as hints and re-fetch through the API. Verified.
- **Test and production separation** for every provider, with separate credentials and no production keys on developer machines.

## Compliance responsibility matrix

Accountable functions are proposals; named owners are TBD.

| Control | Applicability question | Accountable (proposed) | Cyclone work | Provider capability relied on | Launch impact |
|---|---|---|---|---|---|
| Entity and custody classification | Does any entity have "control" of Member assets (vault roles, allowlist key)? | Business + counsel | Document signing authority and key flows | Privy self-custody (verified); Onyx roles (verified) | **Blocker** |
| Launch countries and geographic restriction | Which countries are allowed? | Business + counsel | Country attestation, IP checks, block list | None native | **Blocker** |
| Vault product characterisation | Is the vault offering a regulated product in launch countries? | Business + counsel | Terms, fee and risk screens with acceptance record | Onyx strategy and fees (TBD) | **Blocker** |
| KYC tier | Is any no-KYC tier allowed; at what thresholds? | Business compliance + counsel | Tier fields and gates now; vendor integration if required | None native (Privy KYC via Bridge unavailable) | Before funds |
| Sanctions: addresses | Which lists and when? | Business compliance | Screen wallet, funding source, Redemption destination | Chainalysis free API (verified, discovery) | Before funds |
| Sanctions: persons | Is name screening required? | Business compliance + counsel | Hook into identity tier | Vendor TBD | Before funds if required |
| Vault admission | Only eligible Members may deposit | Business + Enzyme | Allowlist automation after checks | Onyx deposit allowlist (verified) | Before funds |
| AML monitoring and escalation | What monitoring and reporting duties apply? | Business (compliance officer) | Thresholds, exception queue, case log | None native | Before funds (manual minimum) |
| Flagged users and transactions | What may Helm lawfully refuse or hold? | Counsel + Business | Restricted states in Helm; no assumed freezing power | Onyx admin discretion and policies (verified) | Before funds |
| Terms, privacy, consent, retention | Which notices and data-sharing consents? | Business (legal) | Versioned consent; data map per provider | Chatwoot Cloud hosted in the US (verified) | Before funds |
| Referral model and Points | Are referral rewards and Points disclosed and lawful? | Business + counsel | Rules pages; no earnings claims; Points separate from money | PillarsHub, game service | Before funds (disclosures) |
| Provider acceptance | Do providers accept the model on full disclosure? | Business | Avoid Stripe and Bridge features in Privy | Written confirmations | Before funds |

# Implementation decisions and feasibility gaps

| Decision | Recommended answer | Evidence | Unresolved dependency | Responsible function (proposed) | Launch impact |
|---|---|---|---|---|---|
| Network and asset | Arbitrum One, native USDC; Sepolia for tests | Onyx and Privy support Arbitrum; Onyx test deployment is on Sepolia (verified) | Enzyme confirms production chain and asset | Business + Tech | High |
| Wallet model | User-owned Privy embedded wallet, no app signer, sponsored gas, export enabled | Privy docs (verified) | Privy accepts the business model; volume limit above $1M per month | Tech | Medium |
| Vault configuration | Async deposit queue; external allowlist owned by a dedicated list-owner key; non-transferable shares; one asset | Onyx contracts and docs (verified) | Enzyme confirms external list ownership at deployment | Business + Enzyme | High |
| Vault roles | Business Safe multisig as Owner; separate Admin wallet; limited admin for valuation updates | Onyx roles (verified) | Business signers; Manager appointment | Business | **Blocker** |
| Redemption target | Publish an operational target; show stages | No protocol SLA (verified) | Liquidity policy from Manager | Business | High |
| Genealogy authority | PillarsHub, with Helm pending requests and reconciled copy | Customer and tree APIs (verified) | Auto-placement and correction method in staging | Tech + PillarsHub | Medium |
| Phase 0 Commissions | None accrued or paid; events kept in Helm for backfill | Real-time calculation and separate payout step (verified) | Terrel's PRD; Business confirmation | Business | Medium |
| Funding path | Direct crypto; no top-up provider | Paymenture publishes no assets, countries or fees and bars "pyramid schemes" (verified) | Business requirement | Business | Low |
| Points | No cash value; not linked to deposit amounts | No game docs supplied | Game API documentation; counsel review | Business + Cyclone | Medium |
| Identity checks | Gates built now; tier set by counsel; address screening from day one | No KYC in stack (verified) | Counsel decision | Business + counsel | High |

**What would change these defaults:** a requirement for integrated top-up at launch adds a payment provider to the critical path; a requirement to pay three-level Commissions at launch adds money-out integration and payout controls; counsel requiring full KYC adds an identity vendor and a gate before vault access.

# Appendix A: Evidence {.unnumbered}

All links were read on 8 October 2026.

**PillarsHub:** [API authentication](https://pillars-hub.readme.io/reference/authenticating) · [Access tokens](https://pillars-hub.readme.io/reference/access-control-tokens) · [Swagger UI](https://api.pillarshub.com/swagger/index.html) · [Customer API spec](https://api.pillarshub.com/swagger/CustomerV1/swagger.json) · [Commission API spec](https://api.pillarshub.com/swagger/CommissionV1/swagger.json) · [Webhooks](https://pillars-hub.readme.io/reference/getting-started-webhooks) · [Webhook topics](https://pillars-hub.readme.io/reference/topics) · [Invoice dates and real-time commissions](https://pillars-hub.readme.io/docs/invoice-dates-are-used-to-calculate-commissions) · [Launch timing protocol](https://pillars-hub.readme.io/docs/pillars-launch-timing-protocol) · [Money-out integrations](https://pillars-hub.readme.io/docs/money-out-merchant-integration-guide) · [Terms](https://www.pillarshub.com/terms)

**Privy:** [Pricing](https://www.privy.io/pricing) · [Security FAQ](https://docs.privy.io/security/security-faqs) · [Supporting users](https://docs.privy.io/user-management/users/managing-users/supporting-your-users) · [Webhooks](https://docs.privy.io/api-reference/webhooks/overview) · [React quickstart](https://docs.privy.io/basics/react/quickstart) · [Acceptable use policy](https://www.privy.io/acceptable-use-policy)

**Enzyme Onyx:** [Product and pricing](https://enzyme.finance/products/onyx) · [Architecture](https://docs.enzyme.finance/onyx-user-documentation/getting-started/quickstart/architecture) · [Deposit control and allowlists](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/control) · [Redemptions](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/redemptions) · [User roles](https://docs.enzyme.finance/onyx-protocol/user-roles) · [Deployments and upgrades](https://docs.enzyme.finance/onyx-protocol/architecture/deployments-and-upgrades) · [Risks and limitations](https://docs.enzyme.finance/onyx-protocol/security/risks-and-limitations) · [SDK](https://docs.enzyme.finance/onyx-sdk) · [Public API](https://api.onyx.enzyme.finance/reference) · [Contracts](https://github.com/enzymefinance/protocol-onyx) · [Audits](https://github.com/enzymefinance/protocol-onyx/tree/main/audits)

**Chatwoot:** [Developer docs](https://developers.chatwoot.com/introduction) · [Pricing](https://www.chatwoot.com/pricing)

**Funding and compliance:** [Paymenture](https://paymenture.com/) · [Bridge developer agreement](https://www.bridge.xyz/legal/developer-agreement) · [Chainalysis sanctions oracle](https://go.chainalysis.com/chainalysis-oracle-docs.html) · [FATF 2021 guidance](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html)

Detailed notes with every source and quotation are in `work/notes/01-pillarshub.md`, `02-enzyme-onyx.md`, `03-privy.md` and `04-chatwoot-funding-compliance.md`.

# Appendix B: Assumptions and gaps {.unnumbered}

- **Terrel's PRD was not supplied.** Not validated against it: Commission rules and depth, rank definitions, required back-office features, any requirement for Members to see PillarsHub's back office, any existing-member migration.
- **Game and Points:** no API documentation was supplied. Needed: account linking method, event schema and signing, duplicate and replay protection, abuse controls, Points rules engine, whether Points can be redeemed for anything.
- **Not verified with providers:** PillarsHub auto-placement, depth limits, sponsor correction method, token permission granularity, rate limits, 409 semantics, pricing and security certifications; Privy paid-tier volume limits and business-model acceptance; Enzyme lead times, deployed version, external allowlist ownership, commercial terms; Chatwoot webhook retry behaviour.
- **Pricing:** Enzyme's public price differs from the correspondence; PillarsHub pricing is not public.
- **Team capacity, budget and launch cohort** were not supplied; schedule ranges assume about five engineers.

# Appendix C: Questions for providers {.unnumbered}

**PillarsHub**

1. Does creating a customer with an enroller place the node in the Unilevel tree automatically, with the upline equal to the enroller?
2. Is genealogy depth unlimited? Does listing tree nodes without node IDs return every node, and what is the page-size maximum?
3. What is the supported, audited way to correct a Sponsor? Can customer movements be disabled?
4. What does a 409 on posting a source mean? Is externalId unique per environment? Are duplicate customer IDs rejected?
5. Can a source group exist that no bonus uses? Is backdated volume accepted for closed periods?
6. Can access tokens be limited by area and deny deletes? What are the rate limits?
7. Can webhooks be signed? Is there a placement or source topic?
8. Please confirm in writing that API-based reconciliation of genealogy is permitted under the Terms, and explain the GLBA disclaimer in this context.
9. Security documentation, data residency, pricing and launch-slot booking.

**Privy**

1. Do you accept this business model on full disclosure, and do embedded wallets, gas sponsorship and token verification require any Stripe or Bridge account?
2. How is the $1M monthly transaction volume measured, and what applies above it on paid plans?
3. Can production webhooks or an SLA be added without Enterprise?
4. Security review material for the EIP-7702 delegation used by gas sponsorship.

**Enzyme**

1. Upgrade governance: who controls upgrades, with what notice, and can Helm's vault opt out?
2. Deployed version and addresses; audit coverage of every component Helm uses, including the deployment helper.
3. Confirm Sepolia for the test vault, Admin App access there, and API indexing of Sepolia.
4. Production chain and recommended deposit asset for Arbitrum.
5. Can an external allowlist owned by a Helm list-owner key be attached at deployment? Indexer delay?
6. Configure shares as non-transferable.
7. Redemption: notice-period or gate modules; recommended cadence; handling a batch that reverts on one request.
8. Valuation automation: lead time, cost, data-provider subscriptions.
9. Commercial terms (deployment fee, AUM option vs public plan, $6,000 minimum), MLA draft, onboarding form, lead times.
10. Can Enzyme's default investor interface be disabled so Members use only Helm?

**Chatwoot**

1. Webhook retry and failure behaviour.
2. Data residency options for Cloud; audit logs below Enterprise.

**Cyclone game team**

1. API documentation, event signing, replay protection, abuse controls and Points rules engine.
