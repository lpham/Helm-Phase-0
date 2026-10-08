# Part II: Technical implementation {.unnumbered}

# Traceability to Terrel's requirements

Terrel's *HELM Community Technology Requirements v0.2* (6 October 2026) defines "Must" as required **before the named capability is enabled**, and states that a deferred capability stays disabled. That lets Phase 0 enable a small set of capabilities fully, rather than all capabilities partly. The table maps each requirement group to the Phase 0 Pilot.

| Group | Requirement IDs | Phase 0 Pilot treatment | Where in this document |
|---|---|---|---|
| Identity and member records | ID-01 to ID-04 | **In scope.** Stable person ID; Customer and Builder status; prospect, preregistered, verified and enrolled states; country eligibility and agreement versions | FR-1, FR-15; section 13 |
| Corporate administration | ADM-01 to ADM-03 | **In scope.** Separate view, configure, correct, approve and release roles; maker-checker on Sponsor corrections, holds and payout releases; test environments | FR-13, FR-19; section 11.3 |
| Lifecycle actions | ADM-04 | Merges and recovery in scope as admin processes; suspension, termination and re-entry **disabled** until enabled | Section 13.2 |
| Sponsor and genealogy | GEN-01 to GEN-03 | **In scope.** Referrer, sponsor (enroller) and placement recorded separately with effective dates; loop and duplicate checks; **alpha import with reconciliation** | FR-3, FR-4, FR-20; section 13 |
| Placement window | GEN-04 to GEN-06 | **Disabled** until the placement policy is approved (decision D10); the data model already preserves original referral and history | Section 13.2 |
| Compensation | COMP-01 to COMP-04 | **In scope, simple plan only.** One approved eligible event, versioned three-level Unilevel, replay-safe events, calculated, pending, held, payable and paid states, reconciliation to batches | FR-17, FR-18; sections 12, 13.4 |
| Qualification and rank | QUAL-01 to QUAL-03 | **Disabled.** No ranks in the simple plan; QUAL-03 applies only when rank progress is promised | Scope table |
| Earnings audit | AUD-01 to AUD-03 | **In scope.** Explain each earning from source event to payout; preserve corrections; period statements separating vault performance from referral earnings | FR-18, FR-19 |
| Rewards | REW-01 to REW-03 | Points only; no redemption, promotional credit or cash conversion | FR-11; decision D7 |
| Builder back office | BO-01, BO-02, BO-04 | **In scope.** Referral link, permitted team data, earnings states, statements, dispute request; mobile web and release language | FR-16, FR-19 |
| Team visibility | TEAM-01, TEAM-02 | **In scope, minimum.** Direct team and counts; no access to another branch or anyone's balances, trades or support cases | FR-16 |
| Team tools | TEAM-03 to TEAM-05 | Basic welcome step only (TEAM-05 Pilot); search, contact and automation deferred | Scope table |
| Campaigns | CAMP-01 | **In scope.** Referral link attribution, precedence and invalid referrals; CAMP-02 to CAMP-04 disabled | FR-3 |
| Business intelligence | BI-01, BI-02 | **In scope.** Separate definitions for customers, Builders, deposits, Commissions, liabilities and payouts; reconciliation to sources | FR-14 |
| Payouts | PAY-01 to PAY-04 | **In scope.** Payout instructions from approved payable amounts; restricted destinations; tracked states; reconciliation; payee status | FR-18; sections 12, 15 |
| APIs and events | API-01 to API-03 | **In scope.** Sandbox, stable event IDs, replay and backfill, polling where webhooks are unsafe; **export rights in contract** | Sections 11, 12; launch gate |
| Support | SUP-01 to SUP-07 | **In scope (Pilot).** Agent context view, case links to person and event IDs, agent limits, FAQs and runbooks, metrics | FR-12 |
| Compliance records | REC-01, REC-02 | **In scope.** Versioned agreements, consent and disclosures; country and product restrictions with rule version | FR-15; section 15.3 |
| Operations | OPS-01 to OPS-04 | **In scope.** Load envelope, recovery targets, incident response, per-capability gates | Section 15 |
| Implementation | IMP-01 to IMP-04 | **In scope.** Plan with owners, migration rehearsal, release acceptance, handover | Sections 14, 15 |

**Where this document differs from Terrel's draft:**

- **Provider status.** Terrel's draft lists Pillars and Infinite MLM Software as candidates, with neither selected. Business has since confirmed PillarsHub. This document treats PillarsHub as confirmed and proposes running Terrel's proof scenarios as **validation** of the configuration (decision D12), not as a new selection.
- **Proof scenarios for the Pilot.** T01 (alpha migration), T02 (plan normal and boundary cases), T03 (duplicate and replayed events), T05 (reversal before and after payout), T06 (payout timeout and retry), T07 (leader access limits) and T11 (Customer, Builder and dual role) gate the Pilot. T04, T09, T12 and T13 gate the capabilities they relate to when those are enabled. T10 and T14 gate production handover.
- **Still missing from Terrel's "Waiting for" list:** the compensation specification with worked examples, alpha enrollment and genealogy records, and a one-page release scope (audience, countries, languages, activities).

# Refined high-level PRD

## Objectives

1. Onboard Members, including the alpha community, with one stable identity and a usable, self-custodial wallet.
2. Let Members fund their wallet with crypto and join the approved vault, with a practical Redemption journey.
3. Capture the complete genealogy, with referrer, sponsor and placement kept separately, from the first signup.
4. Pay a simple three-level Commission on one approved eligible event, in Finance-approved USDC batches.
5. Reuse the existing Tap Prediction game and Points to drive engagement.

## Personas

- **Member (Customer):** joins through a referral, funds a wallet, deposits, plays, redeems, asks for support.
- **Builder:** a Member enrolled to refer others; sees the referral link, direct team and Commission states; receives payouts. Not every Member is a Builder (ID-01).
- **Operations administrator:** reviews referral, import and funding exceptions, maintains the vault allowlist, monitors queues and reconciliation, handles escalations.
- **Finance approver:** reviews and approves payout batches and holds; signs treasury transactions.
- **Vault operator** (Business-appointed): updates the vault valuation, executes deposit and redemption queues, manages liquidity. Uses the Onyx Admin App.
- **Support agent:** answers Members in Chatwoot with read-only context; cannot move funds, change Sponsors, release payouts or award Points.
- **Business reviewer:** reads funnel, participation, referral, Commission and engagement reports.

## Functional requirements and acceptance criteria

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-1 | Authenticate with Privy and resolve one Helm member | Repeat logins with any linked method resolve to the same Helm member ID; the backend verifies every Privy token; duplicate-person cases go to an admin queue (ID-02) |
| FR-2 | Create one embedded EVM wallet per Member | Wallet exists after first login; address is read from Privy server-side; the Member can sign a test transaction; recovery and export behaviour is explained in the app |
| FR-3 | Capture a Referral Request at signup | Invite link captured before login and bound to the new member; attribution precedence and window applied (CAMP-01); self-referral rejected; missing or invalid Sponsor follows rule D8 |
| FR-4 | Accept the Sponsor Edge in PillarsHub | Customer created with the Helm-defined ID, signup date and enroller; node read back with the expected upline; edge marked accepted only after read-back; retries never create duplicates; original referrer kept in Helm (GEN-01) |
| FR-5 | Show supported funding network and asset | Only one network and asset are offered; wrong-network warning is shown; funding moves through submitted → confirmed (N blocks) → credited; failed or unsupported transfers go to exceptions |
| FR-6 | Screen addresses | Member wallet on creation, each funding source and each Redemption destination are screened; a hit blocks the vault allowlisting, payout or action and opens a case |
| FR-7 | Gate vault access | Member must accept current vault terms (versioned) and pass eligibility checks; only then is the wallet added to the Onyx allowlist |
| FR-8 | Vault deposit | Member signs exact-amount approval and deposit request; Helm tracks approval → request → pending → executed or cancelled; position counts only after execution |
| FR-9 | Position display | Shares and value as of the vault's last valuation, with the valuation timestamp; matches chain state |
| FR-10 | Redemption | Member signs a redemption request; Helm shows pending, awaiting liquidity, executed, cancelled; asset arrives in the Member's wallet; position, business events and any Commission adjustment follow the approved rule |
| FR-11 | Games and Points | Linked game account; verified events award Points once; rules and daily limits visible; Points shown separately from money (REW-01) |
| FR-12 | Support | Verified chat identity; agent context view shows identity, Customer or Builder status, community status, earnings and payout state, and case history (SUP-01); cases link to person and event IDs (SUP-04); agent actions limited (SUP-05); FAQs and runbooks versioned (SUP-06); logout resets the chat |
| FR-13 | Admin and reconciliation | Separate view, configure, correct, approve and release roles (ADM-01); daily reconciliation of genealogy, funding, vault positions, Commissions, payouts and Points; mismatches in an exception queue with audit trail |
| FR-14 | Reporting | Separate definitions for customers, Builders, deposits, Commissions, liabilities and payouts, with cutoffs and freshness shown and no double counting (BI-01, BI-02) |
| FR-15 | Customer and Builder status, preregistration | Prospect, preregistered, verified and enrolled states tracked separately; Builder enrollment explicit and versioned; preregistered people cannot receive earnings (ID-04); restricted capabilities blocked by country and agreement version (ID-03, REC-02) |
| FR-16 | Team view | Builder sees referral link, direct team members and counts with freshness; cannot see another branch or anyone's balances, positions, trades or support cases (TEAM-01, TEAM-02, BO-01) |
| FR-17 | Post eligible events for Commission | Only the approved eligible event type is posted, after on-chain confirmation, with a stable external ID; replays create one obligation; reversals create a traceable adjustment (COMP-01, COMP-02) |
| FR-18 | Simple payout | Released bonuses arrive as a PillarsHub batch at Helm's merchant endpoint; Finance approves; Helm proposes treasury transactions to the Builder's own Helm wallet only; each payment is reported back as Success, Failure or Pending with the transaction reference; a timeout and retry produce one payment or an explicit exception (PAY-01 to PAY-03, T06) |
| FR-19 | Earnings statement and dispute | Builder sees calculated, pending, held, payable and paid amounts with reasons (COMP-03); period statement separates vault performance from referral earnings (AUD-03); a dispute request carries the earning ID (BO-02) |
| FR-20 | Alpha community import | Alpha members imported Sponsors-first with original dates and provenance "import"; counts and edges reconcile; exceptions resolved or approved; rollback rehearsed (GEN-03, IMP-02, T01) |

## Operational requirements

- Every integration write is idempotent from Helm's side, retried with backoff and reconciled daily (API-02).
- No private key, seed phrase or privileged provider credential reaches the browser, logs or support payloads (SUP-03).
- Separate test and production environments for every provider, with separate credentials (ADM-03).
- Monitoring and alerts for: stale vault valuation, deposit or redemption requests pending beyond target, reconciliation breaks, sync failures, screening hits, payout batches not confirmed within the agreed window.
- An agreed load envelope (people, tree depth, events per hour) and recovery targets before production testing (OPS-01, OPS-03).

## Success metrics (targets TBD)

Time to first approved live deposit and to first payout; signup completion; signup-to-funded and funded-to-deposited conversion; referral attribution completeness (target 100% of accepted signups); alpha import reconciliation (target zero unexplained differences); payout batch accuracy; reconciliation exceptions per week; game participation; support first-response and resolution time.

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
    ADM[Admin console and approvals]
    PAYX[Payout executor: merchant endpoint]
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
  PH -->|payout batch| PAYX
  PAYX -->|propose transfers| SAFE[(Treasury Safe multisig)]
  SAFE -->|USDC to Builder wallets| CHAIN
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
| Admin console and approvals | Exceptions, screening cases, allowlist status, Sponsor corrections, import exceptions, payout batch review and holds, all with maker-checker | Approval workflows (ADM-02) span several providers |
| Payout executor | Receives PillarsHub payout batches at a custom merchant endpoint; validates the callback token; checks payees and holds; proposes USDC transfers to the treasury multisig; reports Success, Failure or Pending per payment | PillarsHub calculates and releases but does not move crypto; no payment provider in scope |
| Alpha import tool | Loads alpha members Sponsors-first, reconciles counts and edges, reports exceptions, supports rollback | No bulk import API in PillarsHub. Verified |

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
| Commission obligations (calculated, released) | **PillarsHub** bonuses and batches | Statement copy with source event IDs |
| Payout execution | Blockchain (treasury transfers) | Payout record with batch, payment and transaction IDs; status reported to PillarsHub |
| Customer and Builder status, preregistration | Helm DB | Master; mirrored to PillarsHub customer type and status |
| Points balance | Cyclone points service | Display copy |
| Conversations | Chatwoot | Link to member ID |
| Terms acceptance, screening results, eligibility | Helm DB | Master |

## Credentials, signing and custody boundaries

| Actor | Can sign or act | Cannot | Notes |
|---|---|---|---|
| Member | Wallet transfers, vault approval, deposit and redemption requests, cancellations | Admin actions | Privy embedded wallet; Onyx requires the Member's own address to sign its requests. Verified |
| Helm backend | PillarsHub writes (customers, nodes, sources) with a limited token; game API; screening API; vault allowlist updates through a list-owner key; **propose** treasury payout transactions | Move Member funds; vault admin actions; execute a payout without Finance signatures | List-owner key held in a key management service; owns only the allowlist contract (to confirm with Enzyme) |
| Vault Owner (Business) | Add and remove Admins; any admin action | — | Recommended: Safe multisig with Business signers |
| Vault Admin / operator (Business) | Update valuation; execute queues; move assets to the strategy wallet; set fees | — | Fully trusted by the protocol. Verified |
| Treasury signers (Finance) | Approve and sign payout transactions from the treasury multisig | Change payout destinations | Payouts go only to the Builder's Helm wallet; a threshold of Finance signers is required |
| Strategy Manager (Business-appointed) | Runs the strategy outside Onyx; returns liquidity | — | Custody of the strategy wallet sits outside Onyx. Verified |
| Enzyme | Deploys; upgrades contracts (global owner) | — | Upgrade governance must be in the MLA. Verified |
| Privy | Runs the signing enclave | Sign for the Member | Privy "is never an authorized signer". Verified |
| Support agent | Reply in Chatwoot; read-only member status | Funds, Sponsors, Points | Enforced in Helm admin |

PillarsHub tokens are environment-bound and do not expire; they can be made read-only. Recommended: a read-only token for reconciliation and a separate write token, with destructive areas denied if PillarsHub allows it (TBD). Bonus release and batch creation are Finance actions in the PillarsHub Portal, not calls from Helm's backend; Helm only receives the resulting batch and reports payment status.

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

```{.mermaid #fig-flow-payout caption="Eligible event to Commission and simple payout."}
sequenceDiagram
  participant H as Helm backend
  participant X as PillarsHub
  participant F as Finance approver
  participant T as Treasury Safe
  participant B as Builder wallet
  H->>X: post eligible event (externalId = chain:tx:log)
  X->>X: calculate 3-level Commission (pending)
  F->>X: period close, hold passed, release bonuses
  X->>H: payout batch (callback token)
  H->>H: validate token, payee status, holds
  H->>T: propose USDC transfers
  F->>T: approve and sign (threshold)
  T->>B: USDC transfer
  H->>X: report Success / Failure / Pending per payment
  H->>H: statement updated, reconcile
```

## Flow matrix

| Flow | Origin → destination | Minimum data | Authoritative record | Deduplication key | Failure and retry | User sees |
|---|---|---|---|---|---|---|
| Signup and referral | App → Helm → PillarsHub | Privy DID, wallet address, invite code, Sponsor member ID | PillarsHub tree (accepted edge) | Helm member ID (PillarsHub customer ID) | Look up before create; backoff; dead letter to ops; nightly tree reconciliation | "Referral pending" then "confirmed" |
| Wallet funding | Exchange → chain → Helm indexer | Chain, tx hash, log index, amount, from, to | Chain | (chain, tx hash, log index) | Re-index from last safe block; reorg handling by confirmation depth | Pending → confirmed balance |
| Vault deposit | App → Onyx contracts; indexer → Helm | Request ID, amount, wallet, terms version | Chain (queue and shares) | (chain, queue address, request ID) | Reverted transactions shown with reason; stale pending alert; Onyx API cross-check | Approval → requested → processing → position |
| Eligible event (approved basis only) | Helm → PillarsHub sources | Member node, amount, business time, receipt time, settlement state, rule version | Helm business event; PillarsHub source | Source externalId = chain:tx:log | Look up by externalId on conflict or timeout; reversal posts a linked adjustment | Builder sees Commission as pending |
| Commission payout | PillarsHub → Helm merchant endpoint → treasury → chain | Batch ID, payment ID, node, bonus, amount, currency, period | PillarsHub (obligation); chain (payment) | Batch ID plus payment ID; transaction hash | Batch ID is the same on retries; Helm never pays a payment ID twice; unconfirmed transfers stay Pending; failures reported per payment | Pending → held → payable → paid, with transaction link |
| Game to Points | Game service → Helm | Event ID, member ID, Points, rule ID | Points service | Event ID | Signed events; replay protection; daily limits | Points balance and history |
| Redemption | App → Onyx; indexer → Helm | Request ID, shares, destination | Chain | (chain, queue address, request ID) | Awaiting-liquidity alert; cancellation after minimum duration | Requested → awaiting liquidity → paid |
| Support | App → Chatwoot; agent → Helm admin | Member ID, identity hash, non-sensitive status | Chatwoot (conversation); Helm (actions) | Conversation ID | Widget reset on logout; signed Chatwoot webhooks logged | Chat thread |

**Unavailable providers:** if PillarsHub is down, signups proceed with the referral pending and sync later. If the indexer lags, balances show "updating". If Onyx's API is unavailable, Helm relies on chain reads. If the game service is down, play is disabled and no Points are lost.

# Genealogy, Commission and Phase 1 readiness

## Minimum data model

| Table | Key fields | Purpose |
|---|---|---|
| member | helm_member_id, handle (optional, proposed by Terrel), lifecycle_state (prospect, preregistered, verified, enrolled), is_builder, builder_enrolled_at, country, created_at | Stable identity; Customer and Builder distinction (ID-01, ID-04) |
| provider_identity | helm_member_id, provider (privy, pillarshub, chatwoot, game), external_id, linked_at | Explicit mappings |
| wallet | helm_member_id, chain_id, address, source (embedded), first_seen_at, screening_status, allowlist_status | One vault and payout wallet per Member |
| agreement_acceptance | helm_member_id, agreement (member terms, Builder terms, vault terms, privacy), version, accepted_at | Versioned consent (REC-01) |
| referral_request | id, helm_member_id, referrer_member_id, invite_code, channel, captured_at, status, rejection_reason | Pending and rejected referrals; original referrer (GEN-04) |
| sponsor_edge | id, member_id, sponsor_member_id (enroller), placement_upline_id, effective_at, accepted_at, provenance (signup, import, correction), policy_version, pillarshub_sync_status, superseded_by | Full graph at every depth; sponsor and placement kept separately (GEN-01) |
| edge_correction | id, edge_id, old values, new values, reason, requested_by, approved_by, approved_at, consent_ref | Audited changes (ADM-02) |
| business_event | id, type, member_id, amount, currency, business_time, receipt_time, settlement_state, product, country, attribution, reverses_event_id, rule_version, source_ref, idempotency_key | Terrel's minimum event contract |
| commission_statement | helm_member_id, period, bonus lines with PillarsHub IDs, state (calculated, pending, held, payable, paid), payout_ref | Builder statements (COMP-03, AUD-03) |
| payout | batch_id, payment_id, helm_member_id, amount, currency, status (received, approved, proposed, signed, confirmed, failed), safe_tx_hash, chain_tx_hash, reported_at | Payout tracking (PAY-02) |
| import_run | run_id, source, counts, exceptions, approved_by, rolled_back | Alpha import evidence (IMP-02) |
| integration_outbox | id, target, payload hash, attempts, status, last_error | Reliable sync |

Only data with an identified purpose is collected. No Sponsor or member data is written on-chain.

## Rules

- **Customer versus Builder:** every Member starts as a Customer; Builder enrollment is an explicit, versioned step with Builder terms. Preregistered people keep their attribution but cannot earn (ID-04).
- **Self-referral:** rejected at capture (same member, same wallet, same verified email or phone).
- **Invalid or missing Sponsor:** attach to the company root account with provenance "no sponsor" and flag for review (decision D8).
- **Cycles and duplicates:** impossible for new Members; checked on every correction and import (GEN-02).
- **Sponsor and placement changes:** never self-service in the Pilot. Admin-only, with reason, consent reference, second approval and audit entry, then a PillarsHub node or placement update and read-back. The governed placement window (preview, consent, deadline, notifications; GEN-04 to GEN-06) is enabled only after the policy is approved (decision D10). Customer movements stay disabled in the PillarsHub tree so the two systems cannot drift.
- **Account merges:** admin process; keep the earliest accepted edge; re-point child edges with audit entries; retire the duplicate identity (ADM-04).
- **Alpha community import:** Sponsors before children, with original signup dates and provenance "import"; record by record because there is no bulk API. Verified. Reconcile counts and edges, resolve or approve every exception, and rehearse rollback before cutover (GEN-03, IMP-02).

## Proving correctness

- **Full export:** page through every node of the tree with an as-of date, not the downline endpoint, which is capped at 10 levels. Verified.
- **Nightly reconciliation:** compare Helm's accepted edges with PillarsHub nodes (count, edge-by-edge upline match, checksum). Any mismatch is an exception.
- **Staging tests before launch:** a synthetic tree at least 15 levels deep; the alpha import dry run (T01); Terrel's scenarios T02, T03, T05, T06, T07 and T11 with Finance-prepared expected results.
- **History:** PillarsHub accepts an as-of date and keeps dated placements, and Helm keeps effective timestamps, so the tree on an original earning date can be shown after a later correction (GEN-01 proof).

## Simple Commission and payout

- **Plan.** Use the three-level Unilevel plan already connected in PillarsHub staging (Correspondence). PillarsHub configures the approved rates; the plan is read-only through the API, so Helm cannot change economics. Verified.
- **Eligible event.** Helm posts only the approved event type (decision D2) to a dedicated source group, after on-chain confirmation, with external ID `chain:tx:log`. PillarsHub calculates in real time, so nothing is posted until the basis is approved. Verified.
- **Reversals.** If the approved rule adjusts Commissions on Redemption or failed events, Helm deletes the source or posts a linked adjustment before release; after payout, the agreed recovery rule applies (T05).
- **Holds and release.** Builders without required payee status or with a screening hit are held. Finance closes the period, reviews and releases bonuses in PillarsHub.
- **Execution.** PillarsHub sends the batch to Helm's merchant endpoint with a callback token, which Helm validates against PillarsHub. Helm proposes USDC transfers to each Builder's Helm wallet in the treasury Safe; Finance signers approve; Helm reports each payment's status back. Verified (batch interface).
- **Reconciliation.** Daily: eligible events → PillarsHub sources → released bonuses → batch payments → on-chain transfers → statements (COMP-04).

# Backlog, dependencies and schedule

## Prioritised backlog

| Priority | Work items | Depends on |
|---|---|---|
| **Start immediately** | App shell; Privy login and embedded wallet; member DB with Customer and Builder states; referral capture and validation; PillarsHub staging sync with read-back; alpha import tool on sample data; event pipeline and source posting (staging only); payout merchant endpoint and Safe proposals on testnet; chain indexer; Onyx deposit and redemption on Sepolia; Chatwoot widget; admin skeleton with roles; screening hook; CI, environments, secrets | Provider test access; alpha sample data |
| **Thin slice (weeks 1–3)** | End-to-end demo on test networks: signup → referral → deposit → test Commission → test payout batch → Redemption; one game-to-Points flow | Game API docs |
| **Before live funds and payouts** | Vault terms and disclosures; allowlist automation; team view and statements; Builder enrollment and terms; payout approvals, holds and reporting; alpha import rehearsal and reconciliation; support agent view, FAQs and runbooks; reconciliation jobs and alerts; country eligibility; production environments; load and recovery tests; security review fixes; operations rehearsal | Strategy, MLA, ownership, Commission basis, legal answers |
| **Deferrable (disabled)** | Governed placement window; ranks and qualification; campaigns; integrated top-up; additional chains and assets; Telegram and WhatsApp; commercial transaction monitoring; native mobile | Business demand and approved rules |

## Critical path

1. Meeting decisions D1–D12.
2. **Vault readiness:** strategy and Manager → vault configuration (asset, async queue, external allowlist, non-transferable shares, fees) → MLA signature → production deployment → ownership handover to the Business multisig.
3. **Commission basis and plan proof:** approved eligible event, rates, period and hold → PillarsHub configuration → Finance expected results match (T02).
4. **Alpha data:** records received → dry run → reconciliation → approved exceptions → rehearsed cutover (T01).
5. **Legal answers:** entity, launch countries, KYC tier, vault terms, referral payout model.
6. **Security review** of Helm's integration, payout executor and vault configuration.
7. **Operations rehearsal:** valuation, queue execution, Redemption liquidity and a small payout batch.
8. PillarsHub production launch slot (Tuesday to Thursday).

Engineering runs in parallel with items 2–5; the launch date is set by whichever finishes last.

# Launch and operational readiness

## Gate for accepting real funds and paying Commissions

All must be true; none is waived to meet a date.

1. Vault strategy, Manager, fees and Member terms approved by Business and counsel.
2. MLA signed; deployed version and audit coverage confirmed by Enzyme; upgrade governance documented.
3. Vault Owner multisig in place; Admin and list-owner keys in managed custody; no Owner or Admin key in Helm's backend.
4. Deposits and Redemptions proven on production with a small operator-funded amount.
5. Daily reconciliation passing; monitoring and alerts live; incident contacts at each provider.
6. Screening and eligibility live for the counsel-approved tier.
7. Security review completed and high-severity findings fixed.
8. Written provider acceptance of the business model (Privy, Enzyme, PillarsHub).
9. Support agent view, FAQs, runbooks and escalation procedure, including handling of flagged users and earnings disputes (SUP-01 to SUP-06).
10. Alpha import reconciled, exceptions resolved or approved, rollback rehearsed (GEN-03, IMP-02).
11. **Before the first payout:** Commission basis, rates, period and hold approved by Owen, Finance and counsel; Finance-prepared plan examples match PillarsHub results (T02); duplicate, replay and reversal scenarios pass (T03, T05); a test batch with a forced timeout produces one payment (T06); treasury Safe with Finance signers in place; payee status captured (PAY-04).
12. Load envelope and recovery targets agreed and tested (OPS-01 to OPS-03); full data export rights in the PillarsHub and Enzyme contracts (API-03).

## Security boundaries

- **Audit coverage.** ChainSecurity audited the Onyx core (December 2025), the cross-chain wallet (May 2026) and the Chainlink compliance integration (July 2026). One deployment helper added after the last audit appears in no audit scope found. Verified. Enzyme must confirm which components Helm's vault uses and that they are covered.
- **Upgrade risk.** Enzyme's global owner can upgrade all vault contracts; the audit describes this role as able to "fully drain the system", and no timelock was found. Verified. The MLA must cover notice and governance.
- **Gas sponsorship.** Privy's native sponsorship upgrades Member wallets with EIP-7702; the delegation contract is part of the security review. Verified.
- **Unsigned PillarsHub webhooks.** Treat them as hints and re-fetch through the API. Verified.
- **Payout callbacks.** PillarsHub authenticates payout batches with a callback token that Helm validates against PillarsHub's token endpoint before acting. Verified. The payout executor holds no signing key; it only proposes Safe transactions.
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
| Referral payout basis | Is paying Commissions on the chosen eligible event lawful in launch countries? | Owen + Finance + counsel | Configurable event pipe; nothing posted until approved | PillarsHub plan (verified) | **Blocker for payouts** |
| Payee status and tax reporting | What payee information is required before payout? | Finance + counsel | Payee status gate; hold process (PAY-04) | None native | Before payouts |
| Earnings disclosures | What earnings and income disclosures are required? | Business + counsel | Statements and disclosure screens (AUD-03) | — | Before payouts |
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
| Simple Commission | Three-level Unilevel on one approved eligible event; Finance-approved USDC batches from a Safe treasury | PillarsHub plan, sources and custom merchant batches (verified) | Approved basis, rates, period and hold; counsel | Owen + Finance + counsel | **Blocker for payouts** |
| Alpha import | Import before launch with history; reconcile and rehearse | Customer create with ID, date and enroller; no bulk API (verified) | Alpha records | Business + Tech | High |
| Placement window | Disabled in the Pilot; enable after policy approval | GEN-04 to GEN-06 | Placement policy | Terrel + Tim | Medium |
| Customer and Builder | Separate states; explicit Builder enrollment | ID-01, ID-04 | Builder terms | Terrel + Owen | Medium |
| Funding path | Direct crypto; no top-up provider | Paymenture publishes no assets, countries or fees and bars "pyramid schemes" (verified) | Business requirement | Business | Low |
| Points | No cash value; not linked to deposit amounts | No game docs supplied | Game API documentation; counsel review | Business + Cyclone | Medium |
| Identity checks | Gates built now; tier set by counsel; address screening from day one | No KYC in stack (verified) | Counsel decision | Business + counsel | High |

**What would change these defaults:** integrated top-up at launch adds a payment provider to the critical path; ranks, matching bonuses or a placement window at launch add plan configuration, proof scenarios and operating capacity; counsel requiring full KYC adds an identity vendor and a gate before vault access and payouts.

# Appendix A: Evidence {.unnumbered}

All links were read on 8 October 2026.

**PillarsHub:** [API authentication](https://pillars-hub.readme.io/reference/authenticating) · [Access tokens](https://pillars-hub.readme.io/reference/access-control-tokens) · [Swagger UI](https://api.pillarshub.com/swagger/index.html) · [Customer API spec](https://api.pillarshub.com/swagger/CustomerV1/swagger.json) · [Commission API spec](https://api.pillarshub.com/swagger/CommissionV1/swagger.json) · [Webhooks](https://pillars-hub.readme.io/reference/getting-started-webhooks) · [Webhook topics](https://pillars-hub.readme.io/reference/topics) · [Invoice dates and real-time commissions](https://pillars-hub.readme.io/docs/invoice-dates-are-used-to-calculate-commissions) · [Launch timing protocol](https://pillars-hub.readme.io/docs/pillars-launch-timing-protocol) · [Money-out integrations](https://pillars-hub.readme.io/docs/money-out-merchant-integration-guide) · [Terms](https://www.pillarshub.com/terms)

**Privy:** [Pricing](https://www.privy.io/pricing) · [Security FAQ](https://docs.privy.io/security/security-faqs) · [Supporting users](https://docs.privy.io/user-management/users/managing-users/supporting-your-users) · [Webhooks](https://docs.privy.io/api-reference/webhooks/overview) · [React quickstart](https://docs.privy.io/basics/react/quickstart) · [Acceptable use policy](https://www.privy.io/acceptable-use-policy)

**Enzyme Onyx:** [Product and pricing](https://enzyme.finance/products/onyx) · [Architecture](https://docs.enzyme.finance/onyx-user-documentation/getting-started/quickstart/architecture) · [Deposit control and allowlists](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/control) · [Redemptions](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/redemptions) · [User roles](https://docs.enzyme.finance/onyx-protocol/user-roles) · [Deployments and upgrades](https://docs.enzyme.finance/onyx-protocol/architecture/deployments-and-upgrades) · [Risks and limitations](https://docs.enzyme.finance/onyx-protocol/security/risks-and-limitations) · [SDK](https://docs.enzyme.finance/onyx-sdk) · [Public API](https://api.onyx.enzyme.finance/reference) · [Contracts](https://github.com/enzymefinance/protocol-onyx) · [Audits](https://github.com/enzymefinance/protocol-onyx/tree/main/audits)

**Chatwoot:** [Developer docs](https://developers.chatwoot.com/introduction) · [Pricing](https://www.chatwoot.com/pricing)

**Funding and compliance:** [Paymenture](https://paymenture.com/) · [Bridge developer agreement](https://www.bridge.xyz/legal/developer-agreement) · [Chainalysis sanctions oracle](https://go.chainalysis.com/chainalysis-oracle-docs.html) · [FATF 2021 guidance](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html)

Detailed notes with every source and quotation are in `work/notes/01-pillarshub.md`, `02-enzyme-onyx.md`, `03-privy.md` and `04-chatwoot-funding-compliance.md`.

# Appendix B: Assumptions and gaps {.unnumbered}

- **Terrel's requirements v0.2 are traced in section 9.** Still missing from its "Waiting for" list: the compensation specification with worked examples, alpha enrollment and genealogy records, and a one-page release scope (audience, countries, languages, activities). Owners in Terrel's draft (Tim, Darren, JT, Finance, compliance) are proposals and are not repeated as commitments here.
- **Commission basis:** not yet approved. The design supports any single eligible event type; nothing is posted until Owen, Finance and counsel approve it.
- **Game and Points:** no API documentation was supplied. Needed: account linking method, event schema and signing, duplicate and replay protection, abuse controls, Points rules engine, whether Points can be redeemed for anything.
- **Not verified with providers:** PillarsHub auto-placement, depth limits, sponsor correction method, token permission granularity, rate limits, 409 semantics, pricing and security certifications; Privy paid-tier volume limits and business-model acceptance; Enzyme lead times, deployed version, external allowlist ownership, commercial terms; Chatwoot webhook retry behaviour.
- **Pricing:** Enzyme's public price differs from the correspondence; PillarsHub pricing is not public.
- **Team capacity, budget and launch cohort** were not supplied; schedule ranges assume about five to six engineers.
- **Placement-window expectations** from Nic's field call are not yet a published policy; the window stays disabled until it is.

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
10. Custom money-out merchant: can the batch carry a custom currency code such as USDC; retry behaviour when Helm reports Pending; how Failure is re-released; per-payment limits?
11. Can Helm's three-level Unilevel staging plan be configured with Finance's rates, period, hold and minimum, and who changes it (the plan is read-only through the API)?
12. Customer types or statuses for Customer versus Builder, and for preregistered people who must not earn.

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
